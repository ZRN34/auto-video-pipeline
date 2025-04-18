import os
import time
import json
import requests

# 1) Variables à personnaliser
HEYGEN_API_KEY = os.getenv("HEYGEN_API_KEY")
AVATAR_ID = "Luca_public"         # remplacez par l'ID de votre avatar
AUDIO_FILE = "voice.mp3"          # le MP3 généré par ElevenLabs
AUDIO_URL = "https://raw.githubusercontent.com/ZRN34/auto-video-pipeline/main/voice.mp3"  # Remplacez par l'URL publique de votre fichier audio
VIDEO_FILE_NAME = "avatar_video.mp4"  # Nom du fichier vidéo final

if not HEYGEN_API_KEY:
    raise RuntimeError("🛑 Définissez HEYGEN_API_KEY dans votre environnement")

# Vérifier si le fichier audio existe localement
if not os.path.exists(AUDIO_FILE):
    raise FileNotFoundError(f"🛑 Le fichier audio {AUDIO_FILE} est introuvable.")

headers = {"X-Api-Key": HEYGEN_API_KEY, "Content-Type": "application/json"}

# 2) Génération de la vidéo avec `audio_url`
print("➡️ Génération de l’avatar vidéo avec HeyGen…")
generate_video_url = "https://api.heygen.com/v2/video/generate"
payload = {
    "video_inputs": [
        {
            "character": {
                "type": "avatar",
                "avatar_id": AVATAR_ID,
                "avatar_style": "normal"
            },
            "voice": {
                "type": "audio",
                "audio_url": AUDIO_URL  # Utilisation de l'URL publique du fichier audio
            },
            "background": {
                "type": "color",
                "value": "#008000"  # Exemple de fond vert
            }
        }
    ],
    "dimension": {"width": 1280, "height": 720}
}

try:
    resp = requests.post(
        generate_video_url,
        headers=headers,
        data=json.dumps(payload)
    )

    if resp.status_code != 200:
        print(f"Erreur lors de la génération de la vidéo : {resp.status_code}")
        print(f"Message d'erreur : {resp.text}")
        raise RuntimeError("Échec de la génération vidéo.")

    resp.raise_for_status()
    video_id = resp.json()["data"]["video_id"]
    print(f"✅ Vidéo générée avec succès, video_id = {video_id}")

except requests.exceptions.RequestException as e:
    print(f"Erreur de requête : {e}")
    raise RuntimeError("Une erreur est survenue lors de la génération de la vidéo.")

# 3) Vérification du statut de la vidéo
print("➡️ Vérification du statut de la vidéo…")
status_url = f"https://api.heygen.com/v1/video_status.get?video_id={video_id}"

status = None
while status != "completed":
    time.sleep(5)
    resp = requests.get(status_url, headers=headers)
    resp.raise_for_status()
    data = resp.json()["data"]
    status = data["status"]
    print(f"  • Statut actuel : {status}")
    if status == "failed":
        error_message = data.get("error", "Aucun message d'erreur détaillé disponible.")
        print(f"❌ Génération de la vidéo échouée. Message d'erreur : {error_message}")
        raise RuntimeError("❌ Génération de la vidéo échouée.")

# 4) Téléchargement de la vidéo générée
video_url = data["video_url"]
print(f"🔗 Téléchargement de la vidéo depuis : {video_url}")
video_data = requests.get(video_url).content
with open(VIDEO_FILE_NAME, "wb") as f:
    f.write(video_data)
print(f"✅ Vidéo téléchargée avec succès : {VIDEO_FILE_NAME}")