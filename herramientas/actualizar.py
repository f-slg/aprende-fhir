"""Mantiene sincronizado el taller.

1. Genera las versiones intermedias de cada recurso (modulos/*/pasos/*.json) a
   partir de herramientas/construccion.json y comprueba que el último paso es
   exactamente la solución.
2. Rellena en los README los bloques entre marcadores:
     <!-- paso 02a 3 --> ... <!-- /paso -->            campos que agrega el paso 3
     <!-- diferencia 02e --> ... <!-- /diferencia -->  campos que cambian respecto de otra solución
     <!-- ficha Patient --> ... <!-- /ficha -->        cardinalidad y tipo de cada elemento,
                                                       tomados de la especificación oficial R4
3. Regenera la colección de Postman.

Uso: python3 herramientas/actualizar.py
     python3 herramientas/actualizar.py --comprobar   (falla si algo no está al día)

La especificación se lee del paquete hl7.fhir.r4.core en ~/.fhir/packages
(lo descarga herramientas/validar.sh la primera vez).
"""
import copy
import glob
import json
import os
import re
import subprocess
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAQUETE = os.path.expanduser("~/.fhir/packages/hl7.fhir.r4.core#4.0.1/package")
comprobar = "--comprobar" in sys.argv
cambios = []


def escribir(ruta, contenido):
    anterior = open(ruta, encoding="utf-8").read() if os.path.exists(ruta) else None
    if anterior != contenido:
        cambios.append(os.path.relpath(ruta, RAIZ))
        if not comprobar:
            os.makedirs(os.path.dirname(ruta), exist_ok=True)
            with open(ruta, "w", encoding="utf-8") as f:
                f.write(contenido)


def a_json(objeto):
    return json.dumps(objeto, ensure_ascii=False, indent=2) + "\n"


def leer(ruta):
    return json.load(open(os.path.join(RAIZ, ruta), encoding="utf-8"))


# --- 1. Pasos de construcción -----------------------------------------------------------
spec = json.load(open(os.path.join(RAIZ, "herramientas", "construccion.json"), encoding="utf-8"))
fragmentos = {}       # ("02a", 3) -> dict con los campos agregados en ese paso
diferencias = {}      # "02e" -> dict con los campos que cambian
for clave, info in spec.items():
    final = leer(info["archivo"])
    if "pasos" in info:
        actual = {}
        for n, paso in enumerate(info["pasos"], start=1):
            nuevos = {}
            for campo in paso.get("campos", []):
                if campo not in final:
                    sys.exit(f"{clave} paso {n}: '{campo}' no está en la solución")
                nuevos[campo] = copy.deepcopy(final[campo])
            nuevos.update(copy.deepcopy(paso.get("parcial", {})))
            actual.update(nuevos)
            ordenado = {k: actual[k] for k in final if k in actual}
            ordenado.update({k: v for k, v in actual.items() if k not in ordenado})
            fragmentos[(clave, n)] = nuevos
            carpeta = os.path.dirname(os.path.dirname(os.path.join(RAIZ, info["archivo"])))
            escribir(os.path.join(carpeta, "pasos", f"{clave}_paso{n}.json"), a_json(ordenado))
        if actual != final:
            faltan = sorted(set(final) - set(actual))
            sys.exit(f"{clave}: el último paso no coincide con la solución (faltan: {faltan})")
    else:
        base = leer(spec[info["diferencia"]]["archivo"]) if info["diferencia"] in spec else \
            leer(glob.glob(os.path.join(RAIZ, "modulos", "*", "soluciones", info["diferencia"] + "_*.json"))[0])
        diferencias[clave] = {k: v for k, v in final.items()
                              if k != "text" and base.get(k) != v}

# --- 2. Especificación oficial para las fichas ----------------------------------------------
definiciones = {}


def elemento(recurso, ruta):
    if recurso not in definiciones:
        archivo = os.path.join(PAQUETE, f"StructureDefinition-{recurso}.json")
        if not os.path.exists(archivo):
            sys.exit(f"No se encontró la definición de {recurso}. Ejecuta herramientas/validar.sh "
                     "una vez para descargar la especificación.")
        sd = json.load(open(archivo, encoding="utf-8"))
        definiciones[recurso] = {e["path"]: e for e in sd["snapshot"]["element"]}
    return definiciones[recurso].get(f"{recurso}.{ruta}")


def tipo(e):
    tipos = []
    for t in e.get("type", []):
        if t["code"] == "Reference" and t.get("targetProfile"):
            destinos = [p.rsplit("/", 1)[-1] for p in t["targetProfile"]]
            if len(destinos) > 4:
                destinos = destinos[:4] + ["…"]
            tipos.append("Reference(" + " \\| ".join(destinos) + ")")
        else:
            tipos.append(t["code"].replace("http://hl7.org/fhirpath/System.", ""))
    if len(tipos) > 4:
        return " \\| ".join(tipos[:4]) + " \\| …"
    return " \\| ".join(tipos)


def ficha(recurso, bloque):
    filas = [l for l in bloque.strip().splitlines() if l.startswith("|")]
    salida = ["| Elemento | Card. | Tipo | Para qué sirve |", "|---|---|---|---|"]
    for fila in filas[2:]:
        celdas = [c.strip() for c in fila.strip("|").split("|")]
        nombre = celdas[0].replace("`", "").replace(" ⚑", "").strip()
        descripcion = celdas[-1]
        e = elemento(recurso, nombre)
        if e is None:
            sys.exit(f"Ficha de {recurso}: el elemento '{nombre}' no existe en FHIR R4")
        card = f'{e["min"]}..{e["max"]}'
        if e["min"] > 0:
            card = f"**{card}**"
        marca = " ⚑" if e.get("isModifier") else ""
        salida.append(f"| `{nombre}`{marca} | {card} | {tipo(e)} | {descripcion} |")
    return "\n".join(salida)


def bloque_json(objeto):
    return "```json\n" + json.dumps(objeto, ensure_ascii=False, indent=2) + "\n```"


PATRONES = [
    (re.compile(r"(?P<ini><!-- paso (?P<id>\w+) (?P<n>\d+) -->)(?P<cuerpo>.*?)(?P<fin><!-- /paso -->)", re.S),
     lambda m: bloque_json(fragmentos[(m["id"], int(m["n"]))])),
    (re.compile(r"(?P<ini><!-- diferencia (?P<id>\w+) -->)(?P<cuerpo>.*?)(?P<fin><!-- /diferencia -->)", re.S),
     lambda m: bloque_json(diferencias[m["id"]])),
    (re.compile(r"(?P<ini><!-- ficha (?P<id>\w+) -->)(?P<cuerpo>.*?)(?P<fin><!-- /ficha -->)", re.S),
     lambda m: ficha(m["id"], m["cuerpo"])),
]

for md in sorted(glob.glob(os.path.join(RAIZ, "modulos", "*", "README.md"))):
    texto = open(md, encoding="utf-8").read()
    nuevo = texto
    for patron, generar in PATRONES:
        def reemplazo(m, generar=generar):
            try:
                contenido = generar(m)
            except KeyError as faltante:
                sys.exit(f"{os.path.relpath(md, RAIZ)}: no existe {faltante} en construccion.json")
            return m["ini"] + "\n" + contenido + "\n" + m["fin"]
        nuevo = patron.sub(reemplazo, nuevo)
    if nuevo != texto:
        escribir(md, nuevo)

# --- 3. Postman ---------------------------------------------------------------------------
destino = os.path.join(RAIZ, "postman", "aprende-fhir.postman_collection.json")
antes = open(destino, encoding="utf-8").read() if os.path.exists(destino) else ""
subprocess.run([sys.executable, os.path.join(RAIZ, "herramientas", "construir_postman.py")],
               check=True, capture_output=True)
if open(destino, encoding="utf-8").read() != antes:
    cambios.append("postman/aprende-fhir.postman_collection.json")
    if comprobar:
        open(destino, "w", encoding="utf-8").write(antes)

if comprobar and cambios:
    print("No están al día (ejecuta python3 herramientas/actualizar.py):")
    print("\n".join("  " + c for c in cambios))
    sys.exit(1)
print("Actualizado:" if cambios else "Todo al día.", *cambios, sep="\n  ")
