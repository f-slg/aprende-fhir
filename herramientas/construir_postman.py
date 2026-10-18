"""Genera las colecciones de Postman a partir de herramientas/pasos.json.

- postman/aprende-fhir.postman_collection.json: el taller completo.
- postman/niveles/N-nivel.postman_collection.json: el mismo taller en tres partes, más
  livianas de importar (la extensión de Postman para VS Code rechaza colecciones grandes).
  Los ids pasan de una parte a otra a través del entorno seleccionado.

Uso: python3 herramientas/construir_postman.py
"""
import json
import os
import uuid

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
    "17-busquedas-y-versiones": "17 · Búsquedas avanzadas y versiones",
    "18-terminologias-y-perfiles": "18 · Terminologías y perfiles",
    "19-resumen-ips": "19 · Resumen del paciente (IPS)",
}

def peticion(paso):
    ruta = paso["ruta"]
    base = "{{TXURL}}" if paso.get("servidor") == "terminologia" else "{{FHIRURL}}"
    raw = base + ("/" + ruta if ruta else "")
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
                    f'if (pm.environment.name) pm.environment.set("{paso["guarda"]}", id);',
                    f'console.log("{paso["guarda"]} = " + id);']
    item = {"name": f'{paso["id"]} · {paso["nombre"]}', "request": req,
            "event": [{"listen": "test", "script": {"type": "text/javascript", "exec": pruebas}}]}
    if "archivo" in paso:
        item["request"]["description"] = f'Cuerpo: `{paso["archivo"]}`'
    return item

carpetas = {}
for paso in manifiesto["pasos"]:
    carpetas.setdefault(paso["modulo"], []).append(peticion(paso))

BASE = [{"key": "FHIRURL", "value": "https://hapi.fhir.org/baseR4"},
        {"key": "TXURL", "value": "https://tx.fhir.org/r4"}]
DESCRIPCION = ("Taller de HL7 FHIR R4 con un caso clínico ecuatoriano ficticio. "
               "Ejecuta las peticiones en orden: cada POST guarda el id creado en una "
               "variable de la colección (y del entorno, si elegiste uno) que usan las "
               "peticiones siguientes. Elige el entorno hapi-publico o hapi-local, o cambia "
               "la variable FHIRURL. Solo datos sintéticos.\n\n"
               "https://github.com/f-slg/aprende-fhir")
NIVELES = [("1-basico", "Nivel básico", range(1, 7)),
           ("2-intermedio", "Nivel intermedio", range(7, 17)),
           ("3-avanzado", "Nivel avanzado", range(17, 20))]


def coleccion(nombre, modulos, clave):
    pasos = [p for p in manifiesto["pasos"] if p["modulo"] in modulos]
    variables = BASE + [{"key": p["guarda"], "value": ""} for p in pasos if "guarda" in p]
    return {
        "info": {
            "_postman_id": str(uuid.uuid5(uuid.NAMESPACE_URL, "aprende-fhir/" + clave)),
            "name": nombre,
            "description": DESCRIPCION,
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
        },
        "item": [{"name": TITULOS[m], "item": carpetas[m]} for m in modulos],
        "variable": variables,
    }


def guardar(objeto, ruta):
    destino = os.path.join(raiz, "postman", ruta)
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    with open(destino, "w", encoding="utf-8") as f:
        json.dump(objeto, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("Escrito:", os.path.relpath(destino, raiz))


guardar(coleccion("Aprende FHIR desde cero", list(carpetas), "completo"),
        "aprende-fhir.postman_collection.json")
for clave, titulo, rango in NIVELES:
    modulos = [m for m in carpetas if int(m[:2]) in rango]
    guardar(coleccion(f"Aprende FHIR · {titulo}", modulos, clave),
            f"niveles/{clave}.postman_collection.json")
