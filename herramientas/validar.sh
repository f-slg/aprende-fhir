#!/usr/bin/env bash
# Valida el taller con el validador oficial de HL7 FHIR (R4):
#   1. las soluciones y los pasos intermedios deben pasar sin errores;
#   2. los errores a propósito marcados con "validador": "falla" en
#      herramientas/pasos.json deben ser detectados.
# Los marcadores {{variable}} se reemplazan por ids de ejemplo antes de validar.
#
# Uso: herramientas/validar.sh [--avisos]
#      VALIDATOR_JAR=/ruta/validator_cli.jar herramientas/validar.sh
set -euo pipefail
raiz="$(cd "$(dirname "$0")/.." && pwd)"
jar="${VALIDATOR_JAR:-$raiz/.validador/validator_cli.jar}"
if [ ! -f "$jar" ]; then
  mkdir -p "$(dirname "$jar")"
  echo "Descargando el validador oficial de HL7..."
  curl -sSL -o "$jar" https://github.com/hapifhir/org.hl7.fhir.core/releases/latest/download/validator_cli.jar
fi
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
mkdir -p "$tmp/correctos" "$tmp/errores"
preparar() { sed -E 's/\{\{([A-Za-z0-9]+)\}\}/ej-\1/g' "$1" > "$2/$(basename "$1")"; }
for f in "$raiz"/modulos/*/soluciones/*.json "$raiz"/modulos/*/pasos/*.json; do
  preparar "$f" "$tmp/correctos"
done
python3 - "$raiz" <<'PY' > "$tmp/deben_fallar.txt"
import json, os, sys
raiz = sys.argv[1]
for p in json.load(open(os.path.join(raiz, "herramientas", "pasos.json"), encoding="utf-8"))["pasos"]:
    if p.get("espera", {}).get("validador") == "falla":
        print(os.path.join(raiz, p["archivo"]))
PY
while read -r f; do preparar "$f" "$tmp/errores"; done < "$tmp/deben_fallar.txt"

validar() {
  java -Duser.language=en -Xmx2g -jar "$jar" -version 4.0.1 -language en \
    "$1"/*.json -output "$1/resultado.json" > "$1/validador.log" 2>&1 || true
}
echo "== Soluciones y pasos intermedios (deben pasar)"
validar "$tmp/correctos"
estado=0
python3 "$raiz/herramientas/resumen_validacion.py" "$tmp/correctos/resultado.json" "$@" | grep -v '^OK ' || estado=$?
python3 "$raiz/herramientas/resumen_validacion.py" "$tmp/correctos/resultado.json" > /dev/null || estado=1

echo
echo "== Errores a propósito (el validador debe detectarlos)"
validar "$tmp/errores"
python3 "$raiz/herramientas/resumen_validacion.py" "$tmp/errores/resultado.json" --deben-fallar || estado=1
exit $estado
