# Árbol de prerrequisitos UC

```bash
pip install requests beautifulsoup4        # + pypdf si usas --pdf
python uc_prereqs.py                       # descarga requisitos y abre uc_prereqs.html
```

- `python uc_prereqs.py --tree IIC2154 --program M296` → árbol en la terminal
- `python uc_prereqs.py --list` → programas disponibles (majors, tracks, minors)
- `python uc_prereqs.py --extra IIC3633` → agregar cursos sueltos
- `python uc_prereqs.py --pdf malla.pdf --pdf-name "Mi Major"` → programa desde otro PDF
- `--offline` usa solo `prereq_cache.json`, `--refresh` vuelve a descargar todo.

En el HTML: elige Major/Track y Minor, luego un curso. Clic = marcar aprobado,
doble clic = enfocar ese curso. Las mallas están en `programs.py`.
