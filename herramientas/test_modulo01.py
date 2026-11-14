"""Prueba el módulo 01 dos veces contra un servidor de prueba local.

El servidor exige un UUID válido por creación y recuerda los identificadores
incluso después del borrado. Así detecta la regresión sin depender de la caché
ni de la disponibilidad del servidor público. Solo usa la biblioteca estándar.

Uso: python3 herramientas/test_modulo01.py
Prueba curl y, si están instalados, R (httr2, jsonlite, uuid) y newman.
"""
import json
import os
from pathlib import Path
import shutil
import subprocess
import threading
import unittest
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


RAIZ = Path(__file__).resolve().parent.parent
SYSTEM = "https://f-slg.github.io/aprende-fhir/sid/ejercicio-01"


class Modulo01Test(unittest.TestCase):
    def setUp(self):
        self.creados = {}
        self.borrados = set()
        self.leidos = []
        self.errores = []
        prueba = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass

            def responder(self, codigo, cuerpo=None):
                datos = json.dumps(cuerpo).encode() if cuerpo is not None else b""
                self.send_response(codigo)
                self.send_header("Content-Type", "application/fhir+json")
                self.send_header("Content-Length", str(len(datos)))
                self.end_headers()
                self.wfile.write(datos)

            def error(self, codigo, mensaje):
                self.responder(codigo, {"resourceType": "OperationOutcome", "issue": [
                    {"severity": "error", "code": "processing", "diagnostics": mensaje}
                ]})

            def do_GET(self):
                if self.path == "/metadata":
                    return self.responder(200, {"resourceType": "CapabilityStatement",
                                                "fhirVersion": "4.0.1"})
                if self.path == "/Patient?_count=5":
                    return self.responder(200, {"resourceType": "Bundle", "type": "searchset"})
                paciente = prueba.creados.get(self.path)
                if paciente is None:
                    return self.error(404, "No existe")
                if self.path in prueba.borrados:
                    return self.error(410, "Borrado")
                prueba.leidos.append(self.path)
                self.responder(200, paciente)

            def do_POST(self):
                paciente = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
                if paciente.get("resourceType") == "Paciente":
                    return self.error(400, "Tipo de recurso incorrecto: Paciente")
                try:
                    if self.path != "/Patient" or paciente.get("resourceType") != "Patient":
                        raise ValueError("Se esperaba POST /Patient")
                    identificador = paciente["identifier"][0]
                    if identificador["system"] != SYSTEM:
                        raise ValueError("Sistema de identificación incorrecto")
                    valor = identificador["value"]
                    if str(uuid.UUID(valor, version=4)) != valor.lower():
                        raise ValueError("Se esperaba un UUID v4")
                    if "nombre" not in paciente or "name" in paciente:
                        raise ValueError("Se perdió el error intencional de nombre")
                    if any(p["identifier"][0]["value"] == valor for p in prueba.creados.values()):
                        raise ValueError("Identificador repetido, aunque el paciente esté borrado")
                except (KeyError, ValueError, IndexError) as error:
                    prueba.errores.append(str(error))
                    return self.error(412, str(error))
                paciente.pop("nombre")  # HAPI tolerante descarta el elemento desconocido.
                paciente["id"] = f"prueba-{len(prueba.creados) + 1}"
                prueba.creados[f'/Patient/{paciente["id"]}'] = paciente
                self.responder(201, paciente)

            def do_DELETE(self):
                if self.path not in prueba.creados:
                    return self.error(404, "No existe")
                prueba.borrados.add(self.path)
                # Ambos tipos de respuesta deben funcionar, incluida la ausencia de JSON.
                if len(prueba.borrados) % 2 == 0:
                    return self.responder(204)
                self.responder(200, {"resourceType": "OperationOutcome", "issue": []})

        self.servidor = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.hilo = threading.Thread(target=self.servidor.serve_forever, daemon=True)
        self.hilo.start()
        self.entorno = dict(os.environ, FHIRURL=f"http://127.0.0.1:{self.servidor.server_port}")

    def tearDown(self):
        self.servidor.shutdown()
        self.servidor.server_close()
        self.hilo.join()

    def ejecutar(self, comando):
        resultado = subprocess.run(comando, cwd=RAIZ, env=self.entorno,
                                   text=True, capture_output=True, timeout=90)
        self.assertEqual(resultado.returncode, 0, resultado.stdout + resultado.stderr)

    def comprobar(self):
        self.assertEqual(self.errores, [])
        self.assertEqual(len(self.creados), 2)
        self.assertEqual(set(self.creados), self.borrados)
        self.assertCountEqual(self.leidos, self.creados)
        for paciente in self.creados.values():
            self.assertNotIn("nombre", paciente)
            self.assertNotIn("name", paciente)

    def test_curl(self):
        for _ in range(2):
            self.ejecutar(["bash", "curl/taller.sh", "01"])
        self.comprobar()

    @unittest.skipUnless(shutil.which("Rscript"), "Rscript no instalado")
    def test_r(self):
        paquetes = subprocess.run(["Rscript", "-e", 'quit(status = !all(vapply('
                                  'c("httr2", "jsonlite", "uuid"), requireNamespace, '
                                  'logical(1), quietly = TRUE)))'], capture_output=True)
        if paquetes.returncode:
            self.skipTest("Faltan httr2, jsonlite o uuid en R")
        # Repetir en la misma sesión también debe producir un UUID nuevo.
        self.ejecutar(["Rscript", "-e", 'source("r/taller.R"); source("r/taller.R")', "01"])
        self.comprobar()

    def postman(self, archivo):
        newman = shutil.which("newman")
        if newman is None:
            self.skipTest("newman no instalado")
        self.ejecutar([newman, "run", archivo, "--folder", "01 · Fundamentos",
                       "--iteration-count", "2", "--env-var",
                       f'FHIRURL={self.entorno["FHIRURL"]}', "--bail"])
        self.comprobar()

    def test_postman_completo(self):
        self.postman("postman/aprende-fhir.postman_collection.json")

    def test_postman_basico(self):
        self.postman("postman/niveles/1-basico.postman_collection.json")


if __name__ == "__main__":
    unittest.main(verbosity=2)
