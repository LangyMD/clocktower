"""Game logs live in a private Hugging Face dataset, not in git: `python -m clocktower fetch v9/e1-*`.

GitHub keeps the code and each game's config.json and result.json (enough to recompute win rates and
ratings); the dataset keeps everything (transcripts, events, calls, probes, conversations). Upload a
finished batch with the hf CLI (needs HF_TOKEN):

    hf upload dwarkesh/clocktower-games games/v9/e1-NAME v9/e1-NAME --repo-type dataset
"""
from __future__ import annotations
from pathlib import Path

REPO = 'dwarkesh/clocktower-games'
GAMES = Path(__file__).resolve().parent.parent / 'games'


def fetch(patterns):
    """Download the matching game directories (e.g. 'v9/e1-*') into games/."""
    from huggingface_hub import snapshot_download
    return snapshot_download(REPO, repo_type='dataset', local_dir=GAMES,
                             allow_patterns=[p.rstrip('/') + '/**' for p in patterns])
