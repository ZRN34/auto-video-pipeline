import subprocess
from pathlib import Path

# Réglages vidéo
SLIDE_DIR = Path("slides_images")
OUT_DIR   = Path("temp_slides")    # dossier temporaire pour les segments
FINAL     = "slides_video.mp4"
WIDTH     = 1280
HEIGHT    = 720

# 1) Préparez le dossier temporaire
OUT_DIR.mkdir(exist_ok=True)

# 2) Générez un segment par slide + audio correspondant
slide_files = sorted(SLIDE_DIR.glob("slide*.png"))

for idx, slide in enumerate(slide_files, start=1):
    audio = Path(f"audio{idx}.mp3")
    if not audio.exists():
        print(f"⚠️ Pas d’audio pour {slide.name}, passage au suivant.")
        continue

    out_segment = OUT_DIR / f"segment{idx}.mp4"

    # Récupérez la durée de l'audio
    cmd_probe = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(audio)
    ]
    duration = float(subprocess.check_output(cmd_probe).strip())

    # Créez la vidéo figée pour la durée de l'audio
    cmd_ffmpeg = [
        "ffmpeg", "-y",
        "-loop", "1", "-i", str(slide),
        "-i", str(audio),
        "-c:v", "libx264",
        "-t", str(duration),
        "-pix_fmt", "yuv420p",
        "-vf", f"scale={WIDTH}:{HEIGHT}",
        "-c:a", "aac",
        "-shortest",
        str(out_segment)
    ]
    print(f"▶️ Génération segment {idx} pour {slide.name}…")
    subprocess.run(cmd_ffmpeg, check=True)

# 3) Préparez la liste pour concaténation
list_txt = OUT_DIR / "list.txt"
segment_files = sorted(OUT_DIR.glob("segment*.mp4"))

with open(list_txt, "w") as f:
    for seg in segment_files:
        # notez bien le chemin relatif ou absolu selon besoin
        f.write(f"file '{seg.name}'\n")

# 4) Concaténez tous les segments en un MP4 final
cmd_concat = [
    "ffmpeg", "-y",
    "-f", "concat",
    "-safe", "0",
    "-i", str(list_txt),
    "-c", "copy",
    FINAL
]
print("🔗 Concaténation en", FINAL, "…")
subprocess.run(cmd_concat, check=True)

# 5) (Optionnel) Nettoyage du dossier temporaire
# import shutil
# shutil.rmtree(OUT_DIR)

print("✅ slides_video.mp4 généré !")
