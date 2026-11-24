#!/usr/bin/env python3
"""
Árbol de prerrequisitos UC (catalogo.uc.cl).

Descarga la página de requisitos de cada curso
  https://catalogo.uc.cl/index.php?tmpl=component&option=com_catalogo&view=requisitos&sigla=XXX
la interpreta ("(A y B) o C", "X(c)" = correquisito), sigue recursivamente los
prerrequisitos y genera un HTML interactivo con:
  - desplegable de Major/Track y de Minor (mapeados desde los PDFs),
  - desplegable de curso: ver qué necesitas para él o qué desbloquea,
  - clic en un curso = marcarlo como aprobado (verde) -> se resaltan los disponibles.

Uso:
  pip install requests beautifulsoup4            (pypdf solo si usas --pdf)
  python uc_prereqs.py                           # descarga todo y abre uc_prereqs.html
  python uc_prereqs.py --tree IIC2133            # árbol en la terminal
  python uc_prereqs.py --tree IIC2133 --program M296   # árbol sin alternativas ajenas al programa
  python uc_prereqs.py --extra IIC3633 MAT2605   # agregar cursos sueltos
  python uc_prereqs.py --pdf otro_major.pdf --pdf-name "Mi Major"   # programa desde un PDF
  python uc_prereqs.py --offline                 # usar solo la caché
  python uc_prereqs.py --refresh                 # volver a descargar todo
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import threading
import time
import webbrowser
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from programs import NAMES, PROGRAMS, program_courses

HERE = Path(__file__).resolve().parent
CACHE_FILE = HERE / "prereq_cache.json"
URL = ("https://catalogo.uc.cl/index.php?tmpl=component&option=com_catalogo"
       "&view=requisitos&sigla={}")
# El sitio rechaza (403 "Malware detected") peticiones sin cabeceras de navegador.
HEADERS = {
    "User-Agent": ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                   "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"),
    "Accept": "text/html,application/xhtml+xml",
    "Accept-Language": "es-CL,es;q=0.9",
}
SIGLA = r"[A-Z]{3}\d{3,4}[A-Z]?"
SIGLA_RE = re.compile(rf"^{SIGLA}$")


# =============================================================== parsing
def parse_expr(text: str):
    """'(IIC1253 y IIC2233) o MAT1203(c)' -> árbol
    {"op": "or", "args": [{"op": "and", "args": [...]}, {"c": "MAT1203", "co": True}]}
    Devuelve None si no hay prerrequisitos."""
    if not text or "no tiene" in text.lower():
        return None
    text = re.sub(rf"({SIGLA})\s*\(\s*c\s*\)", r"\1#c", text)
    tokens = re.findall(rf"{SIGLA}(?:#c)?|\(|\)|\by\b|\bo\b", text)
    pos = 0

    def peek():
        return tokens[pos] if pos < len(tokens) else None

    def parse_or():
        nonlocal pos
        args = [parse_and()]
        while peek() == "o":
            pos += 1
            args.append(parse_and())
        return mk("or", args)

    def parse_and():
        nonlocal pos
        args = [parse_atom()]
        while peek() == "y":
            pos += 1
            args.append(parse_atom())
        return mk("and", args)

    def parse_atom():
        nonlocal pos
        t = peek()
        if t == "(":
            pos += 1
            e = parse_or()
            if peek() == ")":
                pos += 1
            return e
        pos += 1
        if t and t.endswith("#c"):
            return {"c": t[:-2], "co": True}
        if t and SIGLA_RE.match(t):
            return {"c": t, "co": False}
        return None

    def mk(op, args):
        flat = []
        for a in args:
            if a is None:
                continue
            if a.get("op") == op:
                flat.extend(a["args"])
            else:
                flat.append(a)
        if not flat:
            return None
        return flat[0] if len(flat) == 1 else {"op": op, "args": flat}

    return parse_or() if tokens else None


def leaves(expr):
    if not expr:
        return []
    if "c" in expr:
        return [expr["c"]]
    return [s for a in expr["args"] for s in leaves(a)]


def parse_page(html: str) -> dict:
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    fields = {}
    for tr in soup.find_all("tr"):
        tds = tr.find_all("td")
        if len(tds) < 2:
            continue
        label = " ".join(tds[0].get_text(" ").split()).lower()
        value = " ".join(tds[1].get_text(" ").split())
        if label.startswith("prerrequisito"):
            fields["prereq"] = value
        elif label.startswith("relación") or label.startswith("relacion"):
            fields["relacion"] = value
        elif label.startswith("restriccion"):
            fields["restricciones"] = value
        elif label.startswith("equivalencia"):
            fields["equivalencias"] = value
    if "prereq" not in fields:
        raise ValueError("No se encontró la fila 'Prerrequisitos' (¿sigla inexistente?)")
    fields["expr"] = parse_expr(fields["prereq"])
    return fields


# =============================================================== descarga + caché
class Catalog:
    def __init__(self, offline=False, refresh=False, workers=4, delay=0.25):
        self.offline, self.refresh = offline, refresh
        self.workers, self.delay = workers, delay
        self.data: dict[str, dict] = {}
        if CACHE_FILE.exists():
            try:
                self.data = json.loads(CACHE_FILE.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                pass
        self._fresh: set[str] = set()
        self._lock = threading.Lock()
        self._session = None

    def save(self):
        CACHE_FILE.write_text(json.dumps(self.data, ensure_ascii=False, indent=1), encoding="utf-8")

    def _fetch(self, sigla):
        import requests
        if self._session is None:
            self._session = requests.Session()
            self._session.headers.update(HEADERS)
        last = None
        for attempt in range(3):
            try:
                r = self._session.get(URL.format(sigla), timeout=20)
                if r.status_code == 200:
                    info = parse_page(r.text)
                    time.sleep(self.delay)
                    return info
                last = f"HTTP {r.status_code}"
            except Exception as e:  # noqa: BLE001
                last = str(e)
            time.sleep(1.5 * (attempt + 1))
        return {"error": last, "expr": None, "prereq": ""}

    def get(self, sigla):
        with self._lock:
            have = sigla in self.data and "error" not in self.data[sigla]
            if have and (not self.refresh or sigla in self._fresh):
                return self.data[sigla]
        if self.offline:
            return self.data.get(sigla, {"error": "sin caché (offline)", "expr": None, "prereq": ""})
        info = self._fetch(sigla)
        with self._lock:
            self.data[sigla] = info
            self._fresh.add(sigla)
        return info

    def crawl(self, roots, max_depth=None):
        """BFS por prerrequisitos. max_depth=None -> sin límite."""
        seen = set()
        frontier = [s for s in dict.fromkeys(roots)]
        depth = 0
        while frontier:
            frontier = [s for s in frontier if s not in seen]
            seen.update(frontier)
            todo = [s for s in frontier
                    if self.offline or s not in self.data or "error" in self.data[s]
                    or (self.refresh and s not in self._fresh)]
            if todo and not self.offline:
                print(f"  nivel {depth}: descargando {len(todo)} cursos…", flush=True)
            with ThreadPoolExecutor(self.workers) as ex:
                results = list(ex.map(self.get, frontier))
            self.save()
            depth += 1
            if max_depth is not None and depth > max_depth:
                break
            nxt = []
            for info in results:
                nxt.extend(leaves(info.get("expr")))
            frontier = [s for s in dict.fromkeys(nxt) if s not in seen]
        errors = [s for s in seen if "error" in self.data.get(s, {})]
        if errors:
            print(f"  ⚠ {len(errors)} cursos con error: {', '.join(sorted(errors)[:15])}"
                  + (" …" if len(errors) > 15 else ""))
        return seen


# =============================================================== PDF -> programa
def program_from_pdf(path, name):
    from pypdf import PdfReader
    text = "\n".join(p.extract_text() or "" for p in PdfReader(path).pages)
    siglas = list(dict.fromkeys(re.findall(rf"\b{SIGLA}\b", text)))
    siglas = [s for s in siglas if not s.startswith("VRA")]  # exámenes/requisitos de grado
    return {"name": name, "kind": "major",
            "sections": [(f"Todos los cursos encontrados en {Path(path).name}", "req", siglas)]}


# =============================================================== árbol en terminal
def prune_to_program(expr, prog: set):
    """En cada 'o', si alguna alternativa toca el programa, descarta las que no."""
    if not expr or "c" in expr:
        return expr
    args = [prune_to_program(a, prog) for a in expr["args"]]
    if expr["op"] == "or":
        inside = [a for a in args if set(leaves(a)) & prog]
        if inside:
            args = inside
    return args[0] if len(args) == 1 else {"op": expr["op"], "args": args}


def print_tree(cat: Catalog, root, prog: set | None = None):
    expanded = set()

    def label(s):
        n = NAMES.get(s, "")
        mark = "" if prog is None or s in prog else "  [fuera del programa]"
        return f"{s} {n}".rstrip() + mark

    def walk(expr, prefix, last, stack):
        conn = "└── " if last else "├── "
        if "c" in expr:
            s = expr["c"]
            co = " (correquisito)" if expr["co"] else ""
            info = cat.data.get(s, {})
            sub = info.get("expr")
            if prog is not None:
                sub = prune_to_program(sub, prog)
            if s in stack:
                print(prefix + conn + label(s) + co + "  ↺ ciclo")
                return
            if s in expanded and sub:
                print(prefix + conn + label(s) + co + "  (ver arriba)")
                return
            print(prefix + conn + label(s) + co)
            expanded.add(s)
            if sub:
                walk(sub, prefix + ("    " if last else "│   "), True, stack | {s})
            return
        word = "TODOS (y)" if expr["op"] == "and" else "UNO DE (o)"
        print(prefix + conn + word)
        for i, a in enumerate(expr["args"]):
            walk(a, prefix + ("    " if last else "│   "), i == len(expr["args"]) - 1, stack)

    info = cat.data.get(root, {})
    print(label(root))
    if info.get("error"):
        print(f"  ⚠ {info['error']}")
    expr = info.get("expr")
    if prog is not None:
        expr = prune_to_program(expr, prog)
    if not expr:
        print("  (sin prerrequisitos)")
    else:
        walk(expr, "", True, {root})


# =============================================================== HTML
def build_html(cat: Catalog, programs: dict, out: Path):
    courses = {}
    for s, info in cat.data.items():
        courses[s] = {k: info.get(k) for k in
                      ("prereq", "expr", "relacion", "restricciones", "equivalencias", "error")
                      if info.get(k) is not None}
    progs = {}
    for k, p in programs.items():
        progs[k] = {"name": p["name"], "kind": p["kind"],
                    "for": p.get("for"), "excluded": p.get("excluded"),
                    "sections": [{"title": t, "kind": kind,
                                  "items": [i if isinstance(i, list) else [i] for i in items]}
                                 for t, kind, items in p["sections"]]}
    payload = json.dumps({"courses": courses, "names": NAMES, "programs": progs,
                          "url": URL}, ensure_ascii=False)
    template = (HERE / "template.html").read_text(encoding="utf-8")
    out.write_text(template.replace("/*__DATA__*/null", payload), encoding="utf-8")
    return out


# =============================================================== main
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--tree", metavar="SIGLA", help="imprime el árbol de prerrequisitos de SIGLA")
    ap.add_argument("--program", help="clave de programa (M296, M297, M233, N160…) para podar el árbol")
    ap.add_argument("--extra", nargs="*", default=[], help="siglas adicionales a incluir")
    ap.add_argument("--pdf", action="append", default=[], help="PDF de malla del que extraer siglas")
    ap.add_argument("--pdf-name", action="append", default=[], help="nombre para cada --pdf")
    ap.add_argument("--depth", type=int, default=None,
                    help="profundidad máxima de recursión (por defecto sin límite)")
    ap.add_argument("--offline", action="store_true", help="no descargar; usar solo la caché")
    ap.add_argument("--refresh", action="store_true", help="ignorar la caché y volver a descargar")
    ap.add_argument("--out", default=str(HERE / "uc_prereqs.html"))
    ap.add_argument("--no-open", action="store_true", help="no abrir el navegador")
    ap.add_argument("--list", action="store_true", help="listar programas disponibles")
    args = ap.parse_args()

    programs = dict(PROGRAMS)
    for i, pdf in enumerate(args.pdf):
        name = args.pdf_name[i] if i < len(args.pdf_name) else Path(pdf).stem
        key = f"PDF{i + 1}"
        programs[key] = program_from_pdf(pdf, name)
        print(f"PDF '{pdf}': {len(programs[key]['sections'][0][2])} siglas -> programa {key}")

    if args.list:
        for k, p in programs.items():
            print(f"{k:6} {p['kind']:5} {p['name']}")
        return

    cat = Catalog(offline=args.offline, refresh=args.refresh)

    if args.tree:
        root = args.tree.upper()
        print("Descargando requisitos…")
        cat.crawl([root], args.depth)
        prog = None
        if args.program:
            key = args.program.upper()
            if key not in programs:
                sys.exit(f"Programa desconocido: {key} (usa --list)")
            tmp = PROGRAMS
            prog = set()
            for p in programs[key]["sections"]:
                for it in p[2]:
                    prog.update(it if isinstance(it, list) else [it])
            del tmp
        print()
        print_tree(cat, root, prog)
        return

    roots = []
    for k in programs:
        if k in PROGRAMS:
            roots += program_courses(k)
        else:
            roots += programs[k]["sections"][0][2]
    roots += [s.upper() for s in args.extra]
    roots = list(dict.fromkeys(roots))
    print(f"Descargando requisitos de {len(roots)} cursos de los programas (+ sus prerrequisitos)…")
    cat.crawl(roots, args.depth)
    for s in args.extra:
        programs.setdefault("EXTRA", {"name": "Cursos extra (--extra)", "kind": "minor",
                                      "sections": [("Extra", "req", [])]})
        programs["EXTRA"]["sections"][0][2].append(s.upper())
    out = build_html(cat, programs, Path(args.out))
    print(f"\n✔ {len(cat.data)} cursos en caché. HTML: {out}")
    if not args.no_open:
        webbrowser.open(out.resolve().as_uri())


if __name__ == "__main__":
    main()
