# clocktowerbench.com

The public website: a static site (plain HTML, CSS and JavaScript, no framework, no server) built by one Python
command from the game logs.

```
site/
  src/layout.html        header, footer and <head>, shared by every page
  src/pages/*.html       one fragment per page (first line: <!-- title | description | nav -->)
  src/assets/            style.css, site.js (shared helpers and charts), one script per page, icon.svg
  src/config.json        the values below; becomes dist/config.js
  content/               highlights.json (curated games), charts.json (blog-figure series), poster.jpg
  deploy/                example CI workflow for GitHub Pages
  dist/                  the build output (git-ignored); this folder is what you deploy
```

Pages: Home (`index.html`), Leaderboard, Games (library), Game (replay viewer, `game.html?g=<id>`), Highlights,
Play, Run your own, About. The header links Leaderboard, Games, Play and About; Highlights is a tab of Games and
Run your own sits under About (all are in the footer).

## Build

The game logs must be on disk (`python -m clocktower fetch v16/f2-* v17/f3* v17/f4-* v17/f5-* v17/b1-* v17/b2-*`, or
point `--games` at a checkout that has them):

```sh
python -m clocktower.export --games games --media media/explainer-three-tricks/explainer-three-tricks.mp4
python -m http.server -d site/dist 8000        # preview at http://localhost:8000
```

- About 30 s; writes `site/dist/` (~67 MB with the 8 MB explainer video; ~58 MB of it is 538 gzipped games).
- `--media` is optional: without it the video plays from the Hugging Face dataset (`explainerFallback`).
- `--pages-only` re-renders pages and assets over an existing build in a second (for design work).
- `--limit 20` builds a quick site with the highlight games plus 20 others.
- The build refuses to write anything that looks like an API key (`export.SECRET`).
- A refit (`python -m clocktower ratings`) updates `docs/plans/f2-ratings.json`; rebuild and the leaderboard follows.

What it writes: `data/ratings.json` (the fit plus head-to-head counts), `data/index.json` (one row per game),
`data/highlights.json` (each highlight's quote located to its day and event, for "jump to the moment"),
`data/charts.json`, and `data/games/<id with / as -->.json.gz`. Game files are gzip; the viewer inflates them with
the browser's `DecompressionStream` (and also accepts them if a host already decoded them).

Which games: every game in the rating fit (`ratings.BATCHES` minus Opus 4.8's v16 games), those 20 Opus 4.8 games
marked "not rated" (one is a highlight), and the mixed-team batches b1 and b2.

## Config (`site/src/config.json`)

| Key | What | Unset |
|---|---|---|
| `domain` | `clocktowerbench.com`; written to `dist/CNAME` and canonical links | no CNAME |
| `youtubeVideoId` | the video essay's YouTube id; embedded on the home page | the animatic still, "coming soon" |
| `videoUrl` | a link to the video essay (defaults to the YouTube watch page when only the id is set) | button shows "(soon)" |
| `youtubeChannelId` | unused since the redesign (the home page has no live-stream slot) | |
| `playUrl` | the hosted play table | Play button shows "(soon)" |
| `postUrl` | the blog post | button shows "(soon)" |
| `githubUrl` | the public repository | GitHub buttons show "(soon)"; footer link hidden |
| `datasetUrl` | the Hugging Face dataset page | footer link hidden |
| `explainerVideo` / `explainerFallback` | MP4 sources for the explainer, tried in order | |
| `gameDataBase` | where per-game files live (default `data/games/`) | |

`gameDataBase` lets you keep the game files off the site: upload `dist/data/games/` to the dataset (e.g.
`hf upload dwarkesh/clocktower-games site/dist/data/games site/games --repo-type dataset`) and set it to
`https://huggingface.co/datasets/dwarkesh/clocktower-games/resolve/main/site/games/`. That needs the dataset to be
public; the site itself then shrinks to ~9 MB.

## Deploy

Both hosts serve `site/dist/` as is. Pages use relative links, so they also work from a sub-path.

**Cloudflare Pages** (recommended: fast, free, no size worries at this scale):

```sh
npx wrangler pages deploy site/dist --project-name clocktowerbench
```

Then in the Cloudflare dashboard: Pages → the project → Custom domains → add `clocktowerbench.com` (and `www`). If
the domain's DNS is on Cloudflare this is one click; otherwise add the CNAME it shows at your registrar.

**GitHub Pages**: either push `dist/` to a `gh-pages` branch
(`git subtree push --prefix site/dist origin gh-pages` after force-adding it, or use `ghp-import -n -p site/dist`),
or build in CI with `site/deploy/github-pages.yml` (copy it to `.github/workflows/`; it downloads the logs from the
dataset, so it needs `HF_TOKEN` as a repository secret while the dataset is private). Then Settings → Pages → custom
domain `clocktowerbench.com`; at the registrar add `A` records to 185.199.108.153, .109.153, .110.153, .111.153
(or a `CNAME` for `www` to `<user>.github.io`). `dist/CNAME` and `dist/.nojekyll` are written by the build.

## Notes

- Look: the video essay's animatic. Night palette, parchment "script sheets" for data, BotC-style wooden tokens
  carrying each lab's logo, role-card panels with gold corners, vs cards for games. One dark theme.
- Fonts: Pirata One (titles only), Jersey 10 (interface, labels, numbers), EB Garamond (reading; the play table's
  text face), from Google Fonts. Backdrops in `src/assets/img/` are the animatic's own pixel-art plates. No
  official Blood on the Clocktower artwork, logos or icons.
- OpenAI models' reasoning is encrypted by their API; the viewer shows only the short summaries the logs hold.
