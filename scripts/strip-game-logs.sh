#!/bin/bash
# Remove raw game logs from git history (they live in the Hugging Face dataset dwarkesh/clocktower-games,
# with a full-history bundle at backup/clocktower-git-before-rewrite-2026-09-30.bundle). Keeps each game's
# config.json and result.json, *.txt analyses, PROTOCOLS/ledger, and all code. Rewrites and force-pushes
# main and every branch: anyone with a clone should re-clone afterwards.
set -euo pipefail
pip install -q git-filter-repo
rm -rf /tmp/clocktower-strip.git
git clone --mirror https://github.com/dwarkeshsp/clocktower /tmp/clocktower-strip.git
cd /tmp/clocktower-strip.git
git filter-repo --force --filename-callback '
import re
if not re.match(rb"games/(v\d+|logs)/", filename):
    return filename
base = filename.rsplit(b"/", 1)[-1]
return filename if base in (b"config.json", b"result.json") or base.endswith(b".txt") else None
'
git count-objects -vH | grep size-pack
git remote add origin https://github.com/dwarkeshsp/clocktower
git push --force --all origin
