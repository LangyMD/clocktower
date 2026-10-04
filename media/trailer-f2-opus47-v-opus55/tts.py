import json, base64, os, sys, urllib.request, subprocess
D = os.path.dirname(os.path.abspath(__file__))
FF = "/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2"
V = {"NARR": "JBFqnCBsd6RMkjVDRZzb",   # George
     "JULES": "N2lVS1w4EtoT3dr4eOWO",  # Callum
     "BLAIR": "pFZP5JQG7iQjIQuC4Bku",  # Lily
     "HARPER": "EXAVITQu4vr4xnSDxMaL", # Sarah
     "ALEX": "iP95p4xoKVk53GoZ742B"}   # Chris
CLIPS = json.load(open(os.path.join(D, "script.json")))
only = set(sys.argv[1:])
for c in CLIPS:
    cid, who, text = c["id"], c["voice"], c["tts"]
    out = os.path.join(D, "audio2", cid + ".mp3")
    if os.path.exists(out) and cid not in only: continue
    body = json.dumps({"text": text, "model_id": "eleven_v4", "voice_settings": {"speed": c.get("speed", 1.0)}}).encode()
    req = urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{V[who]}/with-timestamps?output_format=mp3_44100_128",
        data=body, headers={"xi-api-key": os.environ["ELEVENLABS_API_KEY"], "Content-Type": "application/json"})
    d = json.load(urllib.request.urlopen(req))
    open(out, "wb").write(base64.b64decode(d["audio_base64"]))
    json.dump(d["alignment"], open(out.replace(".mp3", ".align.json"), "w"))
    print("made", cid)
for c in CLIPS:
    out = os.path.join(D, "audio2", c["id"] + ".mp3")
    p = subprocess.run([FF, "-i", out, "-f", "null", "-"], capture_output=True, text=True).stderr
    dur = [l for l in p.splitlines() if "time=" in l][-1].split("time=")[1].split()[0]
    print(c["id"], c["voice"], dur, c["tts"][:70])
