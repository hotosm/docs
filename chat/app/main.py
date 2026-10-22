import asyncio
import json
import logging
import time
from collections import defaultdict, deque
from contextlib import asynccontextmanager
from typing import Literal

import numpy as np
import yaml
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from . import prompts
from .config import settings
from .corpus import CorpusLoader, chunk_all
from .index import Embedder, SearchIndex, find_tools
from .llm import LLMClient, QueueFull, SlotQueue
from .recommend import Planner

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
log = logging.getLogger("chat")


class State:
    index: SearchIndex | None = None
    status: str = "starting"
    built_at: float = 0
    sources: dict[str, int] = {}


state = State()
settings.data_dir.mkdir(parents=True, exist_ok=True)
planner = Planner(settings.rules_file)
embedder = Embedder(settings.embed_url, settings.data_dir, settings.embed_seed_url)
tool_aliases = yaml.safe_load(settings.corpus_file.read_text()).get("tools", {})
llm = LLMClient(settings.llm_url, settings.max_tokens, settings.temperature)
queue = SlotQueue(settings.llm_slots, settings.max_queue)


async def build_index() -> None:
    state.status = "indexing" if state.index is None else state.status
    loader = CorpusLoader(settings.corpus_file, settings.data_dir, settings.github_token)
    docs = await loader.load()
    chunks = chunk_all(docs)
    log.info("Embedding %d chunks from %d docs", len(chunks), len(docs))
    await embedder.init()
    texts = [c.text for c in chunks]
    vectors = await embedder.embed(texts)
    embedder.prune(texts)
    embedder.save()
    state.index = SearchIndex(chunks, vectors)
    state.sources = {}
    for c in chunks:
        state.sources[c.source] = state.sources.get(c.source, 0) + 1
    state.status, state.built_at = "ready", time.time()
    log.info("Index ready: %d chunks", len(chunks))


async def index_loop() -> None:
    while True:
        try:
            await build_index()
        except Exception:
            log.exception("Index build failed")
            if state.index is None:
                state.status = "error"
                await asyncio.sleep(60)
                continue
        await asyncio.sleep(settings.refresh_hours * 3600)


@asynccontextmanager
async def lifespan(_: FastAPI):
    task = asyncio.create_task(index_loop())
    yield
    task.cancel()
    await llm.aclose()


app = FastAPI(title="HOTOSM Assistant (experimental)", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

_hits: dict[str, deque] = defaultdict(deque)


def client_ip(request: Request) -> str:
    if settings.trust_proxy and (fwd := request.headers.get("x-forwarded-for")):
        return fwd.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def rate_limit(request: Request) -> None:
    now, window = time.monotonic(), _hits[client_ip(request)]
    while window and now - window[0] > 60:
        window.popleft()
    if len(window) >= settings.rate_limit_per_min:
        raise HTTPException(429, "Too many questions, please wait a minute.")
    window.append(now)
    if len(_hits) > 10_000:
        _hits.clear()


class Message(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(max_length=4000)


class ChatRequest(BaseModel):
    messages: list[Message] = Field(default_factory=list, max_length=20)
    plan_answers: dict | None = None


class PlanRequest(BaseModel):
    answers: dict


class Feedback(BaseModel):
    rating: Literal["up", "down"]
    question: str = Field(default="", max_length=1000)
    answer: str = Field(default="", max_length=4000)
    comment: str = Field(default="", max_length=1000)


@app.get("/livez")
async def livez():
    return {"ok": True}


@app.get("/health")
async def health():
    return {
        "status": state.status,
        "chunks": len(state.index.chunks) if state.index else 0,
        "embedding": {"done": embedder.progress[0], "total": embedder.progress[1]},
        "sources": state.sources,
        "llm": await llm.healthy(),
        "queue": {"active": queue.active, "waiting": len(queue.waiters)},
    }


@app.get("/api/plan/questions")
async def plan_questions():
    return planner.public_config()


@app.post("/api/plan/next")
async def plan_next(req: PlanRequest):
    """Next unanswered question, or the recommendation when done."""
    answers = planner.validate(req.answers)
    for q in planner.visible_questions(answers):
        if q["id"] not in answers:
            return {"question": q, "answered": len(answers)}
    return {"plan": planner.recommend(answers)}


@app.post("/api/feedback")
async def feedback(fb: Feedback):
    log.info("feedback %s", json.dumps(fb.model_dump()))
    return {"ok": True}


def sse(event: str, data) -> str:
    return f"event: {event}\ndata: {json.dumps(data)}\n\n"


async def retrieve(queries: list[tuple[str, int]]) -> list:
    vecs = await embedder.embed([q for q, _ in queries])
    hits, seen = [], set()
    for (q, k), vec in zip(queries, vecs):
        for h in state.index.search(np.asarray(vec), q, k):
            if h.chunk.id not in seen:
                seen.add(h.chunk.id)
                hits.append(h)
    return hits


def build_messages(req: ChatRequest, plan_text: str | None, final_user: str) -> list[dict]:
    msgs = [{"role": "system", "content": prompts.SYSTEM}]
    if plan_text:
        msgs += [
            {"role": "user", "content": plan_text},
            {"role": "assistant", "content": prompts.PLAN_ACK},
        ]
    # Keep recent history to reduce CPU prompt processing
    for m in req.messages[:-1][-6:]:
        msgs.append({"role": m.role, "content": m.content[:1500]})
    msgs.append({"role": "user", "content": final_user})
    return msgs


@app.post("/api/chat")
async def chat(req: ChatRequest, request: Request):
    rate_limit(request)
    if state.index is None:
        done, total = embedder.progress
        pct = f" ({100 * done // total}%)" if total else ""
        raise HTTPException(
            503,
            f"The assistant is still indexing the docs{pct}. "
            "This only happens on first start, please try again in a few minutes.",
        )
    if not req.messages and not req.plan_answers:
        raise HTTPException(400, "Empty request")

    plan = planner.recommend(req.plan_answers) if req.plan_answers else None
    plan_text = planner.describe(plan) if plan else None
    explaining_plan = plan is not None and not req.messages

    async def prepare() -> tuple[list, str | None]:
        if explaining_plan:
            goal = plan["answers"].get("goal", "")
            queries = [(goal, 2)] if goal else []
            queries += [
                (f"{t['name']} how to get started", 1)
                for s in plan["stages"]
                for t in s["tools"]
            ]
            hits = (await retrieve(queries))[:4]
            return hits, prompts.plan_prompt(prompts.format_context(hits))

        user_msgs = [m.content for m in req.messages if m.role == "user"]
        question = user_msgs[-1]
        # Include the previous question to retrieve context for follow-ups
        query = " ".join(user_msgs[-2:])[-1000:]
        tools = find_tools(question, tool_aliases)
        if tools:
            # Spell out abbreviations ("ftm") for the embedding model
            query = f"{query} ({', '.join(tools)})"
        queries = [(query, settings.top_k)]
        if len(tools) > 1:
            # Include each tool's docs for comparisons
            queries = [(query, 2)] + [
                (f"{t}: what it does, use it when, probably not when", 2) for t in tools[:3]
            ]
        hits = [
            h for h in (await retrieve(queries))[: settings.top_k + 2]
            if h.score >= settings.min_score * 0.8
        ]
        if not hits or max(h.score for h in hits) < settings.min_score:
            if not plan_text:
                return [], None
            # Use the plan itself to answer follow-ups
            hits = []
        context = prompts.format_context(hits) or "(no matching excerpts, use the plan above)"
        return hits, prompts.question_prompt(context, question)

    async def events():
        yield sse("status", {"stage": "searching"})
        try:
            hits, final_user = await prepare()
        except Exception:
            log.exception("Retrieval error")
            yield sse("error", {"message": "Sorry, searching the docs failed. Please try again."})
            return
        if final_user is None:
            yield sse("token", {"t": prompts.NO_CONTEXT})
            yield sse("done", {"grounded": False})
            return

        yield sse(
            "sources",
            [
                {"n": n, "title": h.chunk.title, "heading": h.chunk.heading,
                 "url": h.chunk.url, "source": h.chunk.source}
                for n, h in enumerate(hits, 1)
            ],
        )

        try:
            ticket = queue.enter()
        except QueueFull:
            yield sse("error", {"message": "The assistant is busy right now. Please try again in a few minutes."})
            return
        try:
            last_pos = 0
            while not ticket.done():
                if (pos := queue.position(ticket)) != last_pos:
                    last_pos = pos
                    yield sse("status", {"stage": "queued", "position": pos})
                await asyncio.wait({ticket}, timeout=1)
            yield sse("status", {"stage": "thinking"})
            async for token in llm.stream(build_messages(req, plan_text, final_user)):
                yield sse("token", {"t": token})
        except Exception:
            log.exception("LLM error")
            yield sse("error", {"message": "Sorry, something went wrong generating the answer."})
            return
        finally:
            queue.leave(ticket)
        yield sse("done", {"grounded": True})

    return StreamingResponse(
        events(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )
