# Módulo 01 · Fundamentos

[← Inicio](../../README.md) · [Módulo 02 →](../02-patient/README.md)

## Objetivos

- Entender qué es un **recurso** FHIR y cómo se ve en JSON.
- Conocer las operaciones **REST** básicas: crear, leer, actualizar, buscar.
- Consultar qué sabe hacer un servidor con su **CapabilityStatement**.

## Conceptos clave

**FHIR** (*Fast Healthcare Interoperability Resources*) es un estándar de HL7
para intercambiar información de salud. Divide la información clínica en
piezas pequeñas llamadas **recursos**: `Patient`, `Encounter`, `Observation`,
`Condition`... Cada recurso tiene una estructura definida en la
[especificación](https://hl7.org/fhir/R4/resourcelist.html) y se puede
representar en JSON o XML. En este taller usamos **FHIR R4 (4.0.1)**, la versión
más implementada.

Todo recurso tiene la misma anatomía:

```json
{
  "resourceType": "Patient",       // qué tipo de recurso es
  "id": "1000",                    // lo asigna el servidor al crearlo
  "meta": { "versionId": "2" },    // versión, fecha de modificación
  "text": { "div": "<div>…</div>" },  // resumen legible por personas
  "identifier": [ … ],             // identificadores del mundo real (cédula)
  "name": [ … ]                    // datos propios del recurso
}
```

Los recursos se **enlazan** con referencias (`"reference": "Patient/1000"`):
así una observación sabe de qué paciente es y en qué consulta se tomó.

La API de FHIR es **REST**: cada tipo de recurso tiene una dirección y se usan
los métodos de HTTP.

| Acción | Método y ruta | Respuesta |
|---|---|---|
| Crear | `POST /Patient` | `201 Created` y el recurso con su `id` |
| Leer | `GET /Patient/1000` | `200 OK` |
| Actualizar | `PUT /Patient/1000` | `200 OK` y una nueva versión |
| Buscar | `GET /Patient?family=Paredes` | `200 OK` y un `Bundle` de resultados |
| Historial | `GET /Patient/1000/_history` | todas las versiones |
| Borrar | `DELETE /Patient/1000` | `200` o `204` |

Siempre se envían los encabezados `Accept: application/fhir+json` y, si hay
cuerpo, `Content-Type: application/fhir+json`.

## Ejercicios

### 01a · ¿Qué sabe hacer el servidor?

Pide la declaración de capacidades del servidor:

```http
GET {{FHIRURL}}/metadata
```

Busca en la respuesta:

1. ¿Qué versión de FHIR implementa (`fhirVersion`)?
2. ¿Qué software es (`software.name`)?
3. En `rest[0].resource`, busca `Patient`: ¿qué operaciones (`interaction`) y
   qué parámetros de búsqueda (`searchParam`) admite?

### 01b · Tu primera búsqueda

```http
GET {{FHIRURL}}/Patient?_count=5
```

La respuesta es un `Bundle` de tipo `searchset`. Observa `total`, `link`
(paginación) y `entry` (los resultados).

> **En un servidor público verás pacientes de otras personas.** Todo lo que
> subas también será visible para todos: usa solo datos sintéticos, como los
> de este taller.

## Para pensar

¿Por qué crees que FHIR separa el `id` (lo asigna el servidor) del
`identifier` (la cédula, la historia clínica)? ¿Qué pasaría si el mismo
paciente se registra en dos servidores distintos?

## Ejecutar este módulo

- **Postman:** carpeta *01 · Fundamentos*.
- **curl:** `curl/taller.sh 01`
- **R:** `source("r/fhir.R"); fhir_leer("metadata")$fhirVersion`
