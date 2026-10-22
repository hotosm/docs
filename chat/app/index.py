"""Hybrid (dense + BM25) search over doc chunks, embeddings via llama-server."""

import asyncio
import hashlib
import logging
import math
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

import httpx
import numpy as np

from .corpus import Chunk

log = logging.getLogger(__name__)

TOKEN = re.compile(r"[a-z0-9]+")
STOPWORDS = set(
    "a an and are as at be by can do does for from how i in is it my of on or "
    "our the this to we what when where which who why with you your".split()
)


def tokenize(text: str) -> list[str]:
    return [t for t in TOKEN.findall(text.lower()) if t not in STOPWORDS]


def find_tools(text: str, tools: dict[str, list[str]]) -> list[str]:
    """Find tool names, matching longer aliases first ("field tm" before "tm").

    Aliases containing capitals match case-sensitively.
    """
    aliases = sorted(
        ((a, name) for name, al in tools.items() for a in al), key=lambda x: -len(x[0])
    )
    found: list[str] = []
    for alias, name in aliases:
        flags = 0 if alias != alias.lower() else re.I
        pattern = re.compile(rf"(?<![\w-]){re.escape(alias)}(?![\w-])", flags)
        if pattern.search(text):
            text = pattern.sub(" ", text)
            if name not in found:
                found.append(name)
    return found


class Embedder:
    """Embed via llama-server with one .npz cache per model.

    A prebuilt CI cache seeds the first run; only changed chunks need embedding.
    """

    def __init__(self, url: str, data_dir: Path, seed_url: str = "", batch: int = 16):
        self.url = url.rstrip("/")
        self.data_dir = data_dir
        self.seed_url = seed_url
        self.batch = batch
        self.model = ""
        self.cache_file: Path | None = None
        self.cache: dict[str, np.ndarray] = {}
        self.progress: tuple[int, int] = (0, 0)  # (embedded, to embed) in current run

    @staticmethod
    def _load(path: Path) -> dict[str, np.ndarray]:
        data = np.load(path, allow_pickle=False)
        return dict(zip(data["keys"].tolist(), data["vecs"]))

    def save(self) -> None:
        if not self.cache or not self.cache_file:
            return
        keys = np.array(list(self.cache.keys()))
        vecs = np.stack(list(self.cache.values()))
        tmp = self.cache_file.with_suffix(".tmp.npz")
        np.savez(tmp, keys=keys, vecs=vecs)
        tmp.replace(self.cache_file)

    def prune(self, texts: list[str]) -> None:
        keep = {hashlib.sha1(t.encode()).hexdigest() for t in texts}
        self.cache = {k: v for k, v in self.cache.items() if k in keep}

    async def init(self, timeout: float = 1800) -> None:
        """Wait for the server, then load (or seed) the cache for its model."""
        deadline = asyncio.get_event_loop().time() + timeout
        async with httpx.AsyncClient(timeout=10, follow_redirects=True) as client:
            while True:
                try:
                    r = await client.get(f"{self.url}/v1/models")
                    if r.status_code == 200:
                        self.model = r.json()["data"][0]["id"]
                        break
                except (httpx.HTTPError, KeyError, IndexError):
                    pass
                if asyncio.get_event_loop().time() > deadline:
                    raise TimeoutError("Embedding server not ready")
                await asyncio.sleep(3)

            # Use the basename so -m paths and -hf repo names share a cache slug.
            slug = re.sub(r"[^a-z0-9]+", "-", self.model.rsplit("/", 1)[-1].lower()).strip("-")
            cache_file = self.data_dir / f"embeddings-{slug}.npz"
            if not cache_file.exists():
                # Adopt a cache saved under an older, path-prefixed name
                for old in self.data_dir.glob(f"embeddings-*-{slug}.npz"):
                    old.replace(cache_file)
                    break
            if cache_file == self.cache_file:
                return
            self.cache_file, self.cache = cache_file, {}
            if cache_file.exists():
                self.cache = self._load(cache_file)
            elif self.seed_url:
                url = self.seed_url.format(model=slug)
                try:
                    r = await client.get(url, timeout=60)
                    r.raise_for_status()
                    tmp = cache_file.with_suffix(".seed.npz")
                    tmp.write_bytes(r.content)
                    self.cache = self._load(tmp)
                    tmp.replace(cache_file)
                    log.info("Seeded %d embeddings from %s", len(self.cache), url)
                except Exception as e:  # noqa: BLE001 - seeding is best effort
                    log.warning("No embedding seed from %s (%s), embedding everything", url, e)

    async def _embed_batch(self, client: httpx.AsyncClient, texts: list[str]) -> np.ndarray:
        r = await client.post(f"{self.url}/v1/embeddings", json={"input": texts})
        r.raise_for_status()
        vecs = np.array([d["embedding"] for d in r.json()["data"]], dtype=np.float32)
        return vecs / np.linalg.norm(vecs, axis=1, keepdims=True).clip(min=1e-9)

    async def embed(self, texts: list[str]) -> np.ndarray:
        keys = [hashlib.sha1(t.encode()).hexdigest() for t in texts]
        missing = [i for i, k in enumerate(keys) if k not in self.cache]
        self.progress = (0, len(missing))
        if missing:
            async with httpx.AsyncClient(timeout=120) as client:
                for start in range(0, len(missing), self.batch):
                    idx = missing[start : start + self.batch]
                    vecs = await self._embed_batch(client, [texts[i] for i in idx])
                    for i, v in zip(idx, vecs):
                        self.cache[keys[i]] = v
                    done = min(start + self.batch, len(missing))
                    self.progress = (done, len(missing))
                    if len(missing) > self.batch and done % (self.batch * 8) == 0:
                        log.info("Embedded %d/%d", done, len(missing))
                        self.save()  # resume here if interrupted
        return np.stack([self.cache[k] for k in keys])


@dataclass
class Hit:
    chunk: Chunk
    score: float  # cosine similarity
    rank_score: float


class SearchIndex:
    def __init__(self, chunks: list[Chunk], vectors: np.ndarray):
        self.chunks = chunks
        self.vectors = vectors
        self.doc_tokens = [tokenize(c.text) for c in chunks]
        self.avgdl = sum(map(len, self.doc_tokens)) / max(len(chunks), 1)
        df: Counter = Counter()
        self.postings: dict[str, list[tuple[int, int]]] = defaultdict(list)
        for i, toks in enumerate(self.doc_tokens):
            for term, tf in Counter(toks).items():
                df[term] += 1
                self.postings[term].append((i, tf))
        n = len(chunks)
        self.idf = {t: math.log(1 + (n - f + 0.5) / (f + 0.5)) for t, f in df.items()}

    def bm25(self, query: str, k1: float = 1.2, b: float = 0.75) -> np.ndarray:
        scores = np.zeros(len(self.chunks), dtype=np.float32)
        for term in set(tokenize(query)):
            idf = self.idf.get(term)
            if idf is None:
                continue
            for i, tf in self.postings[term]:
                dl = len(self.doc_tokens[i])
                scores[i] += idf * tf * (k1 + 1) / (tf + k1 * (1 - b + b * dl / self.avgdl))
        return scores

    def search(self, query_vec: np.ndarray, query: str, k: int, rrf_k: int = 60) -> list[Hit]:
        if not self.chunks:
            return []
        dense = self.vectors @ query_vec
        lexical = self.bm25(query)
        fused = np.zeros(len(self.chunks), dtype=np.float32)
        for scores in (dense, lexical):
            order = np.argsort(-scores)[:100]
            for rank, i in enumerate(order):
                if scores[i] > 0:
                    fused[i] += 1.0 / (rrf_k + rank)
        fused *= np.array([c.weight for c in self.chunks], dtype=np.float32)

        hits, seen_urls = [], Counter()
        for i in np.argsort(-fused):
            if fused[i] <= 0 or len(hits) >= k:
                break
            c = self.chunks[i]
            page = c.url.split("#")[0]
            # Diversity: at most two chunks from one page
            if seen_urls[page] >= 2:
                continue
            seen_urls[page] += 1
            hits.append(Hit(chunk=c, score=float(dense[i]), rank_score=float(fused[i])))
        return hits
