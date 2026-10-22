"""Fetch markdown docs from local paths or GitHub and split into chunks."""

import asyncio
import hashlib
import json
import logging
import os
import re
from dataclasses import dataclass
from pathlib import Path

import httpx
import yaml

from .website import load_news

log = logging.getLogger(__name__)

CHUNK_TARGET = 1200  # characters (~300 tokens)
CHUNK_MIN = 250


@dataclass
class Doc:
    source: str
    path: str
    url: str
    title: str
    text: str
    weight: float
    # Heading anchors exist on mkdocs/starlight/jekyll sites, not GitHub or the roadmap
    anchors: bool = False


@dataclass
class Chunk:
    id: str
    source: str
    title: str
    heading: str
    url: str
    text: str
    weight: float


def glob_to_regex(pattern: str) -> re.Pattern:
    out, i = "", 0
    while i < len(pattern):
        if pattern.startswith("**/", i):
            out, i = out + "(?:.*/)?", i + 3
        elif pattern.startswith("**", i):
            out, i = out + ".*", i + 2
        elif pattern[i] == "*":
            out, i = out + "[^/]*", i + 1
        elif pattern[i] == "?":
            out, i = out + "[^/]", i + 1
        else:
            out, i = out + re.escape(pattern[i]), i + 1
    return re.compile(f"^{out}$")


def path_matches(path: str, include: list[str], exclude: list[str]) -> bool:
    if not any(glob_to_regex(p).match(path) for p in include):
        return False
    return not any(glob_to_regex(p).match(path) for p in exclude)


FRONT_MATTER = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.S)


def split_front_matter(text: str) -> tuple[dict, str]:
    m = FRONT_MATTER.match(text)
    if not m:
        return {}, text
    try:
        meta = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        meta = {}
    return (meta if isinstance(meta, dict) else {}), text[m.end() :]


def page_url(cfg: dict, repo: str, ref: str, path: str, meta: dict) -> str:
    mode = cfg.get("mode", "github")
    base = cfg.get("base", "")
    if path in cfg.get("paths", {}):
        return cfg["paths"][path]
    if mode == "jekyll" and meta.get("permalink"):
        return base.rstrip("/") + "/" + str(meta["permalink"]).lstrip("/")
    if mode in ("mkdocs", "starlight"):
        rel = path.removeprefix(cfg.get("strip", ""))
        rel = re.sub(r"(\.en)?\.(mdx?|rst)$", "", rel)  # .en: mkdocs-static-i18n
        rel = re.sub(r"(^|/)(index|README)$", r"\1", rel)
        if mode == "starlight":
            rel = rel.lower()
        return base + (rel + "/" if rel and not rel.endswith("/") else rel)
    return f"https://github.com/{repo}/blob/{ref}/{path}"


def clean_markdown(text: str) -> str:
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    text = re.sub(r"```mermaid.*?```", "", text, flags=re.S)
    text = re.sub(r"^(import|export) .*$", "", text, flags=re.M)  # mdx
    text = re.sub(r"!\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"</?[A-Za-z][^>]*>", "", text)
    text = re.sub(r"\{%.*?%\}|\{\{.*?\}\}", "", text)  # jekyll liquid
    text = re.sub(r"^(?:\s*(?:\*\*\*|---|___)\s*)$", "", text, flags=re.M)
    return re.sub(r"\n{3,}", "\n\n", text).strip()


RST_UNDERLINE = re.compile(r"""^(.+)\n([=\-`~^"'*+#])\2{2,}\s*$""", re.M)


def clean_rst(text: str) -> str:
    """Rough reStructuredText -> markdown, enough for chunking and embedding."""
    # Comments (".." not followed by a directive or label) and their indented body
    text = re.sub(r"^\.\.(?!\s+[\w-]+::)(?!\s+_)[^\n]*\n(?:[ \t]+[^\n]*\n|[ \t]*\n)*", "", text, flags=re.M)
    text = re.sub(r"^\.\.\s+_[^:]+:.*$", "", text, flags=re.M)  # labels
    text = re.sub(r"^\.\.\s+[\w-]+::.*$", "", text, flags=re.M)  # directive lines
    text = re.sub(r"^[ \t]+:[\w-]+:.*$", "", text, flags=re.M)  # directive options
    levels: list[str] = []

    def heading(m: re.Match) -> str:
        char = m.group(2)
        if char not in levels:
            levels.append(char)
        return "#" * min(levels.index(char) + 1, 3) + " " + m.group(1).strip()

    # Headings first: backtick underlines would otherwise look like inline code
    text = RST_UNDERLINE.sub(heading, text)
    text = re.sub(r":[\w:-]+:`([^`<]+?)\s*(?:<[^>]*>)?`", r"\1", text)  # roles
    text = re.sub(r"`([^`<]+?)\s*<[^>]+>`__?", r"\1", text)  # links
    text = re.sub(r"``([^`\n]+)``", r"`\1`", text)
    text = re.sub(r"^\s*::\s*$", "", text, flags=re.M)  # literal block markers
    text = re.sub(r"(\S)::\s*$", r"\1:", text, flags=re.M)
    return text


def roadmap_docs(src: dict, raw: str) -> list[Doc]:
    """hotosm/roadmap data.json (exported from Linear) -> one doc per item + overview."""
    data = json.loads(raw)
    as_of = str(data.get("generatedAt", ""))[:10]
    url = src.get("url", {}).get("base", "")
    weight = float(src.get("weight", 1.0))

    def month(v) -> str:
        return v[:7] if v else "not set"

    docs, by_status = [], {}
    for item in data.get("items", []):
        title, status = item.get("title", "").strip(), item.get("status", "")
        by_status.setdefault(status, []).append(title)
        theme = item.get("group", "")
        lines = [
            f"# Roadmap: {title}",
            "",
            f"Status: {status}. Start: {month(item.get('startDate'))}. "
            f"Target: {month(item.get('targetDate'))}.",
        ]
        if theme and theme != "Roadmap item":
            lines.append(f"Theme: {theme}.")
        if item.get("summary"):
            lines += ["", item["summary"].strip()]
        # Linked work items: titles and state only (no assignees)
        work = [
            f"- {i['title'].strip()} ({i.get('state', {}).get('name', '?')})"
            for i in item.get("issues", [])
            if i.get("title") and i.get("state", {}).get("type") != "canceled"
        ]
        if work:
            lines += ["", "Work items:"] + work
        lines += ["", f"From HOT's public roadmap as of {as_of}; target dates may change."]
        docs.append(Doc(src["name"], "data.json", url, f"Roadmap: {title}", "\n".join(lines), weight))

    overview = [f"# HOT tools roadmap overview", "", f"HOT's public roadmap as of {as_of}."]
    for status, titles in sorted(by_status.items()):
        overview += ["", f"## {status}", ""] + [f"- {t}" for t in sorted(titles)]
    docs.append(Doc(src["name"], "data.json", url, "HOT tools roadmap overview", "\n".join(overview), weight))
    return docs


def slugify(heading: str) -> str:
    s = re.sub(r"[^\w\s-]", "", heading.lower()).strip()
    return re.sub(r"[\s]+", "-", s)


HEADING = re.compile(r"^(#{1,3})\s+(.+?)\s*#*\s*$", re.M)
SETEXT = re.compile(r"^(.+)\n(=+|-+)\s*$", re.M)


def chunk_doc(doc: Doc) -> list[Chunk]:
    text = SETEXT.sub(
        lambda m: ("# " if m.group(2)[0] == "=" else "## ") + m.group(1), doc.text
    )
    sections: list[tuple[str, str]] = []
    last, heading = 0, ""
    for m in HEADING.finditer(text):
        sections.append((heading, text[last : m.start()].strip()))
        heading, last = m.group(2).strip(), m.end()
    sections.append((heading, text[last:].strip()))

    # Merge tiny sections forward, split long ones on paragraphs
    merged: list[tuple[str, str]] = []
    carry_h, carry = "", ""
    for h, body in sections:
        if not body:
            carry_h = carry_h or h
            continue
        h = h or carry_h
        body = f"{carry}\n\n{body}".strip() if carry else body
        carry_h, carry = "", ""
        if len(body) < CHUNK_MIN:
            carry_h, carry = h, (f"{h}\n{body}" if h else body)
            continue
        merged.append((h, body))
    if carry:
        if merged:
            h, body = merged[-1]
            merged[-1] = (h, f"{body}\n\n{carry}")
        else:
            merged.append((carry_h, carry))

    chunks = []
    for h, body in merged:
        parts, buf = [], ""
        paras = []
        for para in re.split(r"\n\s*\n", body):
            # Hard-wrap huge blocks (tables, code) on line boundaries
            while len(para) > CHUNK_TARGET * 2:
                cut = para.rfind("\n", 0, CHUNK_TARGET)
                cut = cut if cut > 0 else CHUNK_TARGET
                paras.append(para[:cut])
                para = para[cut:].lstrip("\n")
            paras.append(para)
        for para in paras:
            if buf and len(buf) + len(para) > CHUNK_TARGET:
                parts.append(buf)
                buf = para
            else:
                buf = f"{buf}\n\n{para}" if buf else para
        if buf:
            parts.append(buf)
        anchor = f"#{slugify(h)}" if h and doc.anchors else ""
        for i, part in enumerate(parts):
            header = f"{doc.title} > {h}" if h and h != doc.title else doc.title
            cid = hashlib.sha1(f"{doc.url}|{h}|{i}|{part}".encode()).hexdigest()[:16]
            chunks.append(
                Chunk(
                    id=cid,
                    source=doc.source,
                    title=doc.title,
                    heading=h,
                    url=doc.url + anchor,
                    text=f"{header}\n\n{part}",
                    weight=doc.weight,
                )
            )
    return chunks


def path_weight(src: dict, path: str) -> float:
    for pattern, w in src.get("path_weights", {}).items():
        if path_matches(path, [pattern], []):
            return float(w)
    return float(src.get("weight", 1.0))


def make_doc(src: dict, path: str, raw: str) -> Doc | None:
    meta, body = split_front_matter(raw)
    if path.endswith(".rst"):
        body = clean_rst(body)
    body = clean_markdown(body)
    if len(body) < 80:
        return None
    h1 = re.search(r"^#\s+(.+)$", body, re.M) or re.search(r"^(.+)\n=+\s*$", body, re.M)
    title = src.get("titles", {}).get(path) or meta.get("title") or (h1 and h1.group(1))
    title = str(title or Path(path).stem).strip()
    return Doc(
        source=src["name"],
        path=path,
        url=page_url(src.get("url", {}), src["repo"], src["ref"], path, meta),
        title=title,
        text=body,
        weight=path_weight(src, path),
        anchors=src.get("url", {}).get("mode") in ("mkdocs", "starlight", "jekyll"),
    )


class CorpusLoader:
    def __init__(self, corpus_file: Path, cache_dir: Path, github_token: str = ""):
        cfg = yaml.safe_load(corpus_file.read_text())
        self.default_exclude = cfg.get("defaults", {}).get("exclude", [])
        self.sources = cfg["sources"]
        self.cache_dir = cache_dir / "corpus"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        headers = {"User-Agent": "hotosm-docs-chat"}
        if github_token:
            headers["Authorization"] = f"Bearer {github_token}"
        self.headers = headers

    async def load(self) -> list[Doc]:
        async with httpx.AsyncClient(
            headers=self.headers, timeout=30, follow_redirects=True
        ) as client:
            results = await asyncio.gather(
                *(self._load_source(client, s) for s in self.sources),
                return_exceptions=True,
            )
        docs: list[Doc] = []
        for src, res in zip(self.sources, results):
            if isinstance(res, BaseException):
                log.error("Failed to load %s: %s", src["name"], res)
                continue
            log.info("Loaded %d docs from %s", len(res), src["name"])
            docs.extend(res)
        return docs

    def _patterns(self, src: dict) -> tuple[list[str], list[str]]:
        return src["include"], self.default_exclude + src.get("exclude", [])

    async def _load_source(self, client: httpx.AsyncClient, src: dict) -> list[Doc]:
        if src.get("type") == "hotosm-news":
            # Use a separate client to keep the GitHub token off this request
            async with httpx.AsyncClient(
                headers={"User-Agent": "hotosm-docs-chat"}, timeout=30, follow_redirects=True
            ) as web:
                posts = await load_news(web, src, self.cache_dir)
            return [
                # Date each title so chunks show their age
                Doc(src["name"], p["url"], p["url"], f"{p['title']} (news, {p['date']})",
                    p["text"], float(src.get("weight", 1.0)))
                for p in posts
            ]
        include, exclude = self._patterns(src)
        local = Path(src["local"]) if src.get("local") else None
        if local and local.is_dir():
            files = {}
            for root, dirs, names in os.walk(local):
                # Skip hidden dirs (.git, .venv) and build output
                dirs[:] = [d for d in dirs if not d.startswith(".") and d not in ("node_modules", "site")]
                for name in names:
                    rel = os.path.relpath(os.path.join(root, name), local)
                    if path_matches(rel, include, exclude):
                        files[rel] = Path(root, name).read_text(errors="ignore")
        else:
            files = await self._fetch_github(client, src, include, exclude)
        if src.get("transform") == "roadmap":
            return [d for raw in files.values() for d in roadmap_docs(src, raw)]
        return [d for path, raw in sorted(files.items()) if (d := make_doc(src, path, raw))]

    async def _fetch_github(
        self, client: httpx.AsyncClient, src: dict, include: list[str], exclude: list[str]
    ) -> dict[str, str]:
        repo, ref = src["repo"], src["ref"]
        cache = self.cache_dir / (re.sub(r"\W", "_", f"{repo}_{ref}") + ".json")
        cached = json.loads(cache.read_text()) if cache.exists() else None
        patterns = [include, exclude]
        if cached and cached.get("patterns") != patterns:
            # corpus.yaml changed: cached files may be the wrong set
            cached = None
        try:
            r = await client.get(
                f"https://api.github.com/repos/{repo}/git/trees/{ref}?recursive=1"
            )
            r.raise_for_status()
            tree = r.json()
        except httpx.HTTPError:
            if cached:
                log.warning("GitHub unavailable for %s, using cache", repo)
                return cached["files"]
            raise
        if cached and cached.get("sha") == tree["sha"]:
            return cached["files"]

        paths = [
            e["path"]
            for e in tree["tree"]
            if e["type"] == "blob" and path_matches(e["path"], include, exclude)
        ]
        sem = asyncio.Semaphore(8)

        async def fetch(path: str) -> tuple[str, str]:
            async with sem:
                r = await client.get(
                    f"https://raw.githubusercontent.com/{repo}/{ref}/{path}"
                )
                r.raise_for_status()
                return path, r.text

        files = dict(await asyncio.gather(*(fetch(p) for p in paths)))
        cache.write_text(json.dumps({"sha": tree["sha"], "patterns": patterns, "files": files}))
        return files


def chunk_all(docs: list[Doc]) -> list[Chunk]:
    return [c for d in docs for c in chunk_doc(d)]
