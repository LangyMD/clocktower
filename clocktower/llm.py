"""Model conversations for players and the Storyteller (Claude and OpenAI).

Each seat is one append-only conversation: a frozen system prompt (shared by all
seats, so it caches across them), then alternating user turns (what happened since
the seat last acted, plus the current prompt) and the model's full replies,
including its reasoning. Nothing earlier is ever edited or re-sent in a different
form, so the model keeps its own reasoning across the whole game and every request
reads everything before the new turn from cache.

Every model gets the same per-turn output ceiling (`max_tokens`, thinking included).
A truncated turn is retried once at the same ceiling rather than given more room.
"""
from __future__ import annotations
import asyncio
import json
import os
import random
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path

import anthropic

MODEL = 'claude-opus-5-5'


def _price(inp, out, read=None, write_5m=None, write_1h=None):
    """USD per million tokens. Claude cache writes are 1.25x (5 min) / 2x (1 hour) input, reads 0.1x."""
    return {'input': inp, 'read': read if read is not None else inp / 10, 'output': out,
            'write_5m': write_5m if write_5m is not None else inp * 1.25,
            'write_1h': write_1h if write_1h is not None else inp * 2}


PRICES = {
    'claude-opus-5-5': _price(4, 20, read=0.20),
    'claude-opus-5': _price(5, 25),
    'claude-fable-5-1': _price(10, 50, read=0.25),
    'claude-sonnet-5': _price(2, 10),
    'claude-haiku-4-5': _price(1, 5),
    # OpenAI list prices as recorded by the earlier lab (botc/costs.py); Flex is half price.
    'gpt-6-astra': _price(10, 50, read=1, write_5m=12.5, write_1h=12.5),
    'gpt-5.6-sol': _price(4, 20, read=0.4, write_5m=5, write_1h=5),
}


def cost(model, usage, factor=1.0):
    """`usage` is the normalised dict every conversation records (Anthropic field names)."""
    p = PRICES[model]
    w1h = usage.get('cache_creation', {}).get('ephemeral_1h_input_tokens', 0)
    w5m = usage.get('cache_creation_input_tokens', 0) - w1h
    return factor * (p['input'] * usage.get('input_tokens', 0) + p['write_5m'] * w5m + p['write_1h'] * w1h
                     + p['read'] * usage.get('cache_read_input_tokens', 0)
                     + p['output'] * usage.get('output_tokens', 0)) / 1e6


class BudgetExceeded(RuntimeError):
    pass


class Ledger:
    """Append-only record of API spend, shared by every game that points at it."""

    def __init__(self, path, cap=None):
        self.path, self.cap = Path(path), cap
        self.spent = 0.0
        if self.path.exists():
            self.spent = sum(json.loads(line)['cost'] for line in self.path.read_text().splitlines() if line.strip())

    def check(self):
        if self.cap is not None and self.spent >= self.cap:
            raise BudgetExceeded(f'spend ${self.spent:.2f} has reached the cap ${self.cap:.2f}')

    def add(self, amount, **meta):
        self.spent += amount
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open('a') as f:
            f.write(json.dumps({'time': time.time(), 'cost': amount, **meta}) + '\n')


def make_client():
    headers = {}
    workspace = os.environ.get('ANTHROPIC_WORKSPACE_ID')
    if workspace:
        headers['anthropic-workspace-id'] = workspace
    # Claude Code on the web keeps ANTHROPIC_API_KEY for itself, so the key can live under another name
    key = os.environ.get('ANTHROPIC_API_KEY') or os.environ.get('MY_ANTHROPIC_API_KEY')
    return anthropic.AsyncAnthropic(api_key=key, default_headers=headers, max_retries=8, timeout=900)


@dataclass
class Reply:
    action: dict
    thinking: str = ''


class _Base:
    def __init__(self, system, schema, *, label, ledger, semaphore, on_call=None, model=MODEL, effort='high',
                 max_tokens=16000):
        self.system, self.schema = system, schema
        self.label, self.ledger, self.semaphore, self.on_call = label, ledger, semaphore, on_call
        self.model, self.effort, self.max_tokens = model, effort, max_tokens
        self.messages = []

    def record(self, meta, attempt, stop, start, spent, usage, thinking, out, extra=None):
        if self.on_call:
            self.on_call({'label': self.label, **(meta or {}), 'model': self.model, 'attempt': attempt, 'stop': stop,
                          'latency': round(time.monotonic() - start, 2), 'cost': spent, 'usage': usage,
                          'thinking': thinking, 'output': out, **(extra or {})})


class ClaudeConversation(_Base):
    def __init__(self, client, system, schema, *, ttl='5m', **kw):
        super().__init__(system, schema, **kw)
        self.client = client
        self.cache = {'type': 'ephemeral', 'ttl': ttl}

    async def send(self, text, meta=None, commit=True) -> Reply:
        """One turn. With commit=False (a probe) the turn is a fork: neither the question nor
        the reply is added to the conversation."""
        user = {'role': 'user', 'content': text}
        if commit:
            self.messages.append(user)
        messages = self.messages if commit else [*self.messages, user]
        refusals = truncations = 0
        for attempt in range(4):
            self.ledger.check()
            start = time.monotonic()
            async with self.semaphore:
                async with self.client.messages.stream(
                        model=self.model, max_tokens=self.max_tokens,
                        system=[{'type': 'text', 'text': self.system, 'cache_control': self.cache}],
                        messages=messages, cache_control=self.cache,
                        thinking={'type': 'adaptive', 'display': 'summarized'},
                        output_config={'effort': self.effort,
                                       'format': {'type': 'json_schema', 'schema': self.schema}}) as stream:
                    r = await stream.get_final_message()
            usage = r.usage.model_dump(exclude_none=True)
            spent = cost(self.model, usage)
            self.ledger.add(spent, label=self.label)
            thinking = '\n'.join(b.thinking for b in r.content if b.type == 'thinking' and b.thinking)
            out = ''.join(b.text for b in r.content if b.type == 'text')
            refusal = r.stop_details.model_dump() if getattr(r, 'stop_details', None) else None
            self.record(meta, attempt, r.stop_reason, start, spent, usage, thinking, out, {'refusal': refusal})
            if r.stop_reason == 'refusal':
                refusals += 1
                if refusals >= 2:
                    return Reply({}, thinking)
                continue
            if r.stop_reason == 'max_tokens':
                truncations += 1
                if truncations >= 2:
                    return Reply({}, thinking)
                continue
            try:
                action = json.loads(out)
            except json.JSONDecodeError:
                continue
            if commit:
                self.messages.append({'role': 'assistant', 'content': [b.model_dump(exclude_none=True) for b in r.content]})
            return Reply(action, thinking)
        return Reply({})


class OpenAIConversation(_Base):
    """OpenAI Responses API with stateless (store=false) reasoning continuity: every output
    item, including encrypted reasoning, is appended to the input for the next turn."""
    URL = 'https://api.openai.com/v1/responses'

    def __init__(self, system, schema, *, flex=True, **kw):
        super().__init__(system, schema, **kw)
        self.flex = flex
        self.key = os.environ.get('OPENAI_API_KEY')
        if not self.key:
            raise RuntimeError('OPENAI_API_KEY is not set')
        self.messages = [{'role': 'developer', 'content': [self._block(system)]}]

    @staticmethod
    def _block(text):
        return {'type': 'input_text', 'text': text, 'prompt_cache_breakpoint': {'mode': 'explicit'}}

    def _post(self, body):
        req = urllib.request.Request(self.URL, data=json.dumps(body).encode(), method='POST',
                                     headers={'Authorization': f'Bearer {self.key}', 'Content-Type': 'application/json'})
        with urllib.request.urlopen(req, timeout=900 if self.flex else 300) as resp:
            return json.load(resp)

    async def _request(self, body):
        for attempt in range(10):
            try:
                return await asyncio.to_thread(self._post, body)
            except urllib.error.HTTPError as e:
                detail = e.read().decode(errors='replace')[:2000]
                if e.code not in (408, 409, 429, 500, 502, 503, 504) or attempt == 9 or 'insufficient_quota' in detail:
                    raise RuntimeError(f'OpenAI HTTP {e.code}: {detail}') from e
            except (TimeoutError, urllib.error.URLError) as e:
                if attempt == 9:
                    raise RuntimeError(f'OpenAI transport error: {e}') from e
            await asyncio.sleep(min(2 ** attempt, 60) + random.random())

    async def send(self, text, meta=None, commit=True) -> Reply:
        user = {'role': 'user', 'content': [self._block(text)]}
        if commit:
            self.messages.append(user)
        messages = self.messages if commit else [*self.messages, user]
        truncations = 0
        for attempt in range(4):
            self.ledger.check()
            body = {'model': self.model, 'store': False, 'max_output_tokens': self.max_tokens, 'input': messages,
                    'text': {'format': {'type': 'json_schema', 'name': 'game_action', 'strict': True,
                                        'schema': self.schema}},
                    'reasoning': {'effort': self.effort, 'summary': 'auto', 'context': 'all_turns'},
                    'prompt_cache_key': f'clocktower:{self.label}:{id(self) % 10 ** 8}',
                    'prompt_cache_options': {'mode': 'explicit', 'ttl': '30m'}}
            if self.flex:
                body['service_tier'] = 'flex'
            start = time.monotonic()
            async with self.semaphore:
                raw = await self._request(body)
            u = raw.get('usage') or {}
            d = u.get('input_tokens_details') or {}
            read, write = d.get('cached_tokens', 0), d.get('cache_write_tokens', 0)
            usage = {'input_tokens': u.get('input_tokens', 0) - read - write, 'cache_read_input_tokens': read,
                     'cache_creation_input_tokens': write, 'output_tokens': u.get('output_tokens', 0),
                     'output_tokens_details': {'thinking_tokens': (u.get('output_tokens_details') or {}).get('reasoning_tokens', 0)}}
            priced = usage
            if u.get('input_tokens', 0) > 272_000:  # long-context pricing: input x2, output x1.5
                priced = {k: v * 2 for k, v in usage.items() if k.endswith('input_tokens')}
                priced['output_tokens'] = usage['output_tokens'] * 1.5
            spent = cost(self.model, priced, 0.5 if raw.get('service_tier') == 'flex' else 1.0)
            self.ledger.add(spent, label=self.label)
            output = raw.get('output') or []
            thinking = '\n'.join(s.get('text', '') for item in output if item.get('type') == 'reasoning'
                                 for s in item.get('summary') or [])
            parts = [c for item in output if item.get('type') == 'message' for c in item.get('content') or []]
            out = ''.join(c.get('text', '') for c in parts if c.get('type') == 'output_text')
            refused = any(c.get('type') == 'refusal' for c in parts)
            stop = 'refusal' if refused else raw.get('status')
            if (raw.get('incomplete_details') or {}).get('reason') == 'max_output_tokens':
                stop = 'max_tokens'
            self.record(meta, attempt, stop, start, spent, usage, thinking, out)
            if stop == 'max_tokens':
                truncations += 1
                if truncations >= 2:
                    return Reply({}, thinking)
                continue
            if stop != 'completed':
                continue
            try:
                action = json.loads(out)
            except json.JSONDecodeError:
                continue
            if commit:
                self.messages.extend(output)
            return Reply(action, thinking)
        return Reply({})


def conversation(client, system, schema, *, model, **kw):
    """A Claude or OpenAI conversation, by model name."""
    if model.startswith('gpt-'):
        kw.pop('ttl', None)
        return OpenAIConversation(system, schema, model=model, **kw)
    kw.pop('flex', None)
    return ClaudeConversation(client, system, schema, model=model, **kw)
