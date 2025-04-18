import moviepy
import pkgutil
import os

print("moviepy module file :", moviepy.__file__)
print("moviepy package path:", moviepy.__path__)
print("Contenu du dossier moviepy :")
for _, name, ispkg in pkgutil.iter_modules(moviepy.__path__):
    print("  ", ("[pkg]" if ispkg else "[mod]"), name)

# Essayons d'importer directement moviepy
try:
    import moviepy.editor
    print("→ moviepy.editor import OK")
except Exception as e:
    print("→ Erreur import moviepy.editor:", repr(e))
