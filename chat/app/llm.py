"""Streaming client for llama-server, with a slot-aware queue."""

import asyncio
import json
import logging
from collections.abc import AsyncIterator

import httpx

log = logging.getLogger(__name__)


class QueueFull(Exception):
    pass


class SlotQueue:
    """FIFO gate matching llama-server --parallel, so queued users see their position."""

    def __init__(self, slots: int, max_waiting: int):
        self.slots = slots
        self.max_waiting = max_waiting
        self.active = 0
        self.waiters: list[asyncio.Future] = []

    def enter(self) -> asyncio.Future:
        """Returns a future that resolves when a slot is ours."""
        fut = asyncio.get_running_loop().create_future()
        if self.active < self.slots and not self.waiters:
            self.active += 1
            fut.set_result(True)
        elif len(self.waiters) >= self.max_waiting:
            raise QueueFull()
        else:
            self.waiters.append(fut)
        return fut

    def position(self, fut: asyncio.Future) -> int:
        return self.waiters.index(fut) + 1 if fut in self.waiters else 0

    def leave(self, fut: asyncio.Future) -> None:
        """Give up a ticket, whether still waiting or already holding a slot."""
        if fut in self.waiters:
            self.waiters.remove(fut)
        elif fut.done():
            self.release()

    def release(self) -> None:
        while self.waiters:
            fut = self.waiters.pop(0)
            if not fut.done():
                fut.set_result(True)  # slot transfers directly, active unchanged
                return
        self.active -= 1


class LLMClient:
    def __init__(self, url: str, max_tokens: int, temperature: float):
        self.url = url.rstrip("/")
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.client = httpx.AsyncClient(timeout=httpx.Timeout(300, connect=10))

    async def healthy(self) -> bool:
        try:
            return (await self.client.get(f"{self.url}/health", timeout=1)).status_code == 200
        except httpx.HTTPError:
            return False

    async def stream(self, messages: list[dict]) -> AsyncIterator[str]:
        payload = {
            "messages": messages,
            "stream": True,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "top_p": 0.9,
            # llama.cpp extensions: reuse KV cache for the shared prompt prefix
            "cache_prompt": True,
            "chat_template_kwargs": {"enable_thinking": False},
        }
        async with self.client.stream(
            "POST", f"{self.url}/v1/chat/completions", json=payload
        ) as r:
            r.raise_for_status()
            async for line in r.aiter_lines():
                if not line.startswith("data: "):
                    continue
                data = line[6:].strip()
                if data == "[DONE]":
                    break
                try:
                    delta = json.loads(data)["choices"][0].get("delta", {})
                except (json.JSONDecodeError, KeyError, IndexError):
                    continue
                if delta.get("content"):
                    yield delta["content"]

    async def aclose(self) -> None:
        await self.client.aclose()
