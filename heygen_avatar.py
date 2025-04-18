#!/usr/bin/env python3
import os, time, json, requests

HEYGEN_API_KEY  = os.getenv("NjAzNTNjNGM3Y2Q0NDEyZGI3ZWRjZTQ0YmQxNjkyMWEtMTcyNjIxODg4OA==")
AVATAR_ID       = "Luca_public"            # remplace par ton avatar_id
VOICE_MP3_URL   = "https://…/voice.mp3"    # URL publique de ton MP3 ElevenLabs

headers = {
    "X-Api-Key": HEYGEN_API_KEY,
    "Content-Type": "application/json",
}
payload = {
    "video_inputs": [
        {
            "character": {"type":"avatar", "avatar_id":AVATAR_ID},
            "voice":     {"type":"audio",  "audio_url":VOICE_MP3_URL}
        }
    ],
    "dimension": {"width":1280, "height":720}
}

# Lancement de la génération
print("➡️ Génération de l’avatar vidéo chez HeyGen…")
resp = requests.post(
    "https://api.heygen.com/v2/video/generate",
    headers=headers,
    json=payload
)
resp.raise_for_status()
vid = resp.json()["data"]["video_id"]
print("✅ Créé, video_id =", vid)

# Polling jusqu’à completion
status = None
while status != "completed":
    time.sleep(5)
    st = requests.get(
        f"https://api.heygen.com/v2/video/status.get?video_id={vid}",
        headers={"X-Api-Key":HEYGEN_API_KEY}
    ).json()["data"]
    status = st["status"]
    print("  • Statut =", status)
    if status == "failed":
        raise RuntimeError("Avatar vidéo échoué :" + json.dumps(st["error"]))

# Téléchargement
url = st["video_url"]
print("🔗 Téléchargement…")
data = requests.get(url).content
with open("avatar.mp4","wb") as f: f.write(data)
print("✅ avatar.mp4 créé !")
