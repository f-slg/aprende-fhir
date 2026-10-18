# Módulo 04 · Profesionales y organizaciones

[← Módulo 03](../03-transacciones/README.md) · [Inicio](../../README.md) · [Módulo 05 →](../05-diagnostico-y-encuentro/README.md)

## Objetivos

- Registrar a un profesional de salud con `Practitioner`.
- Modelar establecimientos y su jerarquía con `Organization` y `partOf`.
- Buscar recursos por una **referencia**.

## El caso

Luis será atendido por la **Dra. Andrea Lucía Salazar Moreno**, médica general
(registro profesional ficticio `RP-000457`), en el **Hospital General Docente
Ejemplo**, que forma parte de la **Red de Servicios de Salud Ejemplo**. Las
dos organizaciones son ficticias.

## Conceptos clave

- **`Practitioner`** describe a la persona (nombre, títulos en
  `qualification`). Su rol en un establecimiento concreto se modela con
  `PractitionerRole`, que puedes explorar como reto.
- **`Organization.partOf`** construye jerarquías: red → hospital → servicio.
  Es la forma de representar, por ejemplo, zonas, distritos y
  establecimientos de un sistema de salud.
- Las referencias permiten **buscar al revés**: `Organization?partof=X`
  devuelve todas las organizaciones que dependen de X.

## Ejercicios

### 04a · Crear a la médica

Incluye identificador, nombre con prefijo `Dra.`, correo de trabajo, sexo y la
calificación `MD`.

Solución: [`04a_practitioner_crear.json`](soluciones/04a_practitioner_crear.json)

### 04b y 04c · Crear la red y el hospital

Crea primero la red (`04b`) y guarda su `id`. Después crea el hospital (`04c`)
con `partOf` apuntando a la red: `"reference": "Organization/{{organizationId}}"`.

Soluciones: [`04b_organization_red.json`](soluciones/04b_organization_red.json) ·
[`04c_organization_hospital.json`](soluciones/04c_organization_hospital.json)

### 04d · Buscar los establecimientos de la red

`GET {{FHIRURL}}/Organization?partof={{organizationId}}`

## Para pensar

¿Por qué hay que crear la red **antes** que el hospital? ¿Cómo lo resolverías
en una sola transacción usando `urn:uuid` (módulo 03)?

## Ejecutar este módulo

- **Postman:** carpeta *04 · Profesionales y organizaciones*.
- **curl:** `curl/taller.sh 04`
- **R:** `fhir_crear("Practitioner", "modulos/04-profesionales-y-organizaciones/soluciones/04a_practitioner_crear.json", guarda = "practitionerId")`
