# Módulo 07 · Documentos clínicos

[← Módulo 06](../06-observaciones/README.md) · [Inicio](../../README.md) · [Módulo 08 →](../08-anatomia-patologica/README.md)

## Objetivos

- Entender la diferencia entre **recursos sueltos** y un **documento clínico**.
- Crear una `Composition` y un `Bundle` de tipo `document`.

## Conceptos clave

Hasta ahora cada recurso vive por separado en el servidor y puede cambiar.
Un **documento** (un informe, una epicrisis, un certificado) es distinto: se
firma en un momento, no cambia y tiene que poder leerse completo aunque se
envíe a otro sistema.

- **`Composition`** es el "índice" del documento: tipo, autor, fecha, título
  y **secciones** que apuntan a los recursos que contiene.
- **`Bundle` de tipo `document`**: el primer `entry` es la `Composition` y
  después van **todos** los recursos a los que se refiere (paciente, autor,
  custodio, observaciones). Es autocontenido: las referencias usan
  `urn:uuid:` dentro del propio Bundle, no ids del servidor.
- Un documento necesita `identifier` y `timestamp` en el Bundle.

## Ejercicios

### 07a · La composición

Crea una nota de signos vitales (LOINC `8716-3`, *Vital signs note*) con una
sección que apunte a las cuatro observaciones del módulo 06.

Solución: [`07a_composition_signos_vitales.json`](soluciones/07a_composition_signos_vitales.json)

### 07b · El documento autocontenido

Arma el `Bundle` de tipo `document` con la composición, el paciente, la
médica, el hospital y las cuatro observaciones. Envíalo con
`POST {{FHIRURL}}/Bundle`: el servidor lo guarda **como un solo recurso**,
sin separar su contenido.

Solución: [`07b_bundle_document_signos_vitales.json`](soluciones/07b_bundle_document_signos_vitales.json)

### 07c · Leerlo

`GET {{FHIRURL}}/Bundle/{{bundleDocId}}`. Compáralo con la búsqueda del
módulo 06: ¿qué diferencia hay entre un `searchset` y un `document`?

## Para pensar

Si mañana se corrige la presión arterial de Luis (con `PUT`), ¿cambia el
documento ya emitido? ¿Por qué eso es lo deseable en un documento clínico?

## Ejecutar este módulo

- **Postman:** carpeta *07 · Documentos clínicos*.
- **curl:** `curl/taller.sh 07`
- **R:** `fhir_crear("Bundle", "modulos/07-documentos-clinicos/soluciones/07b_bundle_document_signos_vitales.json", guarda = "bundleDocId")`
