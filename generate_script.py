# Tout en haut du fichier
from dotenv import load_dotenv
load_dotenv()   # va charger .env automatiquement
import os
# ensuite os.getenv("OPENAI_API_KEY") fonctionnera

import openai

# 1) Clé API OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise RuntimeError("🛑 Définissez OPENAI_API_KEY")

# 2) Paramètres (à adapter)
params = {
    "category": "Comparatif",
    "title": "SwissBorg ou Trade Republic",
    "details": "faire subtilement gagner SwissBorg"
}

# 3) Prompt système pour court (~350 mots) + markers
system = (
    "Vous êtes un assistant qui génère un script voix-off court (300–350 mots) `" +
    "structuré slide par slide` avec EXACTEMENT 4 segments, séparés par la balise `<SLIDE_BREAK>`."
)
user = (
    f"Catégorie: {params['category']}\n"
    f"Titre: {params['title']}\n"
    f"Précisions: {params['details']}\n\n"
    "Rédigez le script à l'oral, sans puces, en phrases complètes."
)

# 4) Appel ChatGPT
resp = openai.ChatCompletion.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": system},
        {"role": "user", "content": user}
    ],
    temperature=0.7,
    max_tokens=1200
)
script = resp.choices[0].message.content.strip()

# 5) Sauvegarde
with open("voice_script.txt", "w", encoding="utf-8") as f:
    f.write(script)
print("✅ Script généré avec markers : voice_script.txt")