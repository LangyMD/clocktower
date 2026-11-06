# Sources

Everything in this folder is written in our own words. Where it summarises rules or advice, these are the sources.

## Official

- Official wiki: <https://wiki.bloodontheclocktower.com/> (rules, every character page with "How to Run",
  "Tips & Tricks" and "Bluffing as" sections, script pages, Storyteller advice). Each character's page is linked
  from `wiki` in [data/characters.json](data/characters.json).
- TPI toolmaker resources: <https://github.com/ThePandemoniumInstitute/botc-release> (character data, night
  sheet, jinxes, script JSON schema). Used for the structural fields in [data/](data/).
- Script tool: <https://script.bloodontheclocktower.com/>.
- Publisher site and Community Created Content Policy: <https://bloodontheclocktower.com/>.

## Community

- botcscripts.com, the community script library: <https://botcscripts.com/>.
- r/BloodOnTheClocktower: <https://www.reddit.com/r/BloodOnTheClocktower/>.
- Pocket Grimoire and Clocktower.online, community tools for running games.
- Long-running community podcasts and video series on Storytelling and strategy.

## Notes on accuracy

- The official wiki could not be fetched from the environment that wrote these docs, so the rules and advice
  here are summaries from general knowledge of the game, checked against TPI's published data. Spot-check
  details against the linked wiki pages before implementing a rule.
- The experimental characters change occasionally; `python scripts/botc_data.py fetch && build` refreshes the
  structural data, but summaries and tags need a human (or model) to update.
