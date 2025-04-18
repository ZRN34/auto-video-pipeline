import os
import time
import requests

# 1) Récupérer la clé HeyGen
API_KEY = os.getenv("HEYGEN_API_KEY")
if not API_KEY:
    raise RuntimeError("🛑 Définissez HEYGEN_API_KEY comme variable d'environnement")

HEADERS = {
    "X-Api-Key": API_KEY,
    "Content-Type": "application/json"
}

# 2) Lire le script voix-off généré
with open("voice_script.txt", encoding="utf-8") as f:
    script_text = f.read().strip()

# 3) Préparer le payload JSON
payload = {
    "video_inputs": [
        {
            "character": {
                "type": "avatar",
                "avatar_id": "Luca_public",
                "avatar_style": "normal"
            },
            "voice": {
                "type": "text",
                "input_text": script_text,
                # Vous pouvez changer voice_id si vous voulez un autre style de voix HeyGen
                "voice_id": "2d5b0e6cf36f460aa7fc47e3eee4ba54"
            }
        }
    ],
    "dimension": {"width": 1280, "height": 720}
}

# 4) Créer la vidéo
print("➡️ Création de la vidéo chez HeyGen…")
resp = requests.post(
    "https://api.heygen.com/v2/video/generate",
    headers=HEADERS,
    json=payload
)
resp.raise_for_status()
video_id = resp.json()["data"]["video_id"]
print(f"✅ Vidéo créée, ID = {video_id}")

# 5) Polling jusqu'à complétion
# … juste après avoir récupéré `video_id` …
status_url = "https://api.heygen.com/v1/video_status.get"
print("⏳ En attente de la complétion…")
while True:
    r = requests.get(f"{status_url}?video_id={video_id}", headers=HEADERS)
    r.raise_for_status()
    data = r.json().get("data", {})
    status = data.get("status")
    print(f"  • Statut = {status}")
    if status == "completed":
        video_url = data.get("video_url")
        break
    elif status in ("waiting", "pending", "processing"):
        time.sleep(5)
        continue
    elif status == "failed":
        # Afficher le détail de l’erreur
        reason = data.get("fail_reason") or data
        print("❌ Génération HeyGen échouée :", reason)
        raise RuntimeError(f"HeyGen failure: {reason}")
    else:
        raise RuntimeError(f"Statut inattendu HeyGen : {status}")


# 6) Télécharger le mp4 final
print("⬇️ Téléchargement de la vidéo…")
r = requests.get(video_url)
r.raise_for_status()
with open("final.mp4", "wb") as f:
    f.write(r.content)

print("🎉 Vidéo finale enregistrée sous final.mp4")
