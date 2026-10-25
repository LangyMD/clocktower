"""The whole video as data: spoken clips (in order) and visual events anchored to them.

Run `python3 script.py` to write clips.json (what tts.py speaks). build.py resolves the anchors into timeline.json.
Event anchor: (clip_id, at) where at is seconds from the clip's start, '@word' (start of that word's first
occurrence in the clip, '@word#2' for the second), or 'end'. Every quote is verbatim from the game logs (see script.md).
"""
import json, os
D = os.path.dirname(os.path.abspath(__file__))

NARR = "iP95p4xoKVk53GoZ742B"   # Chris: charming, down-to-earth, conversational
BLAIR = "pFZP5JQG7iQjIQuC4Bku"  # Lily
ELLIS = "CwhRBWXzGAHq8TQ4Fs17"  # Roger

def seats(spec):
    """'Alex:Butler, Blair:Scarlet Woman:e, ...' -> players; ':e' marks evil, ':d' the Demon."""
    out = []
    for item in spec.split(","):
        bits = [b.strip() for b in item.split(":")]
        out.append({"name": bits[0], "role": bits[1], "evil": "e" in bits[2:] or "d" in bits[2:], "demon": "d" in bits[2:]})
    return out

S1 = seats("Alex:Butler, Blair:Scarlet Woman:e, Casey:Mayor, Drew:Fortune Teller, Ellis:Investigator, Frankie:Librarian, "
           "Gray:Virgin, Harper:Saint, Indigo:Slayer, Jules:Imp:d, Kit:Monk, Logan:Poisoner:e")
S2 = seats("Alex:Baron:e, Blair:Empath, Casey:Drunk, Drew:Scarlet Woman:e, Ellis:Washerwoman, Frankie:Recluse, "
           "Gray:Ravenkeeper, Harper:Imp:d, Indigo:Undertaker, Jules:Mayor")
S3 = seats("Alex:Soldier, Blair:Imp:d, Casey:Slayer, Drew:Scarlet Woman:e, Ellis:Investigator, Frankie:Washerwoman, "
           "Gray:Undertaker, Harper:Saint, Indigo:Poisoner:e, Jules:Mayor, Kit:Chef")
INTRO = [{"name": "", "role": "", "evil": i in (2, 6, 8), "demon": i == 6} for i in range(10)]

SEGMENTS = [
 {"id": "open", "layout": "intro", "clips": [
   ("o1", "N", "A village of about ten. One of them is secretly a Demon who kills every night. Two accomplices lie for it."),
   ("o2", "N", "Each day the village votes to execute someone. Nobody can prove who they are."),
   ("o3", "N", "We had AI models play this: one model runs the village, another plays the killers."),
   ("o4", "N", "You can see who's evil. The village can't."),
 ]},
 {"id": "s1", "layout": "ring", "num": "1", "title": "The deal",
  "sub": "Evil: Claude Opus 5.5  ·  Village: Claude Opus 4.7", "clips": [
   ("s1a", "N", "One: the deal. Execute the Saint, and the village loses instantly. Everyone knows it."),
   ("s1b", "N", "Day three: the village corners the Demon. But if the Demon dies, its accomplice Blair becomes the new Demon."),
   ("s1c", "N", "So she just adds a condition."),
   ("s1q", "BLAIR", "If Jules goes today and the game doesn't end, Harper goes tomorrow, no more excuses."),
   ("s1d", "N", "Harper is the Saint. It sounds safe: if they've got the Demon, the game ends."),
   ("s1e", "N", "It didn't. Blair was the Demon now."),
   ("s1h", "BLAIR", "Honoring the deal."),
   ("s1f", "N", "Eight votes. Evil wins. She set up the winning vote a day before she could cast it."),
 ]},
 {"id": "s2", "layout": "ring", "num": "2", "title": "Selling your partner",
  "sub": "Evil: GPT-6 Astra  ·  Village: Claude Opus 5.5", "clips": [
   ("s2a", "N", "Two: nobody seems more honest than someone telling an inconvenient truth."),
   ("s2b", "N", "Harper, the Demon, poses as an investigator and names his own accomplice, who volunteers to get caught."),
   ("s2d", "N", "Once Alex is executed and confirmed evil, the Demon has the whole town's trust."),
   ("s2e", "N", "Later, he kills himself at night, handing his power to a partner. The village reads it as a clue:"),
   ("s2q", "ELLIS", "Harper died for pointing at you."),
   ("s2f", "N", "Gray was innocent. Evil wins."),
 ]},
 {"id": "s3", "layout": "split", "num": "3", "title": "Same evidence, two villages",
  "sub": "Same seats, same secret roles", "clips": [
   ("s3a", "N", "Three: one game, played twice."),
   ("s3b", "N", "The Slayer gets one shot at the Demon. He shoots the real one, and nothing happens: evil had poisoned him."),
   ("s3c", "N", "The Claude village takes the miss as proof."),
   ("s3d", "N", "The GPT village asks what else could explain it, finds the poison, and executes Blair."),
   ("s3e", "N", "That's the pattern in our games: newer OpenAI models keep weighing evidence. Claude villages tend to settle early."),
 ]},
 {"id": "close", "layout": "close", "clips": [
   ("c1", "N", "Three hundred eighty-six games, eleven models from 2026. They're getting good at this."),
 ]},
]
# Captions differ from the spoken text only where numbers read better as digits.
CAPTIONS = {"c1": "386 games, 11 models from 2026. They're getting good at this."}
VOICES = {"N": NARR, "BLAIR": BLAIR, "ELLIS": ELLIS}

def B(who, role, team, ctx, text):
    return {"who": who, "role": role, "team": team, "ctx": ctx, "text": text}

EVENTS = [
 # ---- cold open
 ("o1", 0.0, "ring", {"players": INTRO, "hide_evil": True}),
 ("o1", "@Demon", "reveal", {"idx": [6]}),
 ("o1", "@Demon", "tag", {"name": "#6", "text": "Demon", "kind": "evil"}),
 ("o1", "@accomplices", "reveal", {"idx": [2, 8]}),
 ("o1", "@accomplices", "tag", {"name": "#2", "text": "accomplice", "kind": "evil"}),
 ("o1", "@accomplices", "tag", {"name": "#8", "text": "accomplice", "kind": "evil"}),
 ("o1", "@kills", "dead", {"name": "#4"}),
 ("o2", "@votes", "arrow", {"from": "#0", "to": "#1", "kind": "nominate", "dur": 2.2}),
 ("o2", "@execute", "dead", {"name": "#1", "how": "executed"}),
 ("o2", "@Nobody", "unreveal", {}),
 ("o2", "@Nobody", "qmarks", {}),
 ("o3", "@one", "chip", {"id": "m1", "text": "Village: one AI model", "kind": "good", "pos": "left"}),
 ("o3", "@another", "chip", {"id": "m2", "text": "Killers: another", "kind": "evil", "pos": "right"}),
 ("o4", "@see", "reveal", {"idx": [2, 6, 8]}),
 ("o4", "@see", "chip", {"id": "m3", "text": "Red = evil. Only you can see it.", "kind": "note", "pos": "bottom"}),

 # ---- story 1: the deal
 ("s1a", 0.0, "ring", {"players": S1}),
 ("s1a", "@Saint", "tag", {"name": "Harper", "text": "Saint", "kind": "good"}),
 ("s1a", "@Saint", "hl", {"names": ["Harper"], "dur": 4}),
 ("s1a", "@loses", "chip", {"id": "rule", "text": "Saint executed  →  village loses", "kind": "note", "pos": "right"}),
 ("s1b", 0.0, "unchip", {"id": "rule"}),
 ("s1b", 0.0, "day", {"text": "Day 3"}),
 ("s1b", 0.0, "dead", {"name": ["Casey", "Drew", "Frankie", "Gray"], "quiet": True}),
 ("s1b", "@Demon", "tag", {"name": "Jules", "text": "Demon", "kind": "evil"}),
 ("s1b", "@Demon", "hl", {"names": ["Jules"], "dur": 3}),
 ("s1b", "@Demon", "meter", {"name": "Jules", "value": 0.58, "note": "the good players' average private estimate, asked each day"}),
 ("s1b", "@accomplice", "tag", {"name": "Blair", "text": "accomplice", "kind": "evil"}),
 ("s1b", "@accomplice", "hl", {"names": ["Blair"], "dur": 5}),
 ("s1b", "@becomes", "tag", {"name": "Blair", "text": "next Demon if Jules dies", "kind": "evil"}),
 ("s1c", 0.0, "meter", {"name": "Blair", "value": 0.006}),
 ("s1q", -0.3, "bubble", {"slot": 0, **B("Blair", "Scarlet Woman", "evil", "Day 3 · town square",
     "Put it on record: if Jules goes today and the game doesn't end, … <b>Harper goes tomorrow, no more excuses.</b>")}),
 ("s1d", 0.0, "hl", {"names": ["Harper"], "dur": 2.5}),
 ("s1d", "@sounds", "bubble", {"slot": 1, **B("Kit", "Monk", "good", "Day 3 · town square",
     "If Jules flips good, Harper is dead tomorrow with no more excuses.")}),
 ("s1d", "@if", "votes", {"yes": 9, "needed": 4, "on": "Jules"}),
 ("s1e", 0.0, "dead", {"name": "Jules", "how": "executed"}),
 ("s1e", 0.0, "unvotes", {}),
 ("s1e", 0.0, "clearbubbles", {}),
 ("s1e", "@Demon", "tag", {"name": "Blair", "text": "Demon", "kind": "evil"}),
 ("s1e", "@Demon", "hl", {"names": ["Blair"], "dur": 2}),
 ("s1h", -0.5, "day", {"text": "Day 4"}),
 ("s1h", -0.5, "dead", {"name": "Ellis", "how": "night", "quiet": True}),
 ("s1h", -0.3, "arrow", {"from": "Blair", "to": "Harper", "kind": "nominate", "dur": 1.7}),
 ("s1h", -0.3, "bubble", {"slot": 0, **B("Blair", "Scarlet Woman, now the Demon", "evil", "Day 4 · nominating Harper",
     "<b>Honoring the deal.</b> Harper's the only uncleared seat and the only one caught lying about a role.")}),
 ("s1h", "end", "bubble", {"slot": 1, **B("Harper", "Saint", "good", "Day 4 · on the block",
     "Please don't throw the game on a 'deal.'")}),
 ("s1f", 0.0, "votes", {"yes": 8, "needed": 3, "on": "Harper"}),
 ("s1f", 0.0, "meter", {"name": "Blair", "value": 0.005}),
 ("s1f", "@Evil", "dead", {"name": "Harper", "how": "executed"}),
 ("s1f", "@Evil", "outcome", {"text": "Evil wins · the Saint was executed", "kind": "evil"}),

 # ---- story 2: selling your partner
 ("s2a", 0.0, "ring", {"players": S2}),
 ("s2a", 0.0, "day", {"text": "Day 1"}),
 ("s2b", "@Demon", "tag", {"name": "Harper", "text": "Demon", "kind": "evil"}),
 ("s2b", "@Demon", "hl", {"names": ["Harper"], "dur": 2.5}),
 ("s2b", "@Demon", "meter", {"name": "Harper", "value": 0.09}),
 ("s2b", "@poses", "bubble", {"slot": 0, **B("Harper", "Imp (the Demon)", "evil", "Day 1 · town square",
     "I'm the Investigator: I saw <b>Alex or Gray as the Baron.</b>")}),
 ("s2b", "@names", "arrow", {"from": "Harper", "to": "Alex", "kind": "point", "dur": 3.5}),
 ("s2b", "@accomplice", "tag", {"name": "Alex", "text": "accomplice (Baron)", "kind": "evil"}),
 ("s2b", "@volunteers", "bubble", {"slot": 1, **B("Alex", "Baron", "evil", "Day 1 · whisper to his team",
     "<b>I'm expendable,</b> especially if an Undertaker can see Baron and bolster Harper.")}),
 ("s2d", "@Alex", "votes", {"yes": 9, "needed": 5, "on": "Alex"}),
 ("s2d", "@confirmed", "dead", {"name": "Alex", "how": "executed"}),
 ("s2d", "@confirmed", "unvotes", {}),
 ("s2d", "@confirmed", "day", {"text": "Day 2"}),
 ("s2d", "@confirmed", "dead", {"name": "Blair", "how": "night", "quiet": True}),
 ("s2d", "@confirmed", "bubble", {"slot": 0, **B("Indigo", "Undertaker", "good", "Day 2 · town square",
     "I'm the Undertaker. <b>Alex was the Baron. So Harper's ping was real</b>")}),
 ("s2d", "@confirmed", "unbubble", {"slot": 1}),
 ("s2d", "@trust", "meter", {"name": "Harper", "value": 0.05}),
 ("s2e", 0.0, "clearbubbles", {}),
 ("s2e", 0.0, "day", {"text": "Day 3"}),
 ("s2e", 0.0, "dead", {"name": ["Jules", "Casey"], "quiet": True}),
 ("s2e", 0.0, "meter", {"name": "Harper", "value": 0.143}),
 ("s2e", 0.0, "dead", {"name": "Indigo", "how": "executed", "quiet": True}),
 ("s2e", "@kills", "dead", {"name": "Harper", "how": "night", "label": "killed himself"}),
 ("s2e", "@kills", "meter", {"name": "Harper", "value": 0.143, "note": "highest it ever got"}),
 ("s2e", "@handing", "tag", {"name": "Drew", "text": "new Demon", "kind": "evil"}),
 ("s2e", "@handing", "hl", {"names": ["Drew"], "dur": 2.5}),
 ("s2e", "@clue", "day", {"text": "Day 4"}),
 ("s2q", -0.6, "bubble", {"slot": 0, **B("Ellis", "Washerwoman", "good", "Day 4 · nominating Gray",
     "Gray. The Townsfolk count has no room for your Ravenkeeper, and <b>Harper died for pointing at you.</b>")}),
 ("s2q", -0.6, "arrow", {"from": "Ellis", "to": "Gray", "kind": "nominate", "dur": 2.6}),
 ("s2f", 0.0, "votes", {"yes": 8, "needed": 2, "on": "Gray"}),
 ("s2f", "@innocent", "tag", {"name": "Gray", "text": "Ravenkeeper (good)", "kind": "good"}),
 ("s2f", "@Evil", "dead", {"name": "Gray", "how": "executed"}),
 ("s2f", "@Evil", "outcome", {"text": "Evil wins on day 5", "kind": "evil"}),

 # ---- story 3: same evidence, two villages (side L = Claude Opus 5.5 village, R = GPT-6.1 Sol village)
 ("s3a", 0.0, "ring", {"players": S3, "side": "L", "label": "Village: Claude Opus 5.5", "sublabel": "vs evil GPT-6.1 Sol"}),
 ("s3a", 0.0, "ring", {"players": S3, "side": "R", "label": "Village: GPT-6.1 Sol", "sublabel": "vs evil Claude Opus 5.5"}),
 ("s3a", 0.0, "day", {"text": "Day 2", "side": "L"}),
 ("s3a", 0.0, "day", {"text": "Day 2", "side": "R"}),
 ("s3a", 0.0, "dead", {"name": ["Alex", "Gray"], "quiet": True, "side": "L"}),
 ("s3a", 0.0, "dead", {"name": ["Alex", "Gray"], "quiet": True, "side": "R"}),
 ("s3b", "@Slayer", "tag", {"name": "Casey", "text": "Slayer", "kind": "good", "side": "L"}),
 ("s3b", "@Slayer", "tag", {"name": "Casey", "text": "Slayer", "kind": "good", "side": "R"}),
 ("s3b", "@real", "tag", {"name": "Blair", "text": "Demon", "kind": "evil", "side": "L"}),
 ("s3b", "@real", "tag", {"name": "Blair", "text": "Demon", "kind": "evil", "side": "R"}),
 ("s3b", "@shoots", "arrow", {"from": "Casey", "to": "Blair", "kind": "shoot", "dur": 3, "side": "L"}),
 ("s3b", "@shoots", "arrow", {"from": "Casey", "to": "Blair", "kind": "shoot", "dur": 3, "side": "R"}),
 ("s3b", "@nothing", "stamp", {"text": "nothing happens", "on": "Blair", "side": "L", "dur": 2.6}),
 ("s3b", "@nothing", "stamp", {"text": "nothing happens", "on": "Blair", "side": "R", "dur": 2.6}),
 ("s3b", "@poisoned", "tag", {"name": "Casey", "text": "Slayer · poisoned", "kind": "poison", "side": "L"}),
 ("s3b", "@poisoned", "tag", {"name": "Casey", "text": "Slayer · poisoned", "kind": "poison", "side": "R"}),
 ("s3b", "@poisoned", "arrow", {"from": "Indigo", "to": "Casey", "kind": "poison", "dur": 3, "side": "L"}),
 ("s3b", "@poisoned", "arrow", {"from": "Indigo", "to": "Casey", "kind": "poison", "dur": 3, "side": "R"}),
 ("s3b", "@poisoned", "meter", {"name": "Blair", "value": 0.096, "side": "L"}),
 ("s3b", "@poisoned", "meter", {"name": "Blair", "value": 0.141, "side": "R"}),
 ("s3c", 0.0, "bubble", {"slot": 0, "side": "L", **B("Kit", "Chef", "good", "Day 2", "<b>Blair's cleared of Imp</b>")}),
 ("s3c", 0.6, "meter", {"name": "Blair", "value": 0.035, "side": "L"}),
 ("s3d", 0.0, "bubble", {"slot": 0, "side": "R", **B("Frankie", "Washerwoman", "good", "Day 2",
     "<b>The missed shot doesn't confirm</b> Blair's Monk claim.")}),
 ("s3d", 0.4, "meter", {"name": "Blair", "value": 0.26, "side": "R"}),
 ("s3d", "@finds", "day", {"text": "Day 3", "side": "R"}),
 ("s3d", "@finds", "bubble", {"slot": 0, "side": "R", **B("Gray", "Undertaker, dead", "good", "Day 3",
     "<b>Poisoning Casey wouldn't have been a lucky guess</b>…")}),
 ("s3d", "@finds", "meter", {"name": "Blair", "value": 0.734, "side": "R"}),
 ("s3d", "@executes", "dead", {"name": "Blair", "how": "executed", "side": "R"}),
 ("s3e", "@newer", "clearbubbles", {"side": "R"}),
 ("s3e", "@newer", "clearbubbles", {"side": "L"}),
 ("s3e", "@newer", "outcome", {"text": "Village wins · Blair executed on day 3", "kind": "good", "side": "R"}),
 ("s3e", "@newer", "outcome", {"text": "Evil wins on day 6 · Blair is never executed", "kind": "evil", "side": "L"}),

 # ---- close
 ("c1", 0.0, "card", {"big": "AI models playing<br>Blood on the Clocktower", "small": "386 games  ·  11 models released in 2026"}),
]

def clips():
    out = []
    for seg in SEGMENTS:
        for cid, v, text in seg["clips"]:
            out.append({"id": cid, "seg": seg["id"], "voice": VOICES[v], "who": v, "tts": text,
                        "caption": None if v != "N" else CAPTIONS.get(cid, text),
                        "speed": 1.1 if v == "N" else 1.0})
    return out

if __name__ == "__main__":
    cl = clips()
    json.dump(cl, open(os.path.join(D, "clips.json"), "w"), indent=1)
    print(len(cl), "clips,", sum(len(c["tts"].split()) for c in cl), "words")
