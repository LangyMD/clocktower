"""ElevenLabs TTS (eleven_v4, with character timestamps) for every clip in clips.json; cached by text+voice."""
import json, base64, os, urllib.request, hashlib, time
from concurrent.futures import ThreadPoolExecutor
D = os.path.dirname(os.path.abspath(__file__))
os.makedirs(os.path.join(D, "audio"), exist_ok=True)
CLIPS = json.load(open(os.path.join(D, "clips.json")))

def make(c):
    key = hashlib.sha1(json.dumps([c["voice"], c["tts"], c["speed"]]).encode()).hexdigest()[:10]
    out = os.path.join(D, "audio", c["id"] + ".mp3"); meta = os.path.join(D, "audio", c["id"] + ".json")
    if os.path.exists(meta) and json.load(open(meta)).get("key") == key: return None
    body = json.dumps({"text": c["tts"], "model_id": "eleven_v4", "voice_settings": {"speed": c["speed"]}}).encode()
    req = urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{c['voice']}/with-timestamps?output_format=mp3_44100_128",
        data=body, headers={"xi-api-key": os.environ["ELEVENLABS_API_KEY"], "Content-Type": "application/json"})
    for i in range(4):
        try: d = json.load(urllib.request.urlopen(req, timeout=120)); break
        except Exception as e: err = e; time.sleep(2 ** i)
    else: return f"{c['id']} FAILED {err}"
    open(out, "wb").write(base64.b64decode(d["audio_base64"]))
    json.dump({"key": key, "alignment": d.get("alignment"), "normalized": d.get("normalized_alignment")}, open(meta, "w"))
    return "made " + c["id"]

with ThreadPoolExecutor(4) as ex:
    for r in ex.map(make, CLIPS):
        if r: print(r)
