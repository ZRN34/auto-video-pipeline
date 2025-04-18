#!/usr/bin/env python3
import subprocess
import sys
import os

# On utilise le même interpréteur Python que celui qui lance ce script
PYTHON = sys.executable

# Liste des scripts à exécuter dans l'ordre
STEPS = [
    "generate_script.py",          # génère voice_script.txt
    "generate_slides.py",          # génère slides.pptx
    "export_slides.py",            # exporte les slides en images
    "generate_audio_segments.py",  # segmente et génère audio1.mp3, audio2.mp3, ...
    "make_slides_video.py",        # crée slides_video.mp4 (slides+audio)
    "generate_avatar.py",          # compose slides_video.mp4 + avatar.mp4 → final_video.mp4
]

def run_step(script_name):
    print(f"\n➡️ Lancement de {script_name} avec {PYTHON}")
    try:
        subprocess.run([PYTHON, script_name], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Échec de {script_name} (code {e.returncode})")
        sys.exit(1)

def main():
    # Vérifie qu'on est bien dans le bon dossier
    for step in STEPS:
        if not os.path.exists(step):
            print(f"❌ Fichier introuvable : {step}")
            sys.exit(1)

    # Exécution séquentielle
    for step in STEPS:
        run_step(step)

    print("\n🎉 Pipeline terminé avec succès ! Le fichier final est `final_video.mp4`")

if __name__ == "__main__":
    main()
