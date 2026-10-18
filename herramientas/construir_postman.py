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
    "07-antecedentes": "07 · Antecedentes",
    "08-vacunacion": "08 · Vacunación",
    "09-documentos-clinicos": "09 · Documentos clínicos",
    "10-ordenes-y-derivacion": "10 · Órdenes y derivación",
    "11-anatomia-patologica": "11 · Anatomía patológica",
    "12-plan-y-consentimiento": "12 · Plan y consentimiento",
    "13-procedimientos": "13 · Procedimientos",
    "14-citas": "14 · Citas",
    "15-medicamentos": "15 · Medicamentos",
    "16-seguimiento": "16 · Seguimiento",
}

def peticion(paso):
    ruta = paso["ruta"]
    raw = "{{FHIRURL}}" + ("/" + ruta if ruta else "")
    req = {"method": paso["metodo"],
           "header": [{"key": "Accept", "value": "application/fhir+json"}],
           "url": raw}
    for clave, valor in paso.get("encabezados", {}).items():
        req["header"].append({"key": clave, "value": valor})
    if "archivo" in paso:
        req["header"].append({"key": "Content-Type", "value": "application/fhir+json"})
        with open(os.path.join(raiz, paso["archivo"]), encoding="utf-8") as f:
            req["body"] = {"mode": "raw", "raw": f.read(),
                           "options": {"raw": {"language": "json"}}}
    if paso.get("espera", {}).get("servidor") == "rechaza":
        pruebas = ['pm.test("El servidor rechaza el error (4xx)", function () {',
                   '    pm.expect(pm.response.code).to.be.within(400, 499);',
                   '});',
                   'console.log(pm.response.json().issue[0].diagnostics);']
    else:
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
