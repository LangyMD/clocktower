#!/usr/bin/env bash
# Build a clean, single-commit snapshot of this repo for the public GitHub repository.
#
#   scripts/publish_snapshot.sh TARGET_DIR [REF]
#
# Takes the committed tree at REF (default HEAD; uncommitted and untracked files are never included), leaves out
# every path in PUBLISH_EXCLUDE, scans what is left for secrets and private paths, then makes TARGET_DIR a fresh git
# repository with one commit. TARGET_DIR must not exist or be empty. Push it yourself:
#
#   cd TARGET_DIR && git remote add origin git@github.com:OWNER/REPO.git && git push -u origin main
#
# The commit author defaults to this repo's git user; override with SNAPSHOT_AUTHOR="Name <email>".
# Set SNAPSHOT_TEST=1 to also run the unit tests inside the snapshot (needs the dependencies installed).
set -euo pipefail

target=${1:?usage: scripts/publish_snapshot.sh TARGET_DIR [REF]}
ref=${2:-HEAD}
root=$(git rev-parse --show-toplevel)
cd "$root"

if [ -e "$target" ] && [ -n "$(ls -A "$target" 2>/dev/null)" ]; then
  echo "error: $target exists and is not empty" >&2
  exit 1
fi
mkdir -p "$target"
target=$(cd "$target" && pwd)

# 1. The committed tree minus the excluded paths.
excludes=()
while IFS= read -r line; do
  line=${line%%#*}; line=$(echo "$line" | xargs)
  [ -n "$line" ] && excludes+=(":(exclude)$line")
done < PUBLISH_EXCLUDE
git archive --format=tar "$ref" -- . "${excludes[@]}" | tar -x -C "$target"

# 2. Scan for secrets and private details. Any hit stops the publish.
patterns=(
  'sk-ant-[A-Za-z0-9_-]{10,}'            # Anthropic keys
  'sk-(proj-)?[A-Za-z0-9_-]{20,}'        # OpenAI / OpenRouter keys
  'hf_[A-Za-z0-9]{20,}'                  # Hugging Face tokens
  'gh[pousr]_[A-Za-z0-9]{20,}'           # GitHub tokens
  'AKIA[0-9A-Z]{16}'                     # AWS access keys
  'xox[abpr]-[A-Za-z0-9-]{10,}'          # Slack tokens
  '-----BEGIN [A-Z ]*PRIVATE KEY-----'
  'wrkspc_[A-Za-z0-9]{10,}'              # Anthropic workspace ids
  '/home/user/|/root/\.|scratchpad/[0-9a-f-]{20,}'   # local paths from the working machine
)
hits=$(cd "$target" && grep -rInE "$(IFS='|'; echo "${patterns[*]}")" . || true)
for name in ANTHROPIC_API_KEY MY_ANTHROPIC_API_KEY OPENAI_API_KEY OPENROUTER_API_KEY HF_TOKEN ELEVENLABS_API_KEY \
            DATAWRAPPER_API_TOKEN; do
  value=${!name:-}
  if [ ${#value} -ge 12 ] && (cd "$target" && grep -rqF -- "$value" .); then
    hits+=$'\n'"the value of \$$name appears in the snapshot"
  fi
done
if [ -n "$hits" ]; then
  echo "error: possible secrets or private paths in the snapshot:" >&2
  echo "$hits" >&2
  exit 1
fi

# 3. Optionally run the unit tests in the snapshot (no API calls).
if [ "${SNAPSHOT_TEST:-0}" = 1 ]; then
  (cd "$target" && env -u ANTHROPIC_API_KEY -u MY_ANTHROPIC_API_KEY -u OPENAI_API_KEY \
     python -m unittest discover -s tests)
  find "$target" -name __pycache__ -type d -prune -exec rm -rf {} +
fi

# 4. One commit.
author=${SNAPSHOT_AUTHOR:-"$(git config user.name) <$(git config user.email)>"}
source_commit=$(git rev-parse --short "$ref")
git -C "$target" init -q -b main
git -C "$target" add -A
git -C "$target" -c user.name="${author% <*}" -c user.email="$(echo "${author##*<}" | tr -d '>')" \
  commit -q -m "Clocktower: language models play Blood on the Clocktower" --author="$author"
echo "snapshot of $source_commit in $target: $(git -C "$target" ls-files | wc -l) files, $(du -sh --exclude=.git "$target" | cut -f1)"
