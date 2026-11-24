# Árbol de prerrequisitos UC

Programa en Python que descarga los prerrequisitos de los cursos de Ingeniería UC
(catalogo.uc.cl) y genera una página web interactiva (`uc_prereqs.html`) para ver qué
cursos necesitas para tomar otros, cuánto llevas aprobado y qué major/minor te conviene.

Majors incluidos: Computación (Track Computación y Track Sistemas de Información),
Ingeniería de Software, Eléctrica, Robótica, Diseño e Innovación, Biomédica (Track General
y Track Premedicina), Ingeniería Matemática, además de sus minors de profundidad y todos los
Minors de Amplitud.

## Qué necesitas

- **Python 3.9 o más nuevo**
- Las librerías `requests` y `beautifulsoup4` (y `pypdf` solo si usas `--pdf`)
- **git** (o descargar el ZIP desde GitHub: botón verde *Code → Download ZIP*)
- Conexión a internet (la primera vez descarga todo; después usa la caché)

En todos los sistemas se recomienda un **entorno virtual** (`venv`), así las librerías
quedan dentro de la carpeta del proyecto y no tocan el Python del sistema.

---

## macOS

1. Instala Python y git. Con [Homebrew](https://brew.sh):
   ```bash
   brew install python git
   ```
   (Sin Homebrew: instala Python desde https://www.python.org/downloads/macos/ ; git viene
   con las *Command Line Tools*, se instalan con `xcode-select --install`.)
2. Descarga el proyecto y entra a la carpeta:
   ```bash
   git clone https://github.com/Matias3009/courses-pdf-uc.git
   cd courses-pdf-uc
   ```
3. Crea el entorno virtual e instala las librerías:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install requests beautifulsoup4 pypdf
   ```
4. Ejecuta:
   ```bash
   python3 uc_prereqs.py
   ```
   Se abre la página en tu navegador.

## Windows

1. Instala Python y git. En **PowerShell**:
   ```powershell
   winget install Python.Python.3.12 Git.Git
   ```
   (O descárgalos desde https://www.python.org/downloads/windows/ — marca
   **"Add python.exe to PATH"** — y https://git-scm.com/download/win.)
   Cierra y vuelve a abrir PowerShell después de instalar.
2. Descarga el proyecto:
   ```powershell
   git clone https://github.com/Matias3009/courses-pdf-uc.git
   cd courses-pdf-uc
   ```
3. Crea el entorno virtual e instala las librerías:
   ```powershell
   py -m venv .venv
   .venv\Scripts\Activate.ps1
   pip install requests beautifulsoup4 pypdf
   ```
   Si PowerShell dice que *la ejecución de scripts está deshabilitada*, ejecuta una vez
   `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` y repite el comando de activación.
   (En `cmd.exe` se activa con `.venv\Scripts\activate.bat`.)
4. Ejecuta:
   ```powershell
   py uc_prereqs.py
   ```

## Linux — Debian / Ubuntu

1. Instala lo necesario:
   ```bash
   sudo apt update
   sudo apt install python3 python3-venv python3-pip git
   ```
2. Descarga el proyecto:
   ```bash
   git clone https://github.com/Matias3009/courses-pdf-uc.git
   cd courses-pdf-uc
   ```
3. Entorno virtual y librerías (Debian 12+ no deja usar `pip` fuera de un venv):
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install requests beautifulsoup4 pypdf
   ```
   Alternativa sin venv, con los paquetes de Debian:
   `sudo apt install python3-requests python3-bs4 python3-pypdf`
4. Ejecuta:
   ```bash
   python3 uc_prereqs.py
   ```

## Linux — Gentoo

1. Instala lo necesario con Portage:
   ```bash
   sudo emerge --ask dev-lang/python dev-vcs/git
   ```
   Para usar las librerías del sistema en vez de un venv:
   `sudo emerge --ask dev-python/requests dev-python/beautifulsoup4 dev-python/pypdf`
2. Descarga el proyecto:
   ```bash
   git clone https://github.com/Matias3009/courses-pdf-uc.git
   cd courses-pdf-uc
   ```
3. Entorno virtual (si no instalaste las librerías con `emerge`):
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install requests beautifulsoup4 pypdf
   ```
4. Ejecuta:
   ```bash
   python3 uc_prereqs.py
   ```

## OpenBSD

Funciona: el programa es Python puro y solo necesita un navegador para ver el resultado.

1. Instala los paquetes (como root o con `doas`):
   ```sh
   doas pkg_add python%3 git py3-requests py3-beautifulsoup4
   ```
   `pypdf` solo hace falta para `--pdf`; si no está en los paquetes de tu versión,
   instálalo en un venv (`python3 -m venv .venv && . .venv/bin/activate && pip install pypdf`).
2. Descarga el proyecto:
   ```sh
   git clone https://github.com/Matias3009/courses-pdf-uc.git
   cd courses-pdf-uc
   ```
3. Ejecuta. Si no se abre el navegador solo, usa `--no-open` y ábrelo tú:
   ```sh
   python3 uc_prereqs.py --no-open
   firefox uc_prereqs.html
   ```
   (Instala Firefox con `doas pkg_add firefox` si no lo tienes.)

---

## Uso

La próxima vez que lo uses, entra a la carpeta y activa el entorno virtual
(`source .venv/bin/activate` en macOS/Linux/OpenBSD, `.venv\Scripts\Activate.ps1` en
Windows) antes de ejecutarlo. En Windows usa `py` donde aquí dice `python3`.

| Comando | Qué hace |
|---|---|
| `python3 uc_prereqs.py` | Descarga todo (la primera vez tarda unos minutos) y abre la página |
| `python3 uc_prereqs.py --offline` | Usa solo lo ya descargado (sin internet) |
| `python3 uc_prereqs.py --refresh` | Vuelve a descargar todo |
| `python3 uc_prereqs.py --no-info` | No busca nombres, créditos ni descripciones |
| `python3 uc_prereqs.py --tree IIC2154 --program M296` | Árbol de un curso en la terminal |
| `python3 uc_prereqs.py --list` | Lista los majors y minors disponibles |
| `python3 uc_prereqs.py --extra IIC3633` | Agrega cursos sueltos |
| `python3 uc_prereqs.py --pdf malla.pdf --pdf-name "Mi Major"` | Agrega un programa desde otro PDF |
| `python3 uc_prereqs.py --no-open` | Genera la página sin abrir el navegador |

### En la página

- Elige **Major/Track** y **Minor**. Cada opción muestra cuántos de los créditos necesarios
  llevas aprobados; ⭐ marca la mejor opción.
- **📊 Comparar majors y minors**: tabla con todos los majors, el minor que más te conviene en
  cada uno, créditos aprobados (plan común, major, minor), semestres mínimos que te faltan
  (la cadena de prerrequisitos más larga) y cuántos cursos puedes tomar ahora.
- **Máx. créditos por semestre** (por defecto 60, una carga completa; el tope oficial es 65):
  los semestres restantes son el mayor entre *créditos que faltan ÷ ese máximo* y la cadena de
  prerrequisitos más larga que te falta (un correquisito no suma semestre).
- **Clic** en un curso = marcarlo como aprobado (verde). Los que ya puedes tomar se ven en azul.
  Los aprobados se guardan en tu navegador.
- **Doble clic** = ver solo el árbol de ese curso.
- Un curso que pertenece a varias secciones aparece en cada una, marcado con un **asterisco azul (*)**.
  Al aprobar una copia se aprueban todas. Aprobarlo **cumple el requisito en todas las secciones**,
  pero **sus créditos cuentan una sola vez** hacia el total (primero en los mínimos). El cupo de
  créditos de las otras secciones queda vacío y hay que rellenarlo con otro curso (otro optativo,
  exploratorio o electivo). Colores de los recuadros:
  - **verde**: requisito y créditos completos;
  - **amarillo**: requisito cumplido, pero faltan créditos (rellena con otro curso);
  - **azul**: todavía no se cumple.
- En el mapa completo las flechas están ocultas: **pasa el mouse** por un curso para ver qué
  necesita y qué desbloquea, con su nombre completo, créditos y una descripción breve.
- Cómo leer las flechas:
  - Todas las flechas que llegan **directo** a un curso son **obligatorias**.
  - **UNO DE** (naranjo): basta con aprobar uno de los cursos que llegan a esa etiqueta.
  - **TODOS** (morado): dentro de una opción, se necesitan todos los cursos que llegan.
  - Línea punteada: correquisito (se puede tomar en el mismo semestre).
- Cada área del plan (p. ej. "1.1 Ciencias básicas (mínimos)") es un recuadro con los créditos
  que exige y los que llevas.

### Fuentes de datos

Prerrequisitos y descripción: catalogo.uc.cl. Nombre completo y créditos: buscacursos.uc.cl
(prueba 2026-2, 2026-1, 2025-2, 2025-1). Mallas y créditos por área: `programs.py`, tomados
de los PDFs oficiales de cada Major. Los electivos de Formación General no se pueden marcar,
así que el % total no llega a 100.

### Problemas comunes

- **`python3` no existe** (Windows): usa `py`.
- **`pip: externally-managed-environment`** (Debian/Ubuntu/Gentoo): activa el venv primero.
- **La página sale vacía**: la página carga la librería del grafo desde internet (unpkg.com);
  ábrela con conexión.
- **Errores 403 al descargar del catálogo**: el sitio de la UC a veces bloquea muchas
  consultas seguidas; espera un rato y ejecuta de nuevo (lo ya descargado queda en caché).
