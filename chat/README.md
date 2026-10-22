# HOTOSM Assistant (experimental)

A small, self-hosted chat widget for docs.hotosm.org with two modes:

1. **Plan a project**: a short questionnaire (`rules.yaml`) recommends HOT
   tools (imagery → digitisation → field → data). Rules choose the tools;
   the LLM explains the recommendation.
2. **Ask a question**: answers from the tool docs (`corpus.yaml`), with
   numbered citations. If no relevant content is found, it says so.

```text
docs.hotosm.org ── chat-widget.js ──▶ chat-api (FastAPI)
                                       ├─ planner (rules.yaml)
                                       ├─ hybrid search (bge-m3 + BM25, in memory)
                                       ├─▶ embed: llama-server, bge-m3 Q8
                                       └─▶ llm:   llama-server, Gemma 4 QAT Q4
```

The corpus (~600 pages, ~3.5k chunks) includes tool docs from GitHub and the
last two years of public hotosm.org news. It loads on startup and refreshes
every `REFRESH_HOURS`. Embeddings are cached in `/data`; only changed chunks
are re-embedded.

Embedding the full corpus on CPU takes 15–60 minutes.
`.github/workflows/chat_index.yml` prebuilds the cache daily and publishes it
to the `chat-index` release. On first start, the API downloads it
(`EMBED_SEED_URL`) and embeds only changed chunks. Without a published cache,
it indexes everything locally.

## Run locally

```bash
just chat up        # docker compose: docs + api + embed + llm
just chat logs      # wait for "Index ready" and the model to load
open http://localhost:3000
```

On first start, the `models` service (`chat/fetch-models.sh`) downloads ~6GB
to the `models` volume. Downloads resume on the next `docker compose up`;
follow progress with `docker compose logs -f models`. The widget stays hidden
until the API is reachable. Local edits to `docs/`, `chat/app`, `rules.yaml`
and `corpus.yaml` are picked up live. Restart the API to rebuild the docs
index: `docker compose restart chat-api`.

Keep `LLM_THREADS` and `EMBED_THREADS` (both default to 4) at or below your
physical core count; extra threads slow llama.cpp down. Override the model
and threads in `.env`:

```bash
# Default local: Gemma 4 E4B QAT (~6GB RAM)
# Production quality, needs ~20GB RAM:
LLM_HF_REPO=google/gemma-4-26B-A4B-it-qat-q4_0-gguf
LLM_HF_FILE=gemma-4-26B_q4_0-it.gguf
LLM_THREADS=8
```

Tests and evals:

```bash
just chat test                      # unit tests, no models needed
just chat eval                      # questions in evals/ against localhost:8000
uv run python evals/run.py -v URL   # print answers too
```

## Models

| Role          | Model                                     | Size    | Why                                                             |
| ------------- | ----------------------------------------- | ------- | --------------------------------------------------------------- |
| LLM (default) | `google/gemma-4-E4B-it-qat-q4_0-gguf`     | 5.2 GB  | Fits a shared 4 vCPU / 16GB node or a laptop                    |
| LLM (upgrade) | `google/gemma-4-26B-A4B-it-qat-q4_0-gguf` | 14.4 GB | MoE, ~4B active: similar speed, better answers, needs 32GB node |
| Embedding     | `ggml-org/bge-m3-Q8_0-GGUF`               | 0.6 GB  | Multilingual, MIT licence                                       |

Google's QAT (quantisation-aware trained) checkpoints retain near
full-precision quality at 4-bit, unlike post-hoc Q4 quants. All models use
Apache 2.0 or MIT licences.

## llama.cpp tuning

Both compose and the Helm chart use the same flags:

| Flag                         | Why                                                                    |
| ---------------------------- | ---------------------------------------------------------------------- |
| `-np 3` + `-c 24576`         | 3 concurrent slots of 8k tokens, continuously batched                  |
| `-t N` = CPU request         | llama.cpp otherwise spawns a thread per host core and thrashes         |
| `-fa on -ctk q8_0 -ctv q8_0` | Flash attention + 8-bit KV cache: half the KV memory                   |
| `--cache-ram`                | Prompt cache in RAM: shared system prompt and history aren't re-read   |
| `--reasoning-budget 0`       | No hidden "thinking" tokens: far faster first word on CPU              |
| `-lm none`                   | Load weights into RAM rather than mmap from a network volume           |
| `--model` (no `-hf`)         | Models are fetched by a resumable init step; llama.cpp only loads them |

Prompt processing is the CPU bottleneck. The API uses the top 4 chunks
(~300 tokens each), the last 6 messages and a cached system prompt. Requests
beyond the slot count queue, with live queue positions shown in the widget.

vLLM targets GPUs. For ~3 concurrent CPU users, llama.cpp provides
continuous batching with less setup.

## Tuning answers

- **Wrong tool recommended**: edit `rules.yaml` and add a case to `tests/test_recommend.py`.
- **Answer misses a page**: check that it's in `corpus.yaml`, or raise its `weight`.
- **Refuses too often / guesses too much**: adjust `MIN_SCORE` (default 0.45).
- Feedback (👍/👎) is logged as `feedback {...}` lines in the API logs.

## Deploy

- Image: `.github/workflows/chat_image.yml` → `ghcr.io/hotosm/docs/chat`
  (a GitHub release `vX.Y.Z` publishes tag `X.Y.Z`, matching the chart's `appVersion`).
- Chart: `chart/` → `oci://ghcr.io/hotosm/charts/docs-chat` (`chat_chart.yml`).
- Cluster: `k8s-infra/apps/docs-chat.yaml` (ArgoCD), host `docs-chat.k8s-prod.hotosm.org`.
