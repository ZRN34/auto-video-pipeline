#!/usr/bin/env python3
import os, subprocess, sys

# 1) Fichier à pousser
AUDIO_FILE = "voice.mp3"

# 2) URL du dépôt avec token (à définir en variable d’environnement)
GITHUB_REPO_URL = os.getenv("GITHUB_REPO_URL")

if not GITHUB_REPO_URL:
    print("🛑 Définissez la variable GITHUB_REPO_URL (https://TOKEN@github.com/…/auto-video-pipeline.git)")
    sys.exit(1)

# 3) Vérifie que le fichier existe
if not os.path.exists(AUDIO_FILE):
    print(f"❌ Fichier introuvable : {AUDIO_FILE}")
    sys.exit(1)

# 4) Configure la remote pour utiliser le token
subprocess.run(["git", "remote", "set-url", "origin", GITHUB_REPO_URL], check=True)

# 5) Ajoute, commit et push
subprocess.run(["git", "add", "-f", AUDIO_FILE], check=True)
subprocess.run(["git", "commit", "-m", f"🔊 Ajout automatique de {AUDIO_FILE}"], check=True)
subprocess.run(["git", "push", "origin", "main"], check=True)

print(f"✅ {AUDIO_FILE} poussé sur GitHub")
