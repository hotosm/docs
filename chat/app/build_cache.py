"""Build the full corpus embedding cache for CI.

    EMBED_URL=http://localhost:8081 DATA_DIR=.data python -m app.build_cache
"""

import asyncio

from .config import settings
from .corpus import CorpusLoader, chunk_all
from .index import Embedder


async def main() -> None:
    settings.data_dir.mkdir(parents=True, exist_ok=True)
    docs = await CorpusLoader(settings.corpus_file, settings.data_dir, settings.github_token).load()
    texts = [c.text for c in chunk_all(docs)]
    # CI restores the previous cache into DATA_DIR; no seed needed
    embedder = Embedder(settings.embed_url, settings.data_dir)
    await embedder.init()
    before = len(embedder.cache)
    await embedder.embed(texts)
    embedder.prune(texts)
    embedder.save()
    print(f"{embedder.cache_file} ({len(texts)} chunks, {before} cached before)")


if __name__ == "__main__":
    asyncio.run(main())
