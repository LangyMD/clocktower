"""ElevenLabs TTS for every clip in clips.json (cached by id+text)."""
import json, base64, os, sys, urllib.request, hashlib
from concurrent.futures import ThreadPoolExecutor
D = os.path.dirname(os.path.abspath(__file__))
os.makedirs(os.path.join(D, "audio"), exist_ok=True)
CLIPS = json.load(open(os.path.join(D, "clips.json")))
def make(c):
    key = hashlib.sha1(json.dumps(c, sort_keys=True).encode()).hexdigest()[:10]
    out = os.path.join(D, "audio", c["id"] + ".mp3"); tag = out + ".key"
    if os.path.exists(out) and os.path.exists(tag) and open(tag).read() == key: return None
    body = json.dumps({"text": c["tts"], "model_id": "eleven_v4", "voice_settings": {"speed": c.get("speed", 1.0)}}).encode()
    req = urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{c['voice']}/with-timestamps?output_format=mp3_44100_128",
        data=body, headers={"xi-api-key": os.environ["ELEVENLABS_API_KEY"], "Content-Type": "application/json"})
    for i in range(4):
        try: d = json.load(urllib.request.urlopen(req, timeout=120)); break
        except Exception as e:
            err = e; import time; time.sleep(2 ** i)
    else: return f"{c['id']} FAILED {err}"
    open(out, "wb").write(base64.b64decode(d["audio_base64"])); open(tag, "w").write(key)
    return "made " + c["id"]
with ThreadPoolExecutor(4) as ex:
    for r in ex.map(make, CLIPS):
        if r: print(r)
