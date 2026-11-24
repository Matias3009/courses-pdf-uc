# Árbol de prerrequisitos UC

```bash
pip install requests beautifulsoup4        # + pypdf si usas --pdf
python uc_prereqs.py                       # descarga requisitos y abre uc_prereqs.html
```

- `python uc_prereqs.py --tree IIC2154 --program M296` → árbol en la terminal
- `python uc_prereqs.py --list` → programas disponibles (majors, tracks, minors)
- `python uc_prereqs.py --extra IIC3633` → agregar cursos sueltos
- `python uc_prereqs.py --pdf malla.pdf --pdf-name "Mi Major"` → programa desde otro PDF
- `--offline` usa solo las cachés, `--refresh` vuelve a descargar todo, `--no-info` omite nombres/créditos/descripciones.

En el HTML: elige Major/Track y Minor, luego un curso. Clic = marcar aprobado,
doble clic = enfocar ese curso. Cada área del plan (p. ej. "1.1 Ciencias básicas (mínimos)")
se dibuja como un recuadro con los créditos que exige y los que llevas aprobados; cada curso
muestra sus créditos. Al pasar el mouse aparece el nombre completo, créditos y una descripción breve.

Fuentes: prerrequisitos y descripción desde catalogo.uc.cl, nombre completo y créditos desde
buscacursos.uc.cl (prueba 2026-2, 2026-1, 2025-2, 2025-1). Las mallas y créditos por área
están en `programs.py`.
