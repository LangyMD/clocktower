"""The curated highlight episodes: a title and a short hand-written hook each (no spoilers past day 1).

Picks and facts come from docs/analysis/blog/best-games.md, docs/analysis/f2/interesting.md and
docs/analysis/astra/cunning-evil.md, where every quote was checked against the logs. Order = render order.
"""
HIGHLIGHTS = [
    ("v16/f2-opus47-v-opus55/game-01", "The deal",
     ["One of our favourite games. Watch Blair, the Scarlet Woman: if her Demon dies, she takes his place.",
      "Keep an eye on the promises people make in public."]),
    ("v17/f3-opus47-v-fable51/game-03", "The poisoned vision",
     ["In this game the Demon pretends to be the Undertaker, the player who learns what each executed player really was.",
      "So the evil team gets to write the truth about every body."]),
    ("v17/f3-opus55-v-sol61/game-02", "The dead man's reading",
     ["On day one, the Demon quietly claims to be the Ravenkeeper, a role that learns something when it dies at night.",
      "He has a plan for that."]),
    ("v17/f3b-astra-v-opus55/game-01-swap", "Selling his own Minion",
     ["Here the Demon claims Investigator, with a result that is true.",
      "Watch what his own Minion volunteers to do with it."]),
    ("v17/f3b-astra-v-opus55/game-02", "The Empath number",
     ["A detective story. The evil team here is clever, and its Spy can see everyone's secret roles.",
      "Watch for the moment someone knows more than they should."]),
    ("v16/f2-fable5-v-gpt56sol/game-01", "The machine never bled",
     ["The Demon here claims to be the Fortune Teller, and invents her results each night.",
      "The village has to work out how those results were produced."]),
    ("v17/f3-fable5-v-gpt56sol/game-01", "The writers' room",
     ["Three evil players, one fictional history. Watch the evil team edit its lies before publishing them."]),
    ("v16/f2-opus46-v-opus48/game-01", "The Imp nobody suspected",
     ["Watch Blair, the Demon. She says little, agrees with everyone, and keeps an eye on the vote count."]),
    ("v16/f2-astra-v-sol61/game-01-swap", "Same seats, part one",
     ["The same seats and secret roles, played twice. In this game GPT-6 Astra plays evil, against GPT-6.1 Sol."]),
    ("v16/f2-astra-v-sol61/game-01", "Same seats, part two",
     ["The same seats and secret roles as the last game, with the teams swapped: now GPT-6 Astra is the village."]),
    ("v17/f3-gpt54-v-opus55/game-02", "A gift from the Drunk",
     ["Early on, the Saint privately tells the Demon what they are. The evil team will find a use for that."]),
    ("v16/f2-gpt55-v-astra/game-01", "The Imp takes the Virgin test",
     ["The Virgin is good: the first Townsfolk to nominate her is executed on the spot.",
      "Watch who volunteers to test her."]),
]


# Moments the episode must quote (substrings of the verbatim text; each must be found in the game's events).
PINS = {
    "v16/f2-opus47-v-opus55/game-01": ["Harper goes tomorrow, no more excuses", "only one who could point SW at me",
                                       "Please don't throw the game on a 'deal.'"],
    "v17/f3-opus47-v-fable51/game-03": ["DON'T say Spy", "Drew flipped Scarlet Woman", "my death clears my reads"],
    "v17/f3-opus55-v-sol61/game-02": ["keeping it quiet so I might actually get a night result", "Considering self-kill tonight",
                                      "Better: I'll report Harper as Imp", "I changed my intended pick after Blair was executed",
                                      "There's also the starpass possibility"],
}


def get(rel):
    for r, title, hook in HIGHLIGHTS:
        if r == rel:
            return {"title": title, "hook": hook, "pins": PINS.get(rel, [])}
    return None
