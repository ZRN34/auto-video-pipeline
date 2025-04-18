import os
import comtypes.client

# 1) Détection du fichier PPTX généré
pptx_files = [f for f in os.listdir('.') if f.lower().endswith('.pptx')]
if not pptx_files:
    raise FileNotFoundError("Aucun fichier .pptx trouvé dans le dossier.")
pptx_path = os.path.abspath(pptx_files[0])

# 2) Dossier de sortie
out_dir = 'slides_images'
os.makedirs(out_dir, exist_ok=True)

# 3) Lancer PowerPoint en arrière-plan (fenêtre visible par défaut)
powerpoint = comtypes.client.CreateObject("PowerPoint.Application")
# note: ne pas cacher la fenêtre sinon COM peut échouer
presentation = powerpoint.Presentations.Open(pptx_path, WithWindow=False)

# 4) Exporter chaque slide en PNG
for i, slide in enumerate(presentation.Slides, start=1):
    # Chemin absolu pour éviter les erreurs COM
    out_path = os.path.abspath(os.path.join(out_dir, f"slide{i}.png"))
    slide.Export(out_path, "PNG")
    print(f"✅ Slide {i} exportée → {out_path}")

# 5) Fermer PowerPoint
presentation.Close()
powerpoint.Quit()