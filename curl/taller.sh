#!/usr/bin/env bash
# Ejecuta todo el taller con curl, en orden, guardando los ids creados.
#
# Uso:
#   curl/taller.sh                         # servidor público de HAPI
#   FHIRURL=http://localhost:8080/fhir curl/taller.sh
#   curl/taller.sh 06                      # solo hasta el módulo 06
#
# Requiere curl y jq. Solo datos sintéticos.
set -euo pipefail
raiz="$(cd "$(dirname "$0")/.." && pwd)"
FHIRURL="${FHIRURL:-https://hapi.fhir.org/baseR4}"
hasta="${1:-19}"
declare -A ids

sustituir() {   # reemplaza {{variable}} por los ids guardados
  local texto="$1" var
  for var in "${!ids[@]}"; do texto="${texto//\{\{$var\}\}/${ids[$var]}}"; done
  printf '%s' "$texto"
}

echo "Servidor: $FHIRURL"
n=$(jq '.pasos | length' "$raiz/herramientas/pasos.json")
for ((i = 0; i < n; i++)); do
  paso=$(jq -c ".pasos[$i]" "$raiz/herramientas/pasos.json")
  id=$(jq -r .id <<<"$paso"); modulo=$(jq -r .modulo <<<"$paso")
  [ "${modulo:0:2}" \> "$hasta" ] && break
  metodo=$(jq -r .metodo <<<"$paso"); nombre=$(jq -r .nombre <<<"$paso")
  ruta=$(sustituir "$(jq -r .ruta <<<"$paso")")
  url="$FHIRURL${ruta:+/$ruta}"
  args=(-sS -o /tmp/aprende-fhir-respuesta.json -w '%{http_code}' -X "$metodo"
        -H 'Accept: application/fhir+json' --globoff)
  while IFS= read -r encabezado; do
    [ -n "$encabezado" ] && args+=(-H "$encabezado")
  done < <(jq -r '.encabezados // {} | to_entries[] | "\(.key): \(.value)"' <<<"$paso")
  archivo=$(jq -r '.archivo // empty' <<<"$paso")
  if [ -n "$archivo" ]; then
    cuerpo=$(sustituir "$(cat "$raiz/$archivo")")
    args+=(-H 'Content-Type: application/fhir+json' --data-binary "$cuerpo")
  fi
  codigo=$(curl "${args[@]}" "$url")
  guarda=$(jq -r '.guarda // empty' <<<"$paso")
  extra=""
  if [ -n "$guarda" ] && [ "${codigo:0:1}" = "2" ]; then
    ids[$guarda]=$(jq -r .id /tmp/aprende-fhir-respuesta.json)
    extra=" → $guarda = ${ids[$guarda]}"
  fi
  printf '%s %-4s %-6s %s%s\n' "$codigo" "$id" "$metodo" "$nombre" "$extra"
  espera=$(jq -r '.espera.servidor // "acepta"' <<<"$paso")
  if [ "$espera" = "rechaza" ]; then
    if [ "${codigo:0:1}" != "4" ]; then
      echo "El paso $id debía ser rechazado por el servidor y respondió $codigo" >&2; exit 1
    fi
    echo "     ↳ rechazado, como se esperaba: $(jq -r '.issue[0].diagnostics' /tmp/aprende-fhir-respuesta.json | cut -c1-110)"
  elif [ "${codigo:0:1}" != "2" ]; then
    echo "Error en el paso $id. Respuesta del servidor:" >&2
    jq '.issue // .' /tmp/aprende-fhir-respuesta.json >&2
    exit 1
  fi
done
echo "Listo. Expediente completo: $FHIRURL/Patient/${ids[patientId]:-}/\$everything"
