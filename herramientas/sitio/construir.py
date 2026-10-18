"""Arma el sitio web del taller con MkDocs Material.

Copia el contenido del repositorio a .sitio/docs (sin modificar los README
originales), genera .sitio/mkdocs.yml con la navegación por niveles y, si se
pide, construye el sitio en .sitio/site.

Uso:
  pip install -r herramientas/sitio/requisitos.txt
  python3 herramientas/sitio/construir.py            # prepara y construye
  python3 herramientas/sitio/construir.py --servir   # vista previa en http://127.0.0.1:8000
"""
import glob
import os
import re
import shutil
import subprocess
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SITIO = os.path.join(RAIZ, ".sitio")
DOCS = os.path.join(SITIO, "docs")
NIVELES = [("Nivel básico", range(1, 7)), ("Nivel intermedio", range(7, 17)),
           ("Nivel avanzado", range(17, 20))]

# --- 1. Copiar el contenido ---------------------------------------------------------
shutil.rmtree(SITIO, ignore_errors=True)
os.makedirs(DOCS)
for nombre in ("README.md", "LICENSE"):
    shutil.copy(os.path.join(RAIZ, nombre), DOCS)
for carpeta in ("modulos", "imagenes", "postman", "r", "curl"):
    shutil.copytree(os.path.join(RAIZ, carpeta), os.path.join(DOCS, carpeta))
os.makedirs(os.path.join(DOCS, "herramientas"))
for nombre in ("pasos.json", "validar.sh", "construccion.json"):
    shutil.copy(os.path.join(RAIZ, "herramientas", nombre), os.path.join(DOCS, "herramientas"))
shutil.copytree(os.path.join(RAIZ, "herramientas", "sitio", "estilos"), os.path.join(DOCS, "estilos"))

# --- 2. Navegación: el título de cada módulo sale de su primer encabezado -----------
def titulo(md):
    for linea in open(md, encoding="utf-8"):
        if linea.startswith("# "):
            return re.sub(r"^Módulo (\d+) · ", r"\1 · ", linea[2:].strip())
    return os.path.basename(os.path.dirname(md))

modulos = {int(os.path.basename(os.path.dirname(m))[:2]): m
           for m in glob.glob(os.path.join(RAIZ, "modulos", "*", "README.md"))}
nav = ["  - Inicio: README.md"]
for nivel, rango in NIVELES:
    nav.append(f"  - {nivel}:")
    for n in rango:
        if n in modulos:
            ruta = os.path.relpath(modulos[n], RAIZ).replace(os.sep, "/")
            nav.append(f'    - "{titulo(modulos[n])}": {ruta}')

configuracion = open(os.path.join(RAIZ, "herramientas", "sitio", "mkdocs.base.yml"),
                     encoding="utf-8").read()
configuracion += "\nnav:\n" + "\n".join(nav) + "\n"
open(os.path.join(SITIO, "mkdocs.yml"), "w", encoding="utf-8").write(configuracion)
shutil.copy(os.path.join(RAIZ, "herramientas", "sitio", "ganchos.py"), SITIO)
print(f"Sitio preparado en {os.path.relpath(SITIO, RAIZ)}/ con {len(modulos)} módulos.")

# --- 3. Construir o servir ------------------------------------------------------------
orden = ["serve"] if "--servir" in sys.argv else ["build", "--strict"]
sys.exit(subprocess.call([sys.executable, "-m", "mkdocs"] + orden, cwd=SITIO))
