"""One game -> an episode script: an ordered list of steps (spoken clips plus the visual events tied to them).

Everything here is deterministic and drawn from the logs: which moments to show (scored by simple rules),
the quoted excerpts (verbatim sentences, trimmed at sentence boundaries), and the narration (templates filled
from events). Only the curated highlight episodes add a hand-written hook (highlights.py).

A step is {"clip": {...} or None, "hold": seconds of silence after, "ev": [events at clip start],
"ev_end": [events at clip end]}. A clip is {"who": "N" (narrator) or a seat name, "text": spoken text,
"show": displayed text}. Visual events are dicts with a "k" kind; render.py folds them into the frame state.
"""
import re

from .game import Game, claims_in, kind_of
from . import highlights

GLOSS = {
    "Imp": "the Demon, who kills one player each night",
    "Poisoner": "who poisons one player each night, so their information goes wrong",
    "Spy": "who secretly sees every player's true character",
    "Scarlet Woman": "who becomes the new Demon if the Demon dies",
    "Baron": "whose presence adds two extra Outsiders to the game",
}
GOOD_GLOSS = {
    "Saint": "if the village executes the Saint, good loses on the spot",
    "Mayor": "if only three players are left and nobody is executed, good wins",
    "Slayer": "who gets one public shot per game: if it hits the Demon, the Demon dies",
    "Virgin": "the first Townsfolk to nominate the Virgin is executed on the spot",
    "Drunk": None,
}
KEYWORDS = re.compile(r"\b(kill|kills|killed|poison\w*|bluff\w*|frame\w*|claim\w*|tonight|star-?pass\w*|sacrific\w*|"
                      r"deal|Saint|Mayor|execut\w*|nominat\w*|Demon|Imp|Minion|lie|lying|liar|trust|vote|votes|"
                      r"Scarlet Woman|Spy|Baron|Poisoner|Slayer|Virgin|Undertaker|Ravenkeeper|Empath|Fortune Teller|"
                      r"Investigator|Washerwoman|Librarian|Chef|Drunk|Recluse|Soldier|Monk|Butler|evil|cover|plan)\b", re.I)
SUSPECT = re.compile(r"\b(suspicious|sus|evil|Demon|Imp|lying|liar|execute|scum|wolf)\b", re.I)
NUM = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve",
       "thirteen", "fourteen", "fifteen"]


def num(n):
    return NUM[n] if 0 <= n < len(NUM) else str(n)


# ---------------------------------------------------------------- text helpers
def clean(t):
    t = re.sub(r"\*\*?|__|`|#+ ", "", t)
    t = re.sub(r"\s*\n+\s*", " ", t)
    return re.sub(r"\s{2,}", " ", t).strip()


def sentences(t):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+(?=[A-Z\"'(“])", clean(t)) if s.strip()]


def words(s):
    return len(s.split())


def excerpt(text, maxw=34, prefer=None):
    """Best window of consecutive whole sentences (<= maxw words), scored by game keywords and `prefer`."""
    ss = sentences(text)
    if not ss: return ""
    best, bs = None, -1e9
    for i in range(len(ss)):
        w, acc = 0, []
        for j in range(i, len(ss)):
            w += words(ss[j])
            if w > maxw and acc: break
            acc.append(ss[j])
            s = " ".join(acc)
            sc = len(KEYWORDS.findall(s)) + (50 if prefer and re.search(prefer, s, re.I) else 0) - 0.15 * i + 0.02 * words(s)
            if sc > bs: best, bs = s, sc
    if words(best) > maxw:                       # one long sentence: cut at a comma or at maxw words
        ws = best.split()
        cut = maxw
        for k in range(maxw, maxw // 2, -1):
            if ws[k - 1].endswith((",", ";", ":")): cut = k; break
        best = " ".join(ws[:cut]).rstrip(",;:") + "…"
    return best


TTS_SUBS = [(r"\bN(\d)\b", lambda m: "night " + num(int(m.group(1)))), (r"\bD(\d)\b", lambda m: "day " + num(int(m.group(1)))),
            (r"\bSW\b", "Scarlet Woman"), (r"\bFT\b", "Fortune Teller"), (r"\bWW\b", "Washerwoman"),
            (r"\bRK\b", "Ravenkeeper"), (r"\bUT\b", "Undertaker"), (r"\bST\b", "Storyteller"), (r"\bw/", "with "),
            (r"\s*->\s*", ", then "), (r"\s*→\s*", ", then "), (r"\s&\s", " and "), (r"\b(\d+)/(\d+)\b", r"\1 of \2"),
            (r"\+", " and "), (r"…$", "."), (r"\s+-\s+", ", "), (r"\s+—\s+", ", ")]


def tts_text(s):
    for a, b in TTS_SUBS:
        s = re.sub(a, b, s)
    return re.sub(r"\s{2,}", " ", s).strip()


def claim_re(c):
    return r"\bI(?:'m| am|’m)\s+(?:actually\s+|really\s+|the\s+real\s+|the\s+|a\s+|an\s+)*" + re.escape(c)


def first_claim(text):
    """The first 'I'm the X' in a text, ignoring hypotheticals ('if I'm the Saint')."""
    t = clean(text)
    for m in re.finditer(r"\bI(?:'m| am|’m)\b", t):
        if re.search(r"\b(if|If|unless|whether|were|not|way|that|say|says|said)\s*$", t[max(0, m.start() - 9):m.start()]): continue
        if re.match(r"\s+not\b", t[m.end():]): continue
        c = claims_in(t[m.start():m.start() + 60])
        if c and c[0] != "Imp":
            tail = t[m.start():m.start() + 60]
            k = tail.lower().find(c[0].lower()) + len(c[0])
            if re.match(r"[\s,]*(only\s+)?(if|unless|when)\b", tail[k:], re.I): continue
            return c[0]
    return None


# ---------------------------------------------------------------- the episode
class Builder:
    def __init__(self, rel):
        self.g = Game(rel)
        self.steps = []
        self.used = set()        # seqs already quoted
        self.shown_texts = set()
        self.hl = highlights.get(self.g.rel)
        self.pins, self.pin_text = set(), {}
        for sub in (self.hl or {}).get("pins", []):
            hits = [e for e in self.g.events if e["kind"] in ("say", "whisper", "thinking", "nomination", "defense")
                    and sub in clean(e["data"].get("text", ""))]
            assert hits, f"pin not found: {sub}"
            self.pins.add(hits[0]["seq"]); self.pin_text[hits[0]["seq"]] = sub

    def pin_re(self, e):
        s = self.pin_text.get(e["seq"])
        return re.escape(s) if s else None

    # step helpers
    def say(self, text, ev=(), ev_end=(), hold=0.25, caption=None):
        self.steps.append({"clip": {"who": "N", "text": text, "show": caption or text}, "hold": hold, "ev": list(ev), "ev_end": list(ev_end)})

    def quote(self, who, shown, ev=(), ev_end=(), hold=0.45):
        self.shown_texts.add(shown[:60])
        self.steps.append({"clip": {"who": who, "text": tts_text(shown), "show": shown}, "hold": hold, "ev": list(ev), "ev_end": list(ev_end)})

    def pause(self, secs, ev=()):
        self.steps.append({"clip": None, "hold": secs, "ev": list(ev), "ev_end": []})

    def role(self, n):
        return self.g.role_label(n)

    def build(self):
        g = self.g
        self.intro()
        evs = g.events
        days = sorted({e["day"] for e in evs if e["day"] >= 1})
        susp = {(d, p): m for d, p, m in g.suspicion()}
        self.claimed = {}; self.label_claims = {}
        for d in days:
            de = [e for e in evs if e["day"] == d]
            self.night(d, de)
            if any(e["kind"] == "game_over" for e in de if e["phase"] == "night"):
                break
            self.dawn(d, de, susp.get((d, "dawn")))
            self.private(d, de)
            self.square(d, de)
            self.nominations(d, de, susp.get((d, "nominations")))
            if any(e["kind"] == "game_over" for e in de): break
        self.ending(susp)
        return self.steps

    # ------------------------------------------------------------ intro
    def intro(self):
        g = self.g; n = len(g.seats)
        demon = next(s for s in g.seats if g.char[s] == "Imp")
        minions = [s for s in g.seats if kind_of(g.char[s]) == "Minion"]
        title = self.hl["title"] if self.hl else f"{g.team_models(True)} vs {g.team_models(False)}"
        ring = {"k": "ring", "seats": [{"name": s, "role": g.role_label(s), "evil": g.evil[s], "demon": s == demon} for s in g.seats]}
        card = {"k": "title", "title": title, "evil": g.team_models(True), "good": g.team_models(False),
                "sub": f"{n} players · Trouble Brewing · {g.rel}", "highlight": bool(self.hl)}
        self.pause(0.6, [ring, card, {"k": "phase", "text": "Setup", "night": True}])
        if self.hl:
            for line in self.hl["hook"]:
                self.say(line, hold=0.35)
        self.say(f"{num(n).capitalize()} players. The village is played by {g.team_models(False)}. "
                 f"The evil team is {g.team_models(True)}.", ev=[{"k": "untitle"}], hold=0.4)
        self.say(f"The Demon is {demon}, the Imp, who kills one player each night.",
                 ev=[{"k": "panel", "type": "roles", "focus": [demon]}, {"k": "hl", "names": [demon]}])
        for m in minions:
            self.say(f"{m} is the {g.char[m]}, {GLOSS[g.char[m]]}.", ev=[{"k": "hl", "names": [m]}, {"k": "panel", "type": "roles", "focus": [demon] + minions[:minions.index(m) + 1]}])
        for s in g.seats:
            c = g.char[s]
            if c == "Drunk":
                self.say(f"{s} is the Drunk: {s} believes they are the {g.shown[s]}, but their information is false.", ev=[{"k": "hl", "names": [s]}])
            elif c in ("Saint", "Mayor"):
                self.say(f"{s} is the {c}: {GOOD_GLOSS[c]}.", ev=[{"k": "hl", "names": [s]}])
        self.say("We can see every secret. The village can't. The amber ring around each player shows how strongly "
                 "the village suspects them of being the Demon.", ev=[{"k": "hl", "names": []}, {"k": "panel", "type": "legend"}], hold=0.6)

    # ------------------------------------------------------------ night
    def night(self, d, de):
        g = self.g
        ne = [e for e in de if e["phase"] == "night"]
        choices = {e["data"]["role"]: e["data"] for e in ne if e["kind"] == "night_choice"}
        pois = choices.get("Poisoner", {}).get("targets", [None])[0] if "Poisoner" in choices else None
        lines = []
        if pois:
            lines.append({"t": f"{choices['Poisoner']['player']} (Poisoner) poisons {pois}", "c": "poison"})
        imp = choices.get("Imp")
        dawn = next((e for e in de if e["kind"] == "dawn"), None)
        deaths = dawn["data"]["deaths"] if dawn else []
        becomes = [e["data"] for e in ne if e["kind"] == "becomes"]
        if imp and imp.get("targets"):
            t = imp["targets"][0]
            lines.append({"t": f"{imp['player']} (Imp) {'kills themself' if t == imp['player'] else 'attacks ' + t}", "c": "evil"})
        monk = choices.get("Monk")
        if monk and monk.get("targets"):
            lines.append({"t": f"{monk['player']} (Monk) protects {monk['targets'][0]}", "c": "good"})
        for e in ne:
            if e["kind"] != "info" or not isinstance(e["to"], list): continue
            who = e["to"][0]
            txt = re.sub(r"^Night \d+ — ", "", e["data"]["text"])
            txt = re.sub(r"You learn that |You learn ", "", txt).replace("You chose", "chose")
            role, _, rest = txt.partition(": ")
            bad = " · poisoned" if who == pois else (" · Drunk: false" if g.char[who] == "Drunk" else "")
            lines.append({"t": f"{who} ({role}): {rest[:1].lower() + rest[1:] if rest[:1].isupper() and not rest.startswith(tuple(g.seats)) else rest}", "c": "info", "bad": bool(bad), "tag": bad.strip(" ·")})
        links = []
        if pois: links.append({"from": choices["Poisoner"]["player"], "to": [pois], "style": "poison"})
        if imp and imp.get("targets") and imp["targets"][0] != imp["player"]:
            links.append({"from": imp["player"], "to": [imp["targets"][0]], "style": "kill"})
        ev = [{"k": "phase", "text": f"Night {d}", "night": True}, {"k": "panel", "type": "night", "title": f"Night {d}", "lines": lines},
              {"k": "links", "items": links}, {"k": "hl", "names": []}, {"k": "clearvotes"}]
        parts = [f"Night {num(d)}."]
        if pois:
            pp = choices["Poisoner"]["player"]
            parts.append(f"The Poisoner, {pp}, poisons {pois}" + (f", the {self.role(pois)}." if not g.evil[pois] else "."))
        if imp and imp.get("targets"):
            t = imp["targets"][0]; ip = imp["player"]
            if t == ip:
                nb = becomes[0]["player"] if becomes else None
                parts.append(f"The Imp, {ip}, kills themself on purpose." + (f" The Demon passes to {nb}, the {g.char[nb]}." if nb else ""))
            elif t in deaths:
                parts.append(f"The Imp, {ip}, kills {t}" + ("." if g.evil[t] else f", the {self.role(t)}."))
            else:
                why = ""
                if monk and monk.get("targets") == [t] and monk["player"] != pois: why = f" The Monk, {monk['player']}, was protecting them."
                elif g.char[t] == "Soldier" and t != pois: why = " The Soldier can't be killed by the Demon."
                parts.append(f"The Imp, {ip}, attacks {t}, but {t} survives." + why)
                others = [x for x in deaths if x != t]
                if others: parts.append(f"{others[0]} dies instead.")
        bad_info = [ln for ln in lines if ln.get("bad")]
        if d == 1:
            parts.append("Players with information roles get their first clues.")
        if bad_info and len(parts) < 4:
            who = bad_info[0]["t"].split(" ")[0]
            parts.append(f"{who}'s clue tonight is false." if g.char[who] == "Drunk" or who == pois else "")
        night_dead = [{"k": "dead", "name": e["data"]["player"], "how": f"killed night {d}"} for e in ne if e["kind"] == "death"]
        self.say(" ".join(p for p in parts if p), ev=ev, ev_end=night_dead, hold=0.6)
        for b in becomes:
            if not (imp and imp.get("targets") and imp["targets"][0] == imp["player"]):
                self.say(f"{b['player']} becomes the new Imp.", ev=[{"k": "role", "name": b["player"], "role": "Imp", "demon": True}])
            else:
                self.steps[-1]["ev_end"].append({"k": "role", "name": b["player"], "role": f"Imp (was {g.char[b['player']]})", "demon": True})

    # ------------------------------------------------------------ dawn
    def dawn(self, d, de, sus):
        dawn = next((e for e in de if e["kind"] == "dawn"), None)
        if not dawn: return
        deaths = dawn["data"]["deaths"]
        ev = [{"k": "phase", "text": f"Day {d}", "night": False}, {"k": "links", "items": []}]
        ev.append({"k": "panel", "type": "dawn", "title": f"Day {d}", "text": dawn["data"].get("narration", ""), "deaths": deaths})
        if sus: ev.append({"k": "susp", "values": sus})
        if not deaths:
            txt = f"Day {num(d)}. " + ("Everyone is alive." if d == 1 else "Nobody died in the night.")
        else:
            txt = f"Day {num(d)}. " + " and ".join(deaths) + (" is" if len(deaths) == 1 else " are") + " found dead."
        self.say(txt, ev=ev, hold=0.5)

    # ------------------------------------------------------------ private whispers & thinking
    def private(self, d, de):
        g = self.g
        beat = 0; cands = []
        for e in de:
            if e["kind"] == "header" and "private time" in e["data"]["text"]:
                beat = int(e["data"]["text"].rsplit(" ", 1)[1])
            if e["kind"] == "whisper" and e["phase"] == "day":
                w = e["data"]; frm, to = w["from"], w["to"]
                n = words(clean(w["text"]))
                if n < 8: continue
                team_chat = g.evil[frm] and all(g.evil[t] for t in to)
                lie = g.evil[frm] and not any(g.evil[t] for t in to) and first_claim(w["text"])
                sc = min(len(KEYWORDS.findall(w["text"])), 6) + (4 if team_chat else 0) + (2 if lie else 0)
                sc -= 3 if (d == 1 and beat == 1) else 0
                sc -= 0.02 * max(0, n - 60)
                kind = "team" if team_chat else ("lie" if lie else ("evil" if g.evil[frm] else "good"))
                cands.append((sc + (100 if e["seq"] in self.pins else 0), e, kind))
            if e["kind"] == "thinking" and e["data"].get("kind") in ("beat", "night", "nominate", "comment") and e["phase"] == "day":
                p = e["data"]["player"]
                if not g.is_claude(p): continue
                t = clean(e["data"]["text"])
                if words(t) < 12: continue
                sc = min(len(KEYWORDS.findall(t)), 6) + (3 if g.evil[p] else 0) + 1
                demon = g.demon_at(e["seq"])
                if not g.evil[p] and re.search(r"\b" + demon + r"\b", t) and SUSPECT.search(t): sc += 3
                cands.append((sc + (100 if e["seq"] in self.pins else 0), e, "think"))
        cands.sort(key=lambda c: (-c[0], c[1]["seq"]))
        quota = 4 if g.days <= 3 else (3 if g.days <= 5 else 2)
        quota += sum(1 for c in cands if c[1]["seq"] in self.pins)
        picks, speakers = [], set()
        cap = {"team": 2, "lie": 1, "evil": 1, "good": 1, "think_evil": 1, "think_good": 1}
        for sc, e, kind in cands:
            who = e["data"].get("from") or e["data"].get("player")
            slot = kind if kind != "think" else ("think_evil" if g.evil[who] else "think_good")
            if e["seq"] in self.pins:
                picks.append((e, kind)); speakers.add(who); cap[slot] -= 1; continue
            if who in speakers or cap[slot] <= 0: continue
            picks.append((e, kind)); speakers.add(who); cap[slot] -= 1
            if len(picks) >= quota: break
        if not picks: return
        picks.sort(key=lambda p: p[0]["seq"])
        intro = ["Private whispers.", "Then, the whispers.", "Before the town meets, private conversations."][d % 3]
        self.say(intro, ev=[{"k": "phase", "text": f"Day {d} · whispers", "night": False},
                            {"k": "panel", "type": "section", "title": f"Day {d} · private whispers",
                             "sub": "One conversation at a time. Only the people in it hear what is said."}], hold=0.3)
        for e, kind in picks:
            self.used.add(e["seq"])
            if kind == "think":
                p = e["data"]["player"]
                ex = excerpt(e["data"]["text"], 34, prefer=self.pin_re(e))
                side = "evil" if g.evil[p] else "good"
                lead = f"{p}'s private thoughts." if g.evil[p] else f"{p}, the {self.dead_word(p, e)}{self.role(p)}, thinks to themself."
                self.say(lead, ev=[{"k": "hl", "names": [p]}, {"k": "links", "items": []}], hold=0.15)
                self.quote(p, ex, ev=[{"k": "panel", "type": "think", "who": p, "role": self.rolec(p, e), "side": side, "text": ex}])
            else:
                w = e["data"]; frm, to = w["from"], w["to"]
                lie_c = first_claim(w["text"])
                ex = excerpt(w["text"], 34, prefer=self.pin_re(e) or (claim_re(lie_c) if kind == "lie" else None))
                lead = {"team": f"{frm} whispers to {self.join(to)}, in secret." if d > 1 or kind != "team" else f"The evil team meets in private. {frm}:",
                        "lie": f"{frm}, secretly the {self.cur(frm, e)}, whispers to {self.join(to)}.",
                        "evil": f"{frm} whispers to {self.join(to)}.",
                        "good": f"{frm}, the {self.dead_word(frm, e)}{self.role(frm)}, whispers to {self.join(to)}."}[kind]
                if kind == "team" and len(to) >= 2 and d == 1:
                    lead = f"The evil team meets in private. {frm}:"
                self.say(lead, ev=[{"k": "hl", "names": [frm]}, {"k": "links", "items": [{"from": frm, "to": to, "style": "whisper"}]}], hold=0.15)
                self.quote(frm, ex, ev=[{"k": "panel", "type": "whisper", "who": frm, "to": to, "role": self.rolec(frm, e),
                                         "side": "evil" if g.evil[frm] else "good", "secret": kind == "team", "text": ex}])
        self.steps[-1]["ev_end"].append({"k": "links", "items": []})

    def claim_events(self, evs):
        out = []
        for e in evs:
            if e["kind"] not in ("say", "nomination", "defense"): continue
            p = e["data"].get("speaker") or (e["data"]["nominator"] if e["kind"] == "nomination" else e["data"].get("nominee"))
            c = first_claim(e["data"]["text"])
            if p and c and self.label_claims.get(p) != c:
                self.label_claims[p] = c
                out.append({"k": "claim", "name": p, "role": c, "lie": c not in (self.g.shown[p], self.g.char[p])})
        return out

    def join(self, names):
        return names[0] if len(names) == 1 else ", ".join(names[:-1]) + " and " + names[-1]

    # ------------------------------------------------------------ town square
    def square(self, d, de):
        g = self.g
        cands = []
        in_square = False
        for e in de:
            if e["kind"] == "header": in_square = "town square" in e["data"]["text"]
            if e["kind"] != "say" or not in_square: continue
            p = e["data"]["speaker"]; t = e["data"]["text"]
            if words(clean(t)) < 10: continue
            c = first_claim(t)
            new_claim = c and self.claimed.get(p) != c
            truth = g.shown[p]
            lie = c and c != truth and c != g.char[p]
            sc = min(len(KEYWORDS.findall(t)), 6) + (3 if new_claim else 0) + (3 if lie and new_claim else 0)
            sc += 1 if g.evil[p] else 0
            cands.append((sc + (100 if e["seq"] in self.pins else 0), e, c if new_claim else None, lie))
        cands.sort(key=lambda c: (-c[0], c[1]["seq"]))
        quota = 4 if g.days <= 5 else 3
        quota += sum(1 for c in cands if c[1]["seq"] in self.pins)
        picks, speakers = [], set()
        for sc, e, c, lie in cands:
            p = e["data"]["speaker"]
            if p in speakers and e["seq"] not in self.pins: continue
            picks.append((e, c, lie)); speakers.add(p)
            if len(picks) >= quota: break
        sq = [e for e in de if e["phase"] == "day" and e["kind"] == "say"]
        if not picks:
            ce = self.claim_events(sq)
            if ce: self.pause(0.1, ce)
            return
        picks.sort(key=lambda p: p[0]["seq"])
        self.steps.append({"clip": None, "hold": 0, "ev": self.claim_events(sq), "ev_end": []})
        self.say(["In the town square, everyone hears.", "The town square.", "Now, in public."][d % 3],
                 ev=[{"k": "phase", "text": f"Day {d} · town square", "night": False}, {"k": "links", "items": []},
                     {"k": "panel", "type": "section", "title": f"Day {d} · town square",
                      "sub": "Everyone hears what is said here. Nobody can prove who they are."}], hold=0.3)
        for e, c, lie in picks:
            p = e["data"]["speaker"]; self.used.add(e["seq"])
            ex = excerpt(e["data"]["text"], 36, prefer=self.pin_re(e) or (claim_re(c) if c else None))
            if c and not re.search(claim_re(c), ex, re.I): c = None
            ev = [{"k": "hl", "names": [p]}]
            if c:
                self.claimed[p] = c
                cl = {"k": "claim", "name": p, "role": c, "lie": bool(lie)}
                if lie and g.evil[p]:
                    self.say(f"{p}, secretly the {self.cur(p, e)}, claims to be the {c}.", ev=ev + [cl], hold=0.15)
                elif lie:
                    self.say(f"{p}, really the {self.role(p)}, claims to be the {c}.", ev=ev + [cl], hold=0.15)
                elif g.char[p] == "Drunk":
                    self.say(f"{p} claims {c}, not knowing they are the Drunk.", ev=ev + [cl], hold=0.15)
                elif self.dead_word(p, e):
                    self.say(f"{p}, the dead {c}, speaks from the grave.", ev=ev + [cl], hold=0.15)
                else:
                    self.say(f"{p}, the real {c}, goes public.", ev=ev + [cl], hold=0.15)
            else:
                self.say(f"{p}" + (f", the {self.dead_word(p, e)}{self.role(p)}:" if not g.evil[p] else f", secretly the {self.cur(p, e)}:"), ev=ev, hold=0.1)
            self.quote(p, ex, ev=[{"k": "panel", "type": "say", "who": p, "role": self.rolec(p, e), "side": "evil" if g.evil[p] else "good", "text": ex}])

    # ------------------------------------------------------------ nominations
    def nominations(self, d, de, sus):
        g = self.g
        ne = [e for e in de if e["phase"] == "nominations"]
        if not ne: return
        ev = [{"k": "phase", "text": f"Day {d} · nominations", "night": False}, {"k": "links", "items": []}, {"k": "hl", "names": []}]
        line = "Nominations."
        ev.append({"k": "panel", "type": "section", "title": f"Day {d} · nominations",
                   "sub": "Any living player may nominate. Enough votes put the nominee on the block; whoever is on the block at the end of the day is executed."})
        if sus:
            ev.append({"k": "susp", "values": sus})
            alive = [s for s in g.seats if s not in self.dead_before(ne[0]["seq"])]
            top = max(alive, key=lambda s: sus.get(s, 0))
            demon = g.demon_at(ne[0]["seq"])
            line = f"Nominations. In a private poll, the village's top suspect is {top}, at {round(100 * sus[top])} percent"
            if top == demon: line += ", and that's the real Demon."
            else: line += f". The real Demon, {demon}, is at {round(100 * sus.get(demon, 0))}."
            ev.append({"k": "panel", "type": "poll", "values": sus, "top": top, "demon": demon})
        self.say(line, ev=ev, hold=0.5)
        self.steps[-1]["ev_end"] += self.claim_events(ne)
        # group nominations
        noms = []
        for e in ne:
            k = e["kind"]
            if k == "nomination": noms.append({"nom": e, "def": None, "res": None, "virgin": None})
            elif k == "defense" and noms: noms[-1]["def"] = e
            elif k == "vote_result" and noms: noms[-1]["res"] = e
            elif k == "virgin" and noms: noms[-1]["virgin"] = e
        execd = next((e["data"]["player"] for e in ne if e["kind"] == "execution" and e["data"].get("died")), None)
        execd_any = next((e["data"]["player"] for e in ne if e["kind"] == "execution"), None)
        # full treatment for the executed nominee, the closest votes; brief for the rest
        def closeness(n):
            r = n["res"]["data"] if n["res"] else None
            return abs(r["votes"] - r["needed"]) if r else 99
        full = set()
        for n in noms:
            if n["nom"]["data"]["nominee"] == execd_any or n["virgin"]: full.add(n["nom"]["seq"])
        for n in sorted(noms, key=closeness):
            if len(full) >= (3 if g.days <= 3 else 2): break
            full.add(n["nom"]["seq"])
        slayers = [e for e in ne if e["kind"] == "slayer"]
        pinned = [e for e in ne if e["seq"] in self.pins and e["kind"] in ("say", "thinking", "whisper")]
        items = sorted([("nom", n["nom"]["seq"], n) for n in noms] + [("slay", e["seq"], e) for e in slayers]
                       + [("pin", e["seq"], e) for e in pinned], key=lambda x: x[1])
        for kind, seq, n in items:
            if kind == "slay": self.slayer(n); continue
            if kind == "pin": self.pinned(n); continue
            nd = n["nom"]["data"]; a, b = nd["nominator"], nd["nominee"]
            res = n["res"]["data"] if n["res"] else None
            if n["virgin"]:
                self.say(f"{a} nominates {b}, the Virgin. {a} is a Townsfolk, so {a} is executed on the spot.",
                         ev=[{"k": "links", "items": [{"from": a, "to": [b], "style": "nominate"}]}, {"k": "hl", "names": [a]}],
                         ev_end=[{"k": "dead", "name": a, "how": f"executed day {d}"}], hold=0.6)
                continue
            if nd.get("text") and seq in full and words(clean(nd["text"])) >= 4:
                self.say(f"{a} nominates {b}.", ev=[{"k": "links", "items": [{"from": a, "to": [b], "style": "nominate"}]}, {"k": "hl", "names": [a]}, {"k": "clearvotes"}], hold=0.1)
                ex = excerpt(nd["text"], 30, prefer=self.pin_re(n["nom"]) or r"\b" + b + r"\b")
                self.quote(a, ex, ev=[{"k": "panel", "type": "nom", "who": a, "nominee": b, "role": self.rolec(a, n["nom"]), "side": "evil" if g.evil[a] else "good", "text": ex}])
                if n["def"] and words(clean(n["def"]["data"]["text"])) >= 4:
                    dx = excerpt(n["def"]["data"]["text"], 30, prefer=self.pin_re(n["def"]))
                    self.quote(b, dx, ev=[{"k": "hl", "names": [b]}, {"k": "panel", "type": "defense", "who": b, "role": self.rolec(b, n["def"]), "side": "evil" if g.evil[b] else "good", "text": dx}])
                if res: self.votes(res, b, d)
            elif res:
                self.say(f"{a} nominates {b}: {num(res['votes'])} vote{'s' if res['votes'] != 1 else ''}, {num(res['needed'])} needed.",
                         ev=[{"k": "links", "items": [{"from": a, "to": [b], "style": "nominate"}]}, {"k": "hl", "names": [a]},
                             {"k": "votes", "nominee": b, "voters": res["voters"], "needed": res["needed"], "outcome": res["outcome"]},
                             {"k": "panel", "type": "section", "title": f"{a} nominates {b}",
                              "sub": f"{res['votes']} vote{'s' if res['votes'] != 1 else ''}, {res['needed']} needed."}], hold=0.4)
        if any(e["kind"] == "no_execution" for e in ne) or (not execd_any and noms):
            self.say("Nobody is executed today.", ev=[{"k": "links", "items": []}], hold=0.5)
        for e in ne:
            if e["kind"] == "execution":
                p = e["data"]["player"]
                if e["data"].get("died"):
                    who = f"{p} is executed. {p} was " + ("evil: the " + g.char[p] + "." if g.evil[p] else f"good: the {self.role(p)}.")
                    self.say(who, ev=[{"k": "dead", "name": p, "how": f"executed day {d}"}, {"k": "links", "items": []}, {"k": "clearvotes"}], hold=0.6)
                else:
                    self.say(f"{p} is executed, but does not die.", hold=0.5)
            if e["kind"] == "becomes" and e["phase"] == "nominations":
                p = e["data"]["player"]
                self.say(f"The Demon is dead, but {p}, the {g.char[p]}, becomes the new Imp. The game goes on.",
                         ev=[{"k": "role", "name": p, "role": f"Imp (was {g.char[p]})", "demon": True}, {"k": "hl", "names": [p]}], hold=0.6)

    def pinned(self, e):
        g = self.g; d = e["data"]; p = d.get("speaker") or d.get("from") or d.get("player")
        ex = excerpt(d["text"], 34, prefer=self.pin_re(e)); side = "evil" if g.evil[p] else "good"
        if ex[:60] in self.shown_texts: return
        if e["kind"] == "thinking":
            self.say(f"{p}'s private thoughts.", ev=[{"k": "hl", "names": [p]}], hold=0.15)
            self.quote(p, ex, ev=[{"k": "panel", "type": "think", "who": p, "role": self.rolec(p, e), "side": side, "text": ex}])
        elif e["kind"] == "whisper":
            self.say(f"{p} whispers to {self.join(d['to'])}.", ev=[{"k": "hl", "names": [p]}], hold=0.15)
            self.quote(p, ex, ev=[{"k": "panel", "type": "whisper", "who": p, "to": d["to"], "role": self.rolec(p, e), "side": side,
                                   "secret": g.evil[p] and all(g.evil[t] for t in d["to"]), "text": ex}])
        else:
            self.say(f"{p}:", ev=[{"k": "hl", "names": [p]}], hold=0.1)
            self.quote(p, ex, ev=[{"k": "panel", "type": "say", "who": p, "role": self.rolec(p, e), "side": side, "text": ex}])

    def rolec(self, p, e):
        c = self.cur(p, e)
        return self.role(p) if c == self.g.char[p] else f"{c} (was {self.g.char[p]})"

    def cur(self, p, e):
        c = self.g.char[p]
        for x in self.g.events:
            if x["seq"] > e["seq"]: break
            if x["kind"] == "becomes" and x["data"]["player"] == p: c = x["data"]["character"]
        return c

    def dead_word(self, p, e):
        return "dead " if p in self.dead_before(e["seq"]) else ""

    def poisoned_on(self, d):
        c = [e["data"]["targets"][0] for e in self.g.events if e["kind"] == "night_choice" and e["day"] == d
             and e["data"]["role"] == "Poisoner" and e["data"].get("targets")]
        return c[-1] if c else None

    def dead_before(self, seq):
        return {e["data"]["player"] for e in self.g.events if e["kind"] == "death" and e["seq"] < seq}

    def votes(self, res, b, d):
        v, need, out = res["votes"], res["needed"], res["outcome"]
        txt = f"{num(v).capitalize()} vote{'s' if v != 1 else ''}, {num(need)} needed. "
        txt += {"block": f"{b} is on the block.", "short": "Not enough.", "tie": "A tie: nobody is on the block."}.get(out, "")
        self.pause(0.3, [{"k": "votes", "nominee": b, "voters": res["voters"], "needed": need, "outcome": out}])
        self.steps[-1]["hold"] = 0.3 + 0.16 * v
        self.say(txt, hold=0.5)

    def slayer(self, e):
        g = self.g; s, t, died = e["data"]["shooter"], e["data"]["target"], e["data"]["died"]
        ev = [{"k": "links", "items": [{"from": s, "to": [t], "style": "shoot"}]}, {"k": "hl", "names": [s]}]
        if g.char[s] != "Slayer":
            txt = f"{s}, who is not really the Slayer, fakes a Slayer shot at {t}. Nothing happens."
        elif died:
            txt = f"{s}, the Slayer, shoots {t}. {t} dies: {t} was the Demon."
            ev.append({"k": "dead", "name": t, "how": "shot by the Slayer"})
        else:
            txt = f"{s}, the Slayer, shoots {t}. Nothing happens."
            if t == g.demon_at(e["seq"]) and self.poisoned_on(e["day"]) == s: txt += f" {t} is the Demon, but {s} is poisoned."
        self.say(txt, ev=ev, hold=0.6)

    # ------------------------------------------------------------ ending
    def ending(self, susp):
        g = self.g
        go = next((e for e in g.events if e["kind"] == "game_over"), None)
        win = g.winner
        demons = [s for s in g.seats if g.char[s] == "Imp"] + [e["data"]["player"] for e in g.events if e["kind"] == "becomes"]
        last = demons[-1]
        reason = go["data"]["reason"] if go else g.reason
        self.say(f"{reason} {win.capitalize()} wins.", ev=[{"k": "outcome", "team": win, "text": f"{win.capitalize()} wins", "reason": reason},
                                                          {"k": "links", "items": []}, {"k": "hl", "names": []}], hold=1.0)
        pts = g.suspicion()
        traj = [(d, p, m.get(last)) for d, p, m in pts if m.get(last) is not None]
        line = f"The Demon was {last}." if len(set(demons)) == 1 else f"The Demon changed hands: {self.join(list(dict.fromkeys(demons)))}."
        if traj:
            line += f" On the last poll, the village gave {last} {round(100 * traj[-1][2])} percent."
        self.say(line, ev=[{"k": "chart", "points": [[d, p, m] for d, p, m in pts], "demons": list(dict.fromkeys(demons)),
                            "evil": [s for s in g.seats if g.evil[s]], "winner": win,
                            "roles": {s: g.role_label(s) for s in g.seats}}], hold=4.0)
        self.pause(1.5, [{"k": "fade"}])


def build(rel):
    b = Builder(rel)
    steps = b.build()
    return {"game": b.g.rel, "title": b.hl["title"] if b.hl else None, "seats": b.g.seats, "evil": b.g.team_models(True),
            "good": b.g.team_models(False), "winner": b.g.winner, "days": b.g.days, "steps": steps}
