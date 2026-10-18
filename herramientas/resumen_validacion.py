"""Resume la salida del validador de HL7.

Uso: resumen_validacion.py resultado.json [--avisos] [--deben-fallar]
  --avisos        muestra también las advertencias
  --deben-fallar  cada archivo debe tener al menos un error (errores a propósito)
"""
import collections
import json
import os
import sys

resultado = json.load(open(sys.argv[1], encoding="utf-8"))
avisos = "--avisos" in sys.argv[2:]
deben_fallar = "--deben-fallar" in sys.argv[2:]
salidas = [e["resource"] for e in resultado.get("entry", [])] or [resultado]
total = collections.Counter()
problemas = 0
for oo in salidas:
    ext = [x for x in oo.get("extension", []) if "file" in x.get("url", "")]
    nombre = os.path.basename(ext[0]["valueString"]) if ext else "?"
    issues = oo.get("issue", [])
    total.update(i["severity"] for i in issues)
    errores = [i for i in issues if i["severity"] in ("error", "fatal")]
    if deben_fallar:
        ok = bool(errores)
        print(f'{"OK " if ok else "ERR"} {nombre}: {"detectado" if ok else "el validador NO lo detectó"}')
        if errores:
            print(f'     {(errores[0].get("expression") or [""])[0]} | {errores[0]["details"]["text"][:150]}')
        problemas += not ok
        continue
    mostrar = errores + ([i for i in issues if i["severity"] == "warning"] if avisos else [])
    print(f'{"OK " if not errores else "ERR"} {nombre}')
    for i in mostrar:
        print(f'     {i["severity"]}: {(i.get("expression") or [""])[0]} | {i["details"]["text"]}')
    problemas += bool(errores)
if not deben_fallar:
    print(f"\nRecursos: {len(salidas)} · con errores: {problemas} · errores: "
          f"{total['error'] + total['fatal']} · avisos: {total['warning']}")
sys.exit(1 if problemas else 0)
