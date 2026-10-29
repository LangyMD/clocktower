## What and why

## Checklist

- [ ] `python -m unittest discover -s tests` passes (no test calls a paid API)
- [ ] Does this change how games play? If yes, it follows "Changing the rules" in CONTRIBUTING.md (protocol bump,
      `docs/PROTOCOL.md`, `docs/protocol-history.md`, calibration batch); if no, say why not.
- [ ] Rating code untouched, or `python -m clocktower ratings --no-page` still reproduces `docs/plans/f2-ratings.json`
- [ ] Docs updated (README, `docs/findings/README.md`, `experiments/README.md`) where relevant
- [ ] For new games: plan in `experiments/`, configs and results included, cost stated
