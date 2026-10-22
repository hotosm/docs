import asyncio

import pytest

from app.llm import QueueFull, SlotQueue


async def test_slot_handover_and_positions():
    q = SlotQueue(slots=1, max_waiting=2)
    a = q.enter()
    b = q.enter()
    c = q.enter()
    assert a.done() and not b.done()
    assert q.position(b) == 1 and q.position(c) == 2
    with pytest.raises(QueueFull):
        q.enter()
    q.leave(a)
    assert b.done() and q.position(c) == 1 and q.active == 1
    q.leave(c)  # gave up while waiting
    q.leave(b)
    assert q.active == 0 and not q.waiters
    await asyncio.sleep(0)
