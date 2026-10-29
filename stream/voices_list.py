"""Print the ElevenLabs quota and the voices this key can use (to pick stream voices)."""
import json, os, urllib.request
H = {"xi-api-key": os.environ["ELEVENLABS_API_KEY"]}
get = lambda u: json.load(urllib.request.urlopen(urllib.request.Request("https://api.elevenlabs.io" + u, headers=H)))
s = get("/v1/user/subscription")
print({k: s.get(k) for k in ("tier", "character_count", "character_limit", "next_character_count_reset_unix")})
for x in get("/v1/voices")["voices"]:
    lab = x.get("labels") or {}
    print(x["voice_id"], x["name"], x.get("category"), lab.get("gender"), lab.get("accent"), lab.get("age"),
          lab.get("descriptive") or lab.get("description"))
