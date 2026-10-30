"""Upload rendered files to the HF dataset under media/stream/<basename>:  python3 -m stream.hf_upload FILE..."""
import subprocess, sys
from pathlib import Path

for f in sys.argv[1:]:
    p = Path(f)
    r = subprocess.run(["hf", "upload", "dwarkesh/clocktower-games", str(p), f"media/stream/{p.name}", "--repo-type", "dataset"],
                       capture_output=True, text=True)
    print(p.name, "ok" if r.returncode == 0 else "FAILED " + r.stderr[-300:], flush=True)
