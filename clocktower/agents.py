"""Seats and Storytellers.

A seat receives the text of everything it saw since its last turn plus a prompt,
and returns an action dict (the JSON schema in schema.py). Claude seats, scripted
random seats (for tests) and human seats all implement the same `act`.
"""
from __future__ import annotations
import asyncio
import random
from dataclasses import dataclass, field
from typing import Callable

from .llm import Reply


@dataclass
class Request:
    kind: str                   # night | ravenkeeper | beat | nominate | defense | vote
    prompt: str
    day: int
    beat: int | None = None
    n_targets: int = 0          # night choices
    options: list = field(default_factory=list)   # legal targets / nominees
    alive: bool = True
    mode: str = ''              # beats: 'private' (whispers only) or 'public' (town square only)


@dataclass
class STRequest:
    kind: str                   # characters | setup | decisions
    fallback: Callable[[random.Random], dict]   # a complete legal answer (scripted Storyteller)


class ModelSeat:
    def __init__(self, conversation):
        self.conversation = conversation

    async def act(self, text, request: Request) -> Reply:
        return await self.conversation.send(text, {'kind': request.kind, 'day': request.day, 'beat': request.beat})


class ModelStoryteller:
    def __init__(self, conversation):
        self.conversation = conversation

    async def decide(self, text, request: STRequest) -> Reply:
        return await self.conversation.send(text, {'kind': request.kind})


LINES = ['I have info, will share soon.', 'Who wants to claim first?', 'I trust Alex for now.',
         'That claim sounds off to me.', 'Let us not rush an execution.', 'I think we should nominate today.']


class RandomSeat:
    """Plays legal random moves. For tests only."""

    def __init__(self, name, rng: random.Random, names):
        self.name, self.rng, self.names = name, rng, names

    async def act(self, text, request: Request) -> Reply:
        r, others = self.rng, [n for n in self.names if n != self.name]
        a = {'say': '', 'whispers': [], 'nominate': None, 'vote': None, 'targets': [],
             'slayer_shot': None, 'call_nominations': False}
        if request.kind in ('night', 'ravenkeeper'):
            a['targets'] = r.sample(request.options, min(request.n_targets, len(request.options)))
        elif request.kind == 'beat':
            if r.random() < 0.5: a['say'] = r.choice(LINES)
            if r.random() < 0.3: a['whispers'] = [{'to': [r.choice(others)], 'text': 'psst, what are you?'}]
            a['call_nominations'] = r.random() < 0.3
            if r.random() < 0.03: a['slayer_shot'] = r.choice(others)
        elif request.kind == 'nominate':
            if request.options and r.random() < 0.4:
                a['nominate'] = r.choice(request.options)
                a['say'] = 'You seem suspicious.'
        elif request.kind == 'defense':
            a['say'] = 'I am good, I promise.'
        elif request.kind == 'vote':
            a['vote'] = r.random() < 0.5
        return Reply(a)


class ScriptedStoryteller:
    """Makes every Storyteller choice by the policy in state.py (what an experienced human
    Storyteller would usually do, with some randomness). No API calls."""

    def __init__(self, rng: random.Random):
        self.rng = rng

    async def decide(self, text, request: STRequest) -> Reply:
        return Reply(request.fallback(self.rng))


RandomStoryteller = ScriptedStoryteller


class HumanSeat:
    """Waits for a move submitted through the web UI (see web.py)."""

    def __init__(self, name):
        self.name = name
        self.pending: Request | None = None
        self.future: asyncio.Future | None = None
        self.loop: asyncio.AbstractEventLoop | None = None

    async def act(self, text, request: Request) -> Reply:
        self.loop = asyncio.get_running_loop()
        self.future = self.loop.create_future()
        self.pending = request
        try:
            return Reply(await self.future)
        finally:
            self.pending, self.future = None, None

    def submit(self, action: dict):
        """Called from the web server thread."""
        if self.future and self.loop:
            self.loop.call_soon_threadsafe(lambda f=self.future: f.done() or f.set_result(action))
