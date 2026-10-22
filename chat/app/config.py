import os
from dataclasses import dataclass, field
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent.parent


def _env(name: str, default: str) -> str:
    return os.environ.get(name, default)


@dataclass(frozen=True)
class Settings:
    llm_url: str = _env("LLM_URL", "http://localhost:8080")
    embed_url: str = _env("EMBED_URL", "http://localhost:8081")
    # Must match llama-server --parallel
    llm_slots: int = int(_env("LLM_SLOTS", "3"))
    max_queue: int = int(_env("MAX_QUEUE", "12"))
    max_tokens: int = int(_env("MAX_TOKENS", "700"))
    temperature: float = float(_env("TEMPERATURE", "0.2"))

    corpus_file: Path = Path(_env("CORPUS_FILE", str(APP_DIR / "corpus.yaml")))
    rules_file: Path = Path(_env("RULES_FILE", str(APP_DIR / "rules.yaml")))
    data_dir: Path = Path(_env("DATA_DIR", str(APP_DIR / ".data")))
    github_token: str = _env("GITHUB_TOKEN", "")
    refresh_hours: float = float(_env("REFRESH_HOURS", "24"))
    # Prebuilt embeddings from .github/workflows/chat_index.yml; {model} = slug
    embed_seed_url: str = _env(
        "EMBED_SEED_URL",
        "https://github.com/hotosm/docs/releases/download/chat-index/embeddings-{model}.npz",
    )

    top_k: int = int(_env("TOP_K", "4"))
    # Cosine similarity (bge-m3) below which we refuse to answer
    min_score: float = float(_env("MIN_SCORE", "0.45"))

    allowed_origins: list[str] = field(
        default_factory=lambda: [
            o.strip()
            for o in _env(
                "ALLOWED_ORIGINS", "https://docs.hotosm.org,http://localhost:3000"
            ).split(",")
            if o.strip()
        ]
    )
    rate_limit_per_min: int = int(_env("RATE_LIMIT_PER_MIN", "10"))
    trust_proxy: bool = _env("TRUST_PROXY", "true").lower() == "true"


settings = Settings()
