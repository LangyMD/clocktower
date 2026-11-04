# Hand-off: the `gui-redesign` branch

For whoever deploys and secures clocktowerbench.com and the play server. This branch restyles every user-facing
surface (the static site in `site/` and the play table in `clocktower/table/`) and is local only: nothing was
pushed, deployed or put behind DNS. Base: `main` at c2fd11c.

The final look is the **minimal** one. The earlier, richer animatic-style passes are kept as their own commits so
they can be compared or restored:

| Commit | What |
|---|---|
| `Site: animatic redesign, first pass` | the Nov 4 preview, ported unchanged (parchment sheets, corner caps, pixel type) |
| `Play table: animatic restyle, rich pass` | the same look on the play table; also the server, CSP and lobby fixes below |
| `Site: minimal, findability-first redesign` | the current site |
| `Play table: minimal pass` | the current play table |
| `Tests: …`, `Site: focus order, …`, `Hand-off …` | a CSP/font test, small site fixes, this file and a short CLAUDE.md note |

## Information architecture: what moved where

| Before (main / first pass) | Now |
|---|---|
| Header: Leaderboard · Games · Play · About (Highlights a tab under Games; Run your own and Dataset only in the footer) | Header: **Leaderboard · Games · Highlights · Play · About**, all top level, current page marked, same row on phones |
| Home: hero, "what is this", three how-it-works panels, leaderboard sheet + four stats, play band, three highlight cards, explainer video | Home: one-sentence pitch, three actions (**Read a highlight**, **Browse games**, **Play against the AIs**), the leaderboard table, the video essay once it exists |
| "What is this", the how-it-works steps, the explainer video | **About** (`#what`) |
| Run your own (`run.html`) | **About** (`#run-your-own`); `run.html` is a stub that links there |
| Dataset (footer only) | **About** (`#data`) and the footer |
| Games: 538 vs-cards, eight dropdowns | Games: one row per game, three filters + sort up front, **More filters** for the rest, sortable headers, 50 a page |
| Highlights: long parchment cards | Highlights: a list (title, one line, matchup, links; the story behind "The story") |
| Game page: big vs card, chips, a separate toolbar, a seats grid | Game page: one-line header, **Players** table, one sticky bar (days, Reveal secrets, See as) |
| Play page: hero over a painted plate | Play page: plain page, "Open the table" first |
| Play table: no phase banner; small "Night 1" in the header | Play table: **phase band** (when we are + Your turn / Sent / Waiting) and a **dock** that says what you can do now |

## Build and preview locally

```sh
pip install -e .
python -m unittest discover -s tests          # no API calls
python -m clocktower.export --games games     # the site -> site/dist (no logs here: empty library, by design)
python -m http.server -d site/dist 8000       # http://localhost:8000
python -m clocktower play                     # the play table; prints a host link
```

For the play table without any spend, remove the provider keys from the environment first (for example
`env -u OPENAI_API_KEY -u ANTHROPIC_API_KEY python -m clocktower play`) and pick "Practice bots" for both teams.
The local server's rate limit is 40 reads per second per IP, so several scripted players polling from one machine
will see 429s.

## What changed, by file

### Play server (`python -m clocktower play`)

Routes, API, game logic, limits, storage and key handling are unchanged. Only what serving the restyled page needs:

- `clocktower/web.py`
  - `TYPES` also serves `.woff` and `.woff2` (`font/woff`, `font/woff2`), for the page's own fonts. Nothing else new is
    served: the existing rule still only serves files inside `clocktower/table/` with a listed suffix.
  - The Content-Security-Policy is **tighter** (see "CSP" below): no Google Fonts hosts, no `'unsafe-inline'` styles.
- `pyproject.toml`: `package-data` adds `table/fonts/*`, so a `pip install .` ships the fonts. (The Docker image
  runs from `/app/clocktower`, which already contains them.)
- `clocktower/table/index.html`, `table.css`, `table.js`: the restyle. Front-end only. In short:
  - A **phase band** under the header always says when we are (Night 2 / Day 2 · Whispers 3 of 6 / Town square /
    Vote on Gray), with a track of the day's beats and a **Your turn / Sent / Waiting** flag.
  - The **dock** says what you can do now in one line ("Whisper to one or two players. Only they will see it."),
    keeps the engine's exact prompt underneath (tap to expand), and after you act shows what you did ("You
    whispered to Jules. Waiting for the others…"). Buttons show a busy state while a request is in flight.
  - Whispers (dashed, italic, lock), town-square speech, nominations, ballots (hands raised, tally), executions and
    deaths each have their own look. The phone shows the whole town in a two-row strip instead of a cut-off row.
  - Accessibility: every control is ≥ 44 px; focus is visible; sheets move focus in and back out; Escape closes
    sheets and the Grimoire; a polite live region for the feed and an assertive one for "Your turn"; reduced motion
    turns all animation off.
  - **No inline `style=` attributes** anywhere in the markup (positions and delays are set through
    `element.style`, which the CSP allows). Required by the tightened CSP; a test checks it.
  - **Bug fix**: changing your allegiance in the lobby after joining posted to `/api/me` (a 404 the page ignored),
    so the change never reached the server. It now posts to `/api/t/<table>/me`, the existing route.
- `clocktower/table/fonts/`: Pirata One (`.woff`, the original font data, only WOFF-compressed, because its name is
  reserved), Inter and EB Garamond (`.woff2`, Latin subsets), and `OFL.txt` (SIL Open Font License with each font's
  copyright). About 130 KB in all.
- `tests/test_web.py`: `test_self_hosted_assets_and_strict_csp` (the CSP has no external host and no
  `'unsafe-inline'`; the page and script carry no inline styles; each font is served with the right type; every
  `url()` in the stylesheet resolves; `OFL.txt` is not served).

### Static site (`site/`)

Content and data are unchanged except where noted; the exporter is unchanged.

- Navigation: **Leaderboard · Games · Highlights · Play · About**, every destination at the top level, current page
  marked, a plain row of links on phones (no menu button).
- `pages/index.html`, `assets/home.js`: a short home: one-sentence pitch, three actions (read a highlight, browse
  games, play), the leaderboard table, and the video essay embed once `youtubeVideoId` is set (until then no video
  section; with only `videoUrl` set, a "Watch the video essay" button appears).
- `pages/games.html`, `assets/library.js`: a dense list, one row per game (good model vs evil model with tokens,
  winner in team colour, ends on day N, players, Minions, twin link), the whole row clickable, Model / Playing /
  Winner / Sort up front and the rest under More filters, sortable column headers, 50 rows a page, filters and page
  in the URL (old `?good=`, `?evil=`, `?sort=long` links still work). Tested with 538 rows.
- `pages/highlights.html`, `assets/highlights.js`: a plain list (title, one line, matchup, "Jump to the moment",
  the story behind a disclosure).
- `pages/game.html`, `assets/viewer.js`: a one-line header (good X vs evil Y, result), a players table, and one
  sticky bar for the day, Reveal secrets and "See as". The first pass's summary-only fallback ("Transcript not in
  this build") is removed.
- `pages/about.html`, `assets/about.js`: now also holds "what this is", the three how-it-works steps, the explainer
  video (shown only if it loads), **Run your own** (`#run-your-own`) and **The data** (`#data`).
  `pages/run.html` is kept as a stub that links there (old links keep working).
- `pages/leaderboard.html`, `assets/leaderboard.js`, `assets/site.js`: same tables and charts, recoloured for the dark
  page (head-to-head cells capped so text stays above 4.5:1).
- `pages/play.html`, `404.html`, `layout.html`, `assets/style.css` (rewritten), `assets/icon.svg`.
- `assets/fonts/`: Pirata One (wordmark and page titles only), Inter (interface), EB Garamond (reading), `OFL.txt`.
- `assets/img/tower.webp`: the one painted plate (from the video essay's animatic, original art), home hero only.
- `config.json`: `playUrl` is `https://clocktower-ogul.onrender.com` (set by the first pass; see open questions);
  new key `videoUrl`.
- **Transcript-only rule** (Aaron: "we shouldn't be able to look at games if we can't see the transcripts"): the
  exporter already exports only games with `events.jsonl`; the library, twin links and highlights now list and link
  only games present in `data/index.json`. A build without the logs has an empty library (a plain empty state); the
  leaderboard still works because it reads `docs/plans/f2-ratings.json`.
- `site/README.md`: pages, look, fonts and the transcript-only rule.

## Deliberately untouched

- `clocktower/export.py` (the exporter's data logic), `clocktower/ratings.py`, `docs/plans/*`, all game data.
- `stream/`, `Dockerfile`, `fly.toml`, `render.yaml`, `docs/hosting.md`, `site/deploy/github-pages.yml`, DNS.
- Everything in `web.py` beyond `TYPES` and `CSP`: routes, API, game logic, limits, rate limits, key handling, logs.
- `clocktower/viewer/` (the older spectator viewer). No public page uses it: it is served only by the local
  `python -m clocktower watch` command and was published as a claude.ai artifact. Left as it was.

## External hosts and CSP

### Play server

| | Before | After |
|---|---|---|
| `style-src` | `'self' 'unsafe-inline' https://fonts.googleapis.com` | `'self'` |
| `font-src` | `https://fonts.gstatic.com` | `'self'` |
| everything else | `default-src 'self'; script-src 'self'; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'` | unchanged |

The play page now loads nothing from any other host. `img-src data:` stays for the inline SVG favicon. Links out
(clocktowerbench.com) are plain navigations. Any future inline `style=` in table markup will be blocked by the
browser: set styles from JS with `element.style` or use classes.

Worth considering (not done; server logic): the server sends `Cache-Control: no-store` on everything, fonts
included, so each page load fetches ~130 KB of fonts again. A long `max-age` for `/fonts/*` would fix that.

### Static site

The site has no CSP of its own (that is the static host's job). Hosts it can contact:

- **No font hosts any more**: Google Fonts (`fonts.googleapis.com`, `fonts.gstatic.com`) is gone; fonts are in
  `assets/fonts/`.
- `www.youtube-nocookie.com` (iframe) on the home page, only when `youtubeVideoId` is set.
- `huggingface.co`: the explainer video fallback on About (`explainerFallback`; returns 401 while the dataset is
  private, so the video simply stays hidden and the console logs one failed request), the dataset links, and
  `gameDataBase` if you point it there.
- Plain links: `playUrl`, `postUrl`, `githubUrl`, `videoUrl`.
- No inline `<script>` blocks remain. Inline `style=` attributes are still used by the charts, bars and the replay
  viewer, so a CSP for the site needs `style-src 'self' 'unsafe-inline'`.

A starting point if you add headers on Cloudflare Pages (`site/dist/_headers`), to verify against the final config:

```
/*
  Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; font-src 'self'; img-src 'self' data:; media-src 'self' https://huggingface.co https://*.hf.co; frame-src https://www.youtube-nocookie.com; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'none'
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
```

If `gameDataBase` points at Hugging Face, add its host (and the CDN it redirects to) to `connect-src`.

## Config keys still to fill (`site/src/config.json`)

| Key | What | Until set |
|---|---|---|
| `videoUrl` | link to the video essay | About's "Watch the video essay" shows "(soon)" |
| `youtubeVideoId` | the essay's YouTube id; embedded on the home page | no video section on home |
| `postUrl` | the blog post | About's "Read the post" shows "(soon)" |
| `githubUrl` | the public repository | footer link hidden; About's GitHub button "(soon)"; quick start shows a placeholder URL |

Also check `playUrl` (see open questions) and `datasetUrl` (set to the HF dataset page).

## Building with the real logs

The full site needs the game logs from the private Hugging Face dataset **`dwarkesh/clocktower-games`** to publish
the 538 games; without them the library is empty by design.

```sh
pip install -e .
export HF_TOKEN=...                       # read access to dwarkesh/clocktower-games while it is private
python -m clocktower fetch v16/f2-* v17/f3* v17/f4-* v17/f5-* v17/b1-* v17/b2-*
python -m clocktower.export --games games --media media/explainer-three-tricks/explainer-three-tricks.mp4
python -m http.server -d site/dist 8000   # http://localhost:8000
```

Then check: the library shows 538 games; a game page shows nights, whispers, reasoning and the "Who does the town
suspect?" table; the ten highlights appear (they are hidden when their games are not in the build) and "Jump to the
moment" lands on the quote; twin links work. `--media` is optional (without it the explainer tries the dataset).

## What was verified

- `python -m unittest discover -s tests` passes (117 tests). One test, `test_game_survives_a_restart`, failed once
  in four runs; it is timing-dependent and failed the same way on `main` before any change.
- Both build commands run from this branch: `python -m clocktower.export --games games` (with the local practice
  games, see below) and `python -m clocktower play`.
- The play table end to end, with no API calls: a keyless server, `random` practice bots, scripted people over the
  API and two browser seats driven through the real UI (a desktop host at 1366 px and a phone guest at 390 px), over
  whole games: lobby (home, join, gather, latecomer, dead link), role card, night, dawn deaths, whispers, town
  square, nominations, defense, comments, votes, execution, every sheet, game over and the Grimoire. No console or
  CSP errors.
- The site at 1366 px and 390 px on every page, with real practice-game logs in the replay viewer, and the games
  list with 538 rows (a layout-only build from the snapshot's results, never deployable).
- Text contrast ≥ 4.5:1 for every text colour on every surface used; keyboard focus visible on links, buttons, rows
  and the play table's controls.

Screenshots (outside the repo, on Aaron's machine): `claude_scratch/botc_essay/site_redesign/shots_v2/`:
`site_before` / `site_after` (desktop 1366 and phone 390, first screen and full page), `site_stress538` (the list
with 538 rows), `before` (the old play table), `play_final` (every play-table state, both sizes), `focus`.

## Not verified, and open questions

- **GUI work left undone**: the site's charts and replay viewer still use inline `style=` attributes (fine without a
  CSP, but they block a strict one); the play server sends fonts with `no-store`; the last two table fixes (the
  idle dock line following the phase, and the Grimoire's character label) were checked in isolation and by tests,
  not in a fresh full game.
- **Never built with the real logs** (no HF token here): real model games in the viewer, reasoning summaries, the
  belief table, highlights and their jump links have not been seen in this design. Practice games have no reasoning
  or belief probes.
- **Play table only against practice bots**: real-model latency, the own-key flow (needs a key), the paused/resume
  screen after a restart, and the free-budget messages were not exercised.
- Tested in Chromium only (Playwright, with phone emulation). Not on real iOS Safari or Android Chrome, and not with
  a screen reader.
- `playUrl` points at the old free Render service (`clocktower-ogul.onrender.com`), which `docs/hosting.md` says can
  be deleted once `play.clocktowerbench.com` runs. Point it at the new host before launch, or decide whether the
  Render URL should be public at all.
- Fonts are subsets (Latin). Names typed in other scripts fall back to system fonts, which is fine but looks different.
- Image the redesign would still like (not made; the generation budget is spent): a dark, quiet second plate for the
  play lobby, for example the town square at night from street level with no figures, so the lobby can carry a
  little atmosphere without competing with its forms.
