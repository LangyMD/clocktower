"""Print an episode's script as text (no TTS, no rendering): python3 -m stream.dryrun v16/f2-.../game-01"""
import sys
from . import script

for rel in sys.argv[1:]:
    ep = script.build(rel)
    n = chars = 0
    for s in ep["steps"]:
        c = s["clip"]
        if c:
            chars += len(c["text"]); n += 1
            print(f'{c["who"]:>7}: {c["show"]}')
    print(f"# {rel}: {n} clips, {chars} characters, ~{chars / 14.5 / 60 + n * 0.5 / 60:.1f} min")
