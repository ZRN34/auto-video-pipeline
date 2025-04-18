# Tout en haut du fichier
from dotenv import load_dotenv
load_dotenv()   # va charger .env automatiquement
import os
# ensuite os.getenv("OPENAI_API_KEY") fonctionnera
from elevenlabs.client import ElevenLabs

# Clé API
api_key = os.getenv('ELEVENLABS_API_KEY')
if not api_key:
    raise RuntimeError('🛑 Définissez ELEVENLABS_API_KEY')
client = ElevenLabs(api_key=api_key)

# Lecture et découpage
text = open('voice_script.txt', encoding='utf-8').read()
segments = text.split('<SLIDE_BREAK>')

audio_paths = []
for i, seg in enumerate(segments, start=1):
    seg = seg.strip()
    if not seg: continue
    stream = client.text_to_speech.convert(
        text=seg,
        voice_id='scVxIdZxHu0JOphTmu0x',
        model_id='eleven_multilingual_v2',
        output_format='mp3_44100_128'
    )
    out = f'audio{i}.mp3'
    with open(out, 'wb') as f:
        for chunk in stream: f.write(chunk)
    audio_paths.append(out)
    print(f'✅ Généré: {out}')