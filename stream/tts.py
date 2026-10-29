"""ElevenLabs TTS (eleven_v4, character timestamps), cached by voice + text in stream/cache/tts/.

Every narrator line and quoted player line goes through `speak_all`; a line already in the cache costs nothing,
so shared lines (the rules primer, between-game cards, stock phrases) are paid for once.
"""
import base64, hashlib, json, os, time, urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

CACHE = Path(__file__).resolve().parent / "cache" / "tts"
MODEL = "eleven_v4"
NARRATOR = "JBFqnCBsd6RMkjVDRZzb"          # George: warm, captivating storyteller (British)
SEAT_VOICES = {                            # one fixed voice per seat name, the same in every episode
    "Alex": "bIHbv24MWmeRgasZH58o",      # Will
    "Blair": "pFZP5JQG7iQjIQuC4Bku",     # Lily
    "Casey": "EXAVITQu4vr4xnSDxMaL",     # Sarah
    "Drew": "IKne3meq5aSn9XLyUdCD",      # Charlie
    "Ellis": "CwhRBWXzGAHq8TQ4Fs17",     # Roger
    "Frankie": "FGY2WhTYpPnrIDTdsKH5",   # Laura
    "Gray": "pqHfZKP75CvOlQylNhV4",      # Bill
    "Harper": "Xb7hH8MSUJpSbSDYk0k2",    # Alice
    "Indigo": "cgSgspJ2msm6clMCkdW9",    # Jessica
    "Jules": "N2lVS1w4EtoT3dr4eOWO",     # Callum
    "Kit": "XrExE9yKIg1WjnnlVkGX",       # Matilda
    "Logan": "nPczCjzI2devNBz1zQrb",     # Brian
}
SPEED = {"N": 1.0}


def voice_of(who):
    return NARRATOR if who == "N" else SEAT_VOICES.get(who, "SAz9YHcvj6GT2YYXdXww")


def key(who, text):
    return hashlib.sha1(json.dumps([MODEL, voice_of(who), text, SPEED.get(who, 1.0)]).encode()).hexdigest()[:16]


def path(who, text):
    k = key(who, text)
    return CACHE / f"{k}.mp3", CACHE / f"{k}.json"


def _make(item):
    who, text = item
    mp3, meta = path(who, text)
    if meta.exists():
        return 0
    body = json.dumps({"text": text, "model_id": MODEL, "voice_settings": {"speed": SPEED.get(who, 1.0)}}).encode()
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice_of(who)}/with-timestamps?output_format=mp3_44100_128",
        data=body, headers={"xi-api-key": os.environ["ELEVENLABS_API_KEY"], "Content-Type": "application/json"})
    err = None
    for i in range(9):
        try:
            d = json.load(urllib.request.urlopen(req, timeout=180)); break
        except Exception as e:
            err = e; time.sleep(min(3 * 2 ** i, 60))
    else:
        raise RuntimeError(f"TTS failed for {who}: {text[:60]!r}: {err}")
    mp3.write_bytes(base64.b64decode(d["audio_base64"]))
    json.dump({"who": who, "text": text, "alignment": d.get("alignment")}, open(meta, "w"))
    return len(text)


def speak_all(items, workers=2):
    """items: [(who, text)] -> characters newly synthesised."""
    CACHE.mkdir(parents=True, exist_ok=True)
    items = list(dict.fromkeys(items))
    with ThreadPoolExecutor(workers) as ex:
        return sum(ex.map(_make, items))
