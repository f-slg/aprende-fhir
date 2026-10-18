# Módulo 04 · Profesionales y organizaciones

[← Módulo 03](../03-transacciones/README.md) · [Inicio](../../README.md) · [Módulo 05 →](../05-diagnostico-y-encuentro/README.md)

> **Nivel:** básico · **Duración:** 45 minutos · **Necesitas:** módulo 02

## Lo que vas a aprender

1. Qué son **Practitioner** y **Organization**, y en qué se diferencian.
2. A modelar la **jerarquía** de establecimientos con `partOf`.
3. A buscar recursos **por una referencia**.
4. Qué pasa si una referencia apunta a algo que no existe.

## La historia

Luis será atendido por la **Dra. Andrea Lucía Salazar Moreno**, médica
general (registro profesional ficticio `RP-000457`), en el **Hospital
General Docente Ejemplo**. El hospital pertenece a la **Red de Servicios de
Salud Ejemplo**. Las dos organizaciones son ficticias.

Antes de registrar la consulta hay que crear a la médica y a las
organizaciones, porque la consulta las va a referenciar.

---

## Ficha del recurso: Practitioner

**¿Qué es?** Una **persona** que presta servicios de salud: médicos,
enfermeras, odontólogos, técnicos, administrativos de salud.

**¿Para qué se usa?** Para decir **quién** hizo algo: quién atendió la
consulta (Encounter), quién registró el diagnóstico (Condition), quién midió
la presión (Observation), quién prescribió (MedicationRequest).

**¿Cuándo usar otro recurso?**

- **PractitionerRole**: el **rol** de esa persona en un lugar concreto (la
  Dra. Salazar es médica general en el Hospital Ejemplo los lunes y
  oncóloga en otra clínica). Practitioner es la persona; PractitionerRole,
  lo que hace y dónde.
- **RelatedPerson**: un familiar o cuidador del paciente.
- **Patient**: la persona que recibe atención.

**Elementos principales** (<https://hl7.org/fhir/R4/practitioner.html>):

<!-- ficha Practitioner -->
| Elemento | Card. | Tipo | Para qué sirve |
|---|---|---|---|
| `identifier` | 0..* | Identifier | Registro profesional, cédula, código institucional. |
| `active` | 0..1 | boolean | Si el registro está en uso. |
| `name` | 0..* | HumanName | Nombre, con prefijos como `Dr.` o `Dra.` en `prefix`. |
| `telecom` | 0..* | ContactPoint | Teléfono y correo de trabajo. |
| `address` | 0..* | Address | Dirección. |
| `gender` | 0..1 | code | Sexo administrativo. |
| `birthDate` | 0..1 | date | Fecha de nacimiento. |
| `qualification` | 0..* | BackboneElement | Títulos y certificaciones: medicina, especialidad, licencia. |
| `qualification.code` | **1..1** | CodeableConcept | Qué título es. |
| `communication` | 0..* | CodeableConcept | Idiomas que habla. |
<!-- /ficha -->

## Ficha del recurso: Organization

**¿Qué es?** Un **grupo formal** de personas: un hospital, un centro de
salud, un laboratorio, una red, un ministerio, una aseguradora.

**¿Para qué se usa?** Para decir **qué institución** presta el servicio
(`Encounter.serviceProvider`), **quién emite** un informe
(`DiagnosticReport.performer`) o **quién custodia** un documento.

**¿Cuándo usar otro recurso?** Para un **lugar físico** (una sala, un
consultorio, un quirófano) se usa **Location**. Organization es la
institución; Location, el sitio.

**Elementos principales** (<https://hl7.org/fhir/R4/organization.html>):

<!-- ficha Organization -->
| Elemento | Card. | Tipo | Para qué sirve |
|---|---|---|---|
| `identifier` | 0..* | Identifier | Código del establecimiento, RUC. |
| `active` ⚑ | 0..1 | boolean | Si la organización está en funcionamiento. |
| `type` | 0..* | CodeableConcept | Clase de organización: prestador (`prov`), aseguradora, gobierno... |
| `name` | 0..1 | string | Nombre oficial. |
| `alias` | 0..* | string | Otros nombres o siglas. |
| `telecom` | 0..* | ContactPoint | Teléfono, correo, web. |
| `address` | 0..* | Address | Dirección. |
| `partOf` | 0..1 | Reference(Organization) | La organización de la que forma parte. |
| `contact` | 0..* | BackboneElement | Personas de contacto (director, encargado). |
<!-- /ficha -->

Una regla de Organization: debe tener **al menos `name` o `identifier`**
(restricción `org-1`).

**Con qué se relacionan:** casi todos los recursos clínicos apuntan a un
Practitioner (quién) y a una Organization (dónde o en nombre de quién).

---

## Paso a paso: la médica

### Paso 1 · Quién es: identificador y nombre

<!-- paso 04a 1 -->
```json
{
  "resourceType": "Practitioner",
  "identifier": [
    {
      "use": "official",
      "system": "https://f-slg.github.io/aprende-fhir/sid/registro-profesional",
      "value": "RP-000457"
    }
  ],
  "name": [
    {
      "use": "official",
      "text": "Dra. Andrea Lucía Salazar Moreno",
      "prefix": [
        "Dra."
      ],
      "family": "Salazar Moreno",
      "given": [
        "Andrea",
        "Lucía"
      ]
    }
  ]
}
```
<!-- /paso -->

`prefix` va en una lista porque puede haber varios (`Dra.`, `MSc.`). El
registro profesional usa el mismo patrón `system` + `value` que la cédula.

### Paso 2 · Contacto y sexo

<!-- paso 04a 2 -->
```json
{
  "active": true,
  "telecom": [
    {
      "system": "email",
      "value": "andrea.salazar@hospital-ejemplo.invalid",
      "use": "work"
    }
  ],
  "gender": "female"
}
```
<!-- /paso -->

En `telecom`, `system` dice qué medio es (`phone`, `email`) y `use` para qué
(`work`, `home`, `mobile`). El dominio `.invalid` está reservado para
ejemplos: nunca llegará un correo.

### Paso 3 · Su título profesional

<!-- paso 04a 3 -->
```json
{
  "qualification": [
    {
      "code": {
        "coding": [
          {
            "system": "http://terminology.hl7.org/CodeSystem/v2-0360",
            "code": "MD",
            "display": "Doctor of Medicine"
          }
        ],
        "text": "Médica"
      }
    }
  ],
  "text": {
    "status": "generated",
    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><p>Dra. Andrea Lucía Salazar Moreno, médica general. Registro profesional ficticio RP-000457.</p></div>"
  }
}
```
<!-- /paso -->

`qualification.code` usa la tabla `v2-0360` de HL7, donde `MD` es *Doctor of
Medicine*. Solución completa:
[`04a_practitioner_crear.json`](soluciones/04a_practitioner_crear.json).

## Paso a paso: las organizaciones

### Paso 1 · La red: nombre e identificador

<!-- paso 04b 1 -->
```json
{
  "resourceType": "Organization",
  "identifier": [
    {
      "system": "https://f-slg.github.io/aprende-fhir/sid/establecimiento",
      "value": "RED-0001"
    }
  ],
  "name": "Red de Servicios de Salud Ejemplo"
}
```
<!-- /paso -->

### Paso 2 · Tipo y ubicación

<!-- paso 04b 2 -->
```json
{
  "active": true,
  "type": [
    {
      "coding": [
        {
          "system": "http://terminology.hl7.org/CodeSystem/organization-type",
          "code": "prov",
          "display": "Healthcare Provider"
        }
      ]
    }
  ],
  "address": [
    {
      "city": "Quito",
      "state": "Pichincha",
      "country": "EC"
    }
  ],
  "text": {
    "status": "generated",
    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><p>Red de Servicios de Salud Ejemplo (organización ficticia).</p></div>"
  }
}
```
<!-- /paso -->

`type` con el código `prov` (*Healthcare Provider*) indica que presta
servicios de salud. Solución: [`04b_organization_red.json`](soluciones/04b_organization_red.json).

### El hospital: igual que la red, más `partOf`

El hospital se construye igual que la red. Lo nuevo es `partOf`, que apunta
a la red recién creada. Esto es lo que cambia respecto de la red:

<!-- diferencia 04c -->
```json
{
  "identifier": [
    {
      "system": "https://f-slg.github.io/aprende-fhir/sid/establecimiento",
      "value": "HGDE-0001"
    }
  ],
  "name": "Hospital General Docente Ejemplo",
  "telecom": [
    {
      "system": "phone",
      "value": "+593 2 000 0000",
      "use": "work"
    }
  ],
  "address": [
    {
      "line": [
        "Av. Principal Ejemplo S00-00"
      ],
      "city": "Quito",
      "state": "Pichincha",
      "country": "EC"
    }
  ],
  "partOf": {
    "reference": "Organization/{{organizationId}}",
    "display": "Red de Servicios de Salud Ejemplo"
  }
}
```
<!-- /diferencia -->

Solución: [`04c_organization_hospital.json`](soluciones/04c_organization_hospital.json).

---

## Ejercicios en el servidor

### 04a · Crear a la médica

```http
POST {{FHIRURL}}/Practitioner
```

Guarda el `id` en `practitionerId`.

### 04b y 04c · Crear la red y luego el hospital

El orden importa: primero la red (`POST {{FHIRURL}}/Organization`, guarda
`organizationId`) y después el hospital, cuyo `partOf` apunta a
`Organization/{{organizationId}}` (guarda `hospitalId`).

### 04d · Los establecimientos de la red

```http
GET {{FHIRURL}}/Organization?partof={{organizationId}}
```

Es una **búsqueda por referencia**: "las organizaciones cuyo `partOf` es la
red". Devuelve el hospital. Así se recorre una jerarquía hacia abajo, por
ejemplo de una zona a sus distritos y de los distritos a sus
establecimientos.

### 04e · Error a propósito: una referencia a algo que no existe

Envía ([`04e1_referencia_inexistente.json`](errores/04e1_referencia_inexistente.json)):

```json
{ "resourceType": "Organization", "name": "Centro de Salud Ejemplo",
  "partOf": { "reference": "Organization/no-existe-123" } }
```

El servidor responde **`400`**:

```
HAPI-1094: Resource Organization/no-existe-123 not found, specified in path: Organization.partOf
```

El servidor comprueba que las referencias apunten a recursos que existen
(**integridad referencial**). Fíjate que el recurso en sí es válido: el
validador no lo detecta, porque no consulta el servidor. Es un error que solo
ve el servidor.

## Autoevaluación

<details><summary>1. La Dra. Salazar atiende en dos hospitales. ¿Cuántos Practitioner necesitas?</summary>

Uno solo: es la misma persona. Lo que cambia es su rol en cada lugar, que se
modela con un **PractitionerRole** por hospital.
</details>

<details><summary>2. ¿Organization o Location para el "Consultorio 3 de Medicina General"?</summary>

**Location**: es un lugar físico. La organización es el hospital al que
pertenece el consultorio.
</details>

<details><summary>3. ¿Por qué hay que crear la red antes que el hospital?</summary>

Porque el hospital la referencia con `partOf`, y el servidor exige que el
recurso referenciado exista. Otra opción es enviar ambos en una transacción
usando `urn:uuid:` (módulo 03).
</details>

## Resumen

- **Practitioner** es la persona que presta servicios; **PractitionerRole**,
  su rol en un lugar.
- **Organization** es la institución; **Location**, el lugar físico.
- `partOf` construye jerarquías y se recorre con búsquedas por referencia.
- El servidor verifica que las referencias existan.

## Ejecutar este módulo

- **Postman:** carpeta *04 · Profesionales y organizaciones*.
- **curl:** `curl/taller.sh 04`
- **R:**

  ```r
  dir <- "modulos/04-profesionales-y-organizaciones/soluciones/"
  fhir_crear("Practitioner", paste0(dir, "04a_practitioner_crear.json"), guarda = "practitionerId")
  fhir_crear("Organization", paste0(dir, "04b_organization_red.json"), guarda = "organizationId")
  fhir_crear("Organization", paste0(dir, "04c_organization_hospital.json"), guarda = "hospitalId")
  fhir_tabla(fhir_buscar("Organization?partof={{organizationId}}"),
             list(nombre = function(r) r$name))
  ```
