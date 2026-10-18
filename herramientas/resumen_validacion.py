"""Resume la salida del validador de HL7 y termina con error si hay errores."""
import collections
import json
import os
import sys

resultado = json.load(open(sys.argv[1], encoding="utf-8"))
salidas = [e["resource"] for e in resultado.get("entry", [])] or [resultado]
total = collections.Counter()
for oo in salidas:
    ext = [x for x in oo.get("extension", []) if "file" in x.get("url", "")]
    nombre = os.path.basename(ext[0]["valueString"]) if ext else "?"
    graves = []
    for i in oo.get("issue", []):
        total[i["severity"]] += 1
        if i["severity"] in ("error", "fatal") or (i["severity"] == "warning" and "--avisos" in sys.argv[2:]):
            graves.append(i)
    marca = "OK " if not [g for g in graves if g["severity"] in ("error", "fatal")] else "ERR"
    print(f"{marca} {nombre}")
    for g in graves:
        lugar = (g.get("expression") or [""])[0]
        print(f"     {g['severity']}: {lugar} | {g['details']['text']}")
print(f"\nRecursos: {len(salidas)} · errores: {total['error'] + total['fatal']} · "
      f"avisos: {total['warning']} · información: {total['information']}")
sys.exit(1 if total["error"] + total["fatal"] else 0)
