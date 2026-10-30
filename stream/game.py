"""Load one game's logs (events.jsonl, probes.jsonl, result.json, config.json) into a convenient digest."""
import json, os, re
from pathlib import Path

from clocktower.characters import TOWNSFOLK, OUTSIDERS, MINIONS, DEMONS

REPO = Path(__file__).resolve().parent.parent
ROOTS = [Path(p) for p in [os.environ.get("CLOCKTOWER_GAMES", ""), REPO / "games", "/home/user/clocktower/games"] if p]

MODEL_NAMES = {
    "gpt-6-astra": "GPT-6 Astra", "gpt-6.1-sol": "GPT-6.1 Sol", "claude-fable-5-1": "Claude Fable 5.1",
    "gpt-5.6-sol": "GPT-5.6 Sol", "claude-fable-5": "Claude Fable 5", "claude-opus-5-5": "Claude Opus 5.5",
    "gpt-5.5": "GPT-5.5", "claude-opus-4-6": "Claude Opus 4.6", "gpt-5.4": "GPT-5.4",
    "claude-opus-4-7": "Claude Opus 4.7", "claude-opus-4-8": "Claude Opus 4.8", "claude-sonnet-5-5": "Claude Sonnet 5.5",
}
ROLE_NAMES = TOWNSFOLK + OUTSIDERS + MINIONS + DEMONS


def model_name(m):
    return MODEL_NAMES.get(m, m)


def find(rel):
    """'v16/f2-x/game-01' (or a path) -> the directory that holds its events.jsonl."""
    p = Path(rel)
    if (p / "events.jsonl").exists():
        return p
    rel = str(rel).split("games/", 1)[-1]
    for r in ROOTS:
        if (r / rel / "events.jsonl").exists():
            return r / rel
    raise FileNotFoundError(f"no events.jsonl for {rel} under {ROOTS}")


def kind_of(ch):
    if ch in TOWNSFOLK: return "Townsfolk"
    if ch in OUTSIDERS: return "Outsider"
    if ch in MINIONS: return "Minion"
    return "Demon"


class Game:
    def __init__(self, rel):
        self.dir = find(rel)
        self.rel = str(self.dir).split("games/", 1)[-1]
        jl = lambda f: [json.loads(l) for l in open(self.dir / f)] if (self.dir / f).exists() else []
        self.events = jl("events.jsonl")
        self.probes = jl("probes.jsonl")
        self.result = json.load(open(self.dir / "result.json"))
        self.config = json.load(open(self.dir / "config.json"))
        setup = next(e for e in self.events if e["kind"] == "setup")["data"]["seats"]
        self.seats = [s["name"] for s in setup]
        self.char = {s["name"]: s["character"] for s in setup}
        self.shown = {s["name"]: s.get("shown", s["character"]) for s in setup}
        self.evil = {n: self.char[n] in MINIONS + DEMONS for n in self.seats}
        self.models = self.result.get("models", {})
        self.winner = self.result["winner"]
        self.reason = self.result.get("reason", "")
        self.days = max(e["day"] for e in self.events)

    # ---- teams and models
    def team_models(self, evil):
        ms = sorted({self.models[n] for n in self.seats if self.evil[n] == evil})
        return " + ".join(model_name(m) for m in ms)

    def is_claude(self, name):
        return self.models.get(name, "").startswith("claude")

    def demon_at(self, seq):
        """Who is the Demon just after event seq (star-passes and Scarlet Woman catches move it)."""
        d = next(n for n in self.seats if self.char[n] == "Imp")
        for e in self.events:
            if e["seq"] > seq: break
            if e["kind"] == "becomes" and e["data"].get("character") == "Imp":
                d = e["data"]["player"]
        return d

    def role_label(self, n):
        c = self.char[n]
        if c == "Drunk": return f"Drunk (thinks {self.shown[n]})"
        return c

    # ---- probes: the village's average P(Demon) for each seat, at each probe point
    def suspicion(self):
        """[(day, point, {seat: avg P(demon) over living good players other than the seat})]."""
        out = {}
        for r in self.probes:
            if r.get("team") != "good" or not r.get("alive") or not r.get("players"): continue
            key = (r["day"], r["point"])
            for n, v in r["players"].items():
                if n == r["player"] or n not in self.char: continue
                try: x = float(v.get("demon"))
                except (TypeError, ValueError): continue
                out.setdefault(key, {}).setdefault(n, []).append(x / 100 if x > 1 else x)
        return [(d, p, {n: sum(v) / len(v) for n, v in m.items()})
                for (d, p), m in sorted(out.items(), key=lambda kv: (kv[0][0], kv[0][1] != "dawn"))]


CLAIM_RE = re.compile(r"\bI(?:'m| am|’m)\s+(?:actually\s+|really\s+|the\s+real\s+|truly\s+)?(?:the\s+|a\s+|an\s+|your\s+)?("
                      + "|".join(sorted(ROLE_NAMES, key=len, reverse=True)) + r")\b", re.I)


def claims_in(text):
    return [next(r for r in ROLE_NAMES if r.lower() == m.group(1).lower()) for m in CLAIM_RE.finditer(text)]
