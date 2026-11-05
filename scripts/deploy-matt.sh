#!/usr/bin/env bash
# Deploy Matt's instances: the static site to Cloudflare Pages (clocktowerbench.pages.dev) and the play server
# to Fly (clocktower-play.fly.dev).
#
#   scripts/deploy-matt.sh              # everything: rebuild the site pages, upload to Pages, fly deploy
#   scripts/deploy-matt.sh site         # only the site (Cloudflare Pages)
#   scripts/deploy-matt.sh play         # only the play server
#   scripts/deploy-matt.sh site --full  # full site build (game logs must be on disk) instead of a pages-only re-render
#   DRY_RUN=1 scripts/deploy-matt.sh    # print the commands instead of running them
#
# Needs: flyctl logged in, and CLOUDFLARE_API_TOKEN in the environment (a token with Pages edit rights).
# CLOUDFLARE_ACCOUNT_ID defaults to Matt's account.
set -euo pipefail
cd "$(dirname "$0")/.."

what=${1:-all}; shift || true
full=0; for a in "$@"; do [ "$a" = "--full" ] && full=1; done
PY=${PY:-$([ -x .venv/bin/python ] && echo .venv/bin/python || echo python3)}
: "${CLOUDFLARE_ACCOUNT_ID:=21de960d9ef60cd76d25cc183e0892e6}"
run() { echo "+ $*"; [ "${DRY_RUN:-0}" = 1 ] || "$@"; }

site() {
  if [ "$full" = 1 ]; then run env PYTHONPATH="$PWD" "$PY" -m clocktower.export --games games
  else run env PYTHONPATH="$PWD" "$PY" -m clocktower.export --pages-only; fi
  [ -n "${CLOUDFLARE_API_TOKEN:-}" ] || { echo "error: CLOUDFLARE_API_TOKEN is not set" >&2; exit 1; }
  ( export CLOUDFLARE_API_TOKEN CLOUDFLARE_ACCOUNT_ID   # exported, not echoed: the token never appears in the output
    run npx -y wrangler@latest pages deploy site/dist --project-name clocktowerbench --branch main --commit-dirty=true )
  [ "${DRY_RUN:-0}" = 1 ] || curl -s -o /dev/null -m 20 -w "clocktowerbench.pages.dev: HTTP %{http_code}\n" https://clocktowerbench.pages.dev/
}

play() {
  run fly deploy --app clocktower-play --yes
  [ "${DRY_RUN:-0}" = 1 ] || { sleep 3; echo -n "clocktower-play.fly.dev/healthz: "; curl -s -m 20 https://clocktower-play.fly.dev/healthz; echo; }
}

case "$what" in
  all) site; play ;;
  site) site ;;
  play) play ;;
  *) echo "usage: $0 [all|site|play] [--full]" >&2; exit 2 ;;
esac
