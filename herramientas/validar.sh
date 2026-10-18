#!/usr/bin/env bash
# Valida todos los recursos del taller con el validador oficial de HL7 FHIR (R4).
# Los marcadores {{variable}} se reemplazan por ids de ejemplo antes de validar.
# Uso: herramientas/validar.sh [ruta/a/validator_cli.jar]
set -euo pipefail
raiz="$(cd "$(dirname "$0")/.." && pwd)"
jar="${1:-${VALIDATOR_JAR:-$raiz/.validador/validator_cli.jar}}"
if [ ! -f "$jar" ]; then
  mkdir -p "$(dirname "$jar")"
  echo "Descargando el validador oficial de HL7..."
  curl -sSL -o "$jar" https://github.com/hapifhir/org.hl7.fhir.core/releases/latest/download/validator_cli.jar
fi
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
for f in "$raiz"/modulos/*/soluciones/*.json; do
  sed -E 's/\{\{([A-Za-z]+)\}\}/ej-\1/g' "$f" > "$tmp/$(basename "$f")"
done
java -Duser.language=en -Xmx2g -jar "$jar" -version 4.0.1 -language en \
  "$tmp"/*.json -output "$tmp/resultado.json" > "$tmp/validador.log" 2>&1 || true
python3 "$raiz/herramientas/resumen_validacion.py" "$tmp/resultado.json" "${@:2}"
