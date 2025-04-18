import os
from elevenlabs.client import ElevenLabs

# 1) Clé API
api_key = os.getenv("ELEVENLABS_API_KEY")
if not api_key:
    raise RuntimeError("🛑 Définissez ELEVENLABS_API_KEY")

# 2) Instanciation du client
client = ElevenLabs(api_key=api_key)

# 3) Lecture du script généré
with open("voice_script.txt", encoding="utf-8") as f:
    voice_text = f.read()

# 4) Génération du flux audio
audio_stream = client.text_to_speech.convert(
    text=voice_text,
    voice_id="scVxIdZxHu0JOphTmu0x",
    model_id="eleven_multilingual_v2",
    output_format="mp3_44100_128",
    voice_settings={                        # reproduit les réglages UI
        "stability": 0.50,                  # 0 à 1, copie depuis l’UI
        "similarity_boost": 0.75            # 0 à 1, idem
    }
)

# 5) Écriture du MP3
with open("voice.mp3", "wb") as f:
    for chunk in audio_stream:
        f.write(chunk)

print("✅ Génération audio terminée : voice.mp3")
