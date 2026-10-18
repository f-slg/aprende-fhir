"""Genera postman/aprende-fhir.postman_collection.json a partir de herramientas/pasos.json.

Uso: python3 herramientas/construir_postman.py
"""
import json
import os

raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
manifiesto = json.load(open(os.path.join(raiz, "herramientas", "pasos.json"), encoding="utf-8"))
TITULOS = {
    "01-fundamentos": "01 · Fundamentos",
    "02-patient": "02 · Patient",
    "03-transacciones": "03 · Transacciones",
    "04-profesionales-y-organizaciones": "04 · Profesionales y organizaciones",
    "05-diagnostico-y-encuentro": "05 · Diagnóstico y encuentro",
    "06-observaciones": "06 · Observaciones",
    "07-documentos-clinicos": "07 · Documentos clínicos",
    "08-anatomia-patologica": "08 · Anatomía patológica",
    "09-procedimientos": "09 · Procedimientos",
    "10-medicamentos": "10 · Medicamentos",
}

def peticion(paso):
    ruta = paso["ruta"]
    raw = "{{FHIRURL}}" + ("/" + ruta if ruta else "")
    req = {"method": paso["metodo"],
           "header": [{"key": "Accept", "value": "application/fhir+json"}],
           "url": raw}
    if "archivo" in paso:
        req["header"].append({"key": "Content-Type", "value": "application/fhir+json"})
        with open(os.path.join(raiz, paso["archivo"]), encoding="utf-8") as f:
            req["body"] = {"mode": "raw", "raw": f.read(),
                           "options": {"raw": {"language": "json"}}}
    pruebas = ['pm.test("Respuesta exitosa (2xx)", function () {',
               '    pm.expect(pm.response.code).to.be.within(200, 299);',
               '});']
    if "guarda" in paso:
        pruebas += ['const id = pm.response.json().id;',
                    f'pm.collectionVariables.set("{paso["guarda"]}", id);',
                    f'console.log("{paso["guarda"]} = " + id);']
    item = {"name": f'{paso["id"]} · {paso["nombre"]}', "request": req,
            "event": [{"listen": "test", "script": {"type": "text/javascript", "exec": pruebas}}]}
    if "archivo" in paso:
        item["request"]["description"] = f'Cuerpo: `{paso["archivo"]}`'
    return item

carpetas = {}
for paso in manifiesto["pasos"]:
    carpetas.setdefault(paso["modulo"], []).append(peticion(paso))

variables = [{"key": "FHIRURL", "value": "https://hapi.fhir.org/baseR4"}]
variables += [{"key": p["guarda"], "value": ""} for p in manifiesto["pasos"] if "guarda" in p]
coleccion = {
    "info": {
        "name": "Aprende FHIR desde cero",
        "description": ("Taller de HL7 FHIR R4 con un caso clínico ecuatoriano ficticio. "
                        "Ejecuta las peticiones en orden: cada POST guarda el id creado en una "
                        "variable de la colección que usan las peticiones siguientes. Cambia la "
                        "variable FHIRURL para usar otro servidor. Solo datos sintéticos.\n\n"
                        "https://github.com/f-slg/aprende-fhir"),
        "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
    },
    "item": [{"name": TITULOS[m], "item": items} for m, items in carpetas.items()],
    "variable": variables,
}
destino = os.path.join(raiz, "postman", "aprende-fhir.postman_collection.json")
os.makedirs(os.path.dirname(destino), exist_ok=True)
with open(destino, "w", encoding="utf-8") as f:
    json.dump(coleccion, f, ensure_ascii=False, indent=2)
    f.write("\n")
print("Escrito:", os.path.relpath(destino, raiz))
