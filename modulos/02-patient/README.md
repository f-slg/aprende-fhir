# Módulo 02 · Patient: el paciente

[← Módulo 01](../01-fundamentos/README.md) · [Inicio](../../README.md) · [Módulo 03 →](../03-transacciones/README.md)

> **Nivel:** básico · **Duración:** 60 minutos · **Necesitas:** módulo 01

## Lo que vas a aprender

1. Qué es el recurso **Patient**, para qué se usa y qué contiene.
2. A construirlo **paso a paso**, desde un paciente vacío hasta uno completo.
3. A crearlo, leerlo, buscarlo y actualizarlo en el servidor.
4. A ver su **historial de versiones**.

## La historia

**Luis Alberto Paredes Cevallos** nació el 12 de marzo de 1979 en Riobamba y
vive en Quito. Llega por primera vez al *Hospital General Docente Ejemplo*.
Antes de cualquier atención, hay que registrarlo: en FHIR eso es crear su
recurso **Patient**.

Sus datos (ficticios):

| Dato | Valor |
|---|---|
| Cédula | `9900000017` (empieza con `99`, un código de provincia que no existe) |
| Historia clínica | `HC-000123` |
| Nombre | Luis Alberto Paredes Cevallos; le dicen Luis Paredes |
| Sexo / nacimiento | masculino · 12 de marzo de 1979, en Riobamba (Chimborazo) |
| Dirección | Av. de los Ejemplos N00-00 y calle Ficticia, Quito |
| Idioma | español |

---

## Ficha del recurso: Patient

**¿Qué es?** El registro **demográfico y administrativo** de una persona que
recibe atención de salud: quién es, cómo se le identifica y cómo se le
contacta. No contiene información clínica.

**¿Para qué se usa?** Es el centro de casi todo en FHIR. Las consultas, los
diagnósticos, los signos vitales, las vacunas y las recetas apuntan a un
Patient con una referencia (`subject` o `patient`). Por eso es lo primero que
se crea.

**¿Cuándo usar otro recurso?**

- Para un profesional de salud: **Practitioner** (módulo 04).
- Para un familiar o contacto del paciente: **RelatedPerson**, o el elemento
  `contact` del propio Patient.
- Para los diagnósticos, alergias o antecedentes: recursos clínicos como
  **Condition** o **AllergyIntolerance**, que apuntan al Patient. Nunca dentro
  de él.

**Elementos principales** (especificación completa:
<https://hl7.org/fhir/R4/patient.html>):

<!-- ficha Patient -->
| Elemento | Card. | Tipo | Para qué sirve |
|---|---|---|---|
| `identifier` | 0..* | Identifier | Identificadores del mundo real: cédula, historia clínica, pasaporte. |
| `active` ⚑ | 0..1 | boolean | Si el registro está en uso. Se pone `false` cuando se fusionan duplicados. |
| `name` | 0..* | HumanName | Nombres de la persona: oficial, de uso habitual, de soltera... |
| `telecom` | 0..* | ContactPoint | Teléfonos y correos. |
| `gender` | 0..1 | code | Sexo administrativo: `male`, `female`, `other` o `unknown`. |
| `birthDate` | 0..1 | date | Fecha de nacimiento (año-mes-día). |
| `deceased[x]` ⚑ | 0..1 | boolean \| dateTime | Si falleció: `true`/`false` o la fecha de fallecimiento. |
| `address` | 0..* | Address | Direcciones de domicilio o de trabajo. |
| `maritalStatus` | 0..1 | CodeableConcept | Estado civil. |
| `contact` | 0..* | BackboneElement | Personas de contacto: familiar, tutor, a quién avisar. |
| `communication` | 0..* | BackboneElement | Idiomas que habla y cuál prefiere. |
| `generalPractitioner` | 0..* | Reference(Organization \| Practitioner \| PractitionerRole) | Su médico o centro de salud de cabecera. |
| `managingOrganization` | 0..1 | Reference(Organization) | La organización que custodia este registro. |
| `link` ⚑ | 0..* | BackboneElement | Enlaces a otros registros de la misma persona (duplicados fusionados). |
<!-- /ficha -->

**Ningún elemento es obligatorio**: un `{"resourceType": "Patient"}` es
válido. En la práctica, cada país o programa define con un **perfil** qué
datos exige (por ejemplo, cédula, nombre, sexo y fecha de nacimiento).

**Con qué se relaciona:** todos los recursos clínicos apuntan al Patient.
Él solo apunta, si acaso, a su médico de cabecera y a la organización que lo
custodia.

---

## Paso a paso: construir el paciente

Vas a construir el recurso de a poco. Cada paso es un recurso **válido**: si
quieres, envíalo al servidor o valídalo antes de seguir. Todas las versiones
intermedias están en [`pasos/`](pasos/).

### Paso 1 · El mínimo: un paciente vacío

<!-- paso 02a 1 -->
```json
{
  "resourceType": "Patient"
}
```
<!-- /paso -->

Es válido, pero no sirve de nada: no sabemos quién es. `resourceType` es lo
único que todo recurso lleva siempre.

### Paso 2 · Los identificadores: cédula e historia clínica

<!-- paso 02a 2 -->
```json
{
  "identifier": [
    {
      "use": "official",
      "type": {
        "coding": [
          {
            "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
            "code": "NI",
            "display": "National unique individual identifier"
          }
        ],
        "text": "Cédula de identidad"
      },
      "system": "https://f-slg.github.io/aprende-fhir/sid/cedula",
      "value": "9900000017"
    },
    {
      "use": "usual",
      "type": {
        "coding": [
          {
            "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
            "code": "MR",
            "display": "Medical record number"
          }
        ],
        "text": "Historia clínica"
      },
      "system": "https://f-slg.github.io/aprende-fhir/sid/historia-clinica/hospital-general-docente-ejemplo",
      "value": "HC-000123"
    }
  ]
}
```
<!-- /paso -->

Cada identificador tiene cuatro partes:

- `system`: **quién emite** el identificador, expresado como una dirección
  única. Aquí usamos direcciones didácticas del taller; en un sistema real se
  usa la que defina la guía nacional (por ejemplo, la del Registro Civil para
  la cédula).
- `value`: el número.
- `type`: **qué clase** de identificador es, con la tabla `v2-0203` de HL7:
  `NI` (identificador nacional) para la cédula y `MR` (*medical record*) para
  la historia clínica.
- `use`: `official` para la cédula y `usual` para el que se usa a diario.

La pareja **`system` + `value`** identifica a la persona sin ambigüedad. Con
ella se busca al paciente en el ejercicio 02c.

> **Sobre un aviso del validador.** Al validar verás: *"None of the codings
> provided are in the value set 'IdentifierType'"*. La lista sugerida de FHIR
> R4 para `type` no incluye `NI`. Esa lista es **extensible**: se puede usar
> otro código cuando ninguno de la lista sirve, y para una cédula ninguno
> sirve. Es un aviso, no un error.

### Paso 3 · El nombre, primero simple

<!-- paso 02a 3 -->
```json
{
  "name": [
    {
      "use": "official",
      "text": "Luis Alberto Paredes Cevallos",
      "family": "Paredes Cevallos",
      "given": [
        "Luis",
        "Alberto"
      ]
    }
  ]
}
```
<!-- /paso -->

`family` es el apellido y `given` la lista de nombres de pila. `text` es el
nombre completo como se escribe. `name` es una lista (`0..*`), porque una
persona puede tener varios nombres.

### Paso 4 · Los dos apellidos y el nombre de uso habitual

<!-- paso 02a 4 -->
```json
{
  "name": [
    {
      "use": "official",
      "text": "Luis Alberto Paredes Cevallos",
      "family": "Paredes Cevallos",
      "_family": {
        "extension": [
          {
            "url": "http://hl7.org/fhir/StructureDefinition/humanname-fathers-family",
            "valueString": "Paredes"
          },
          {
            "url": "http://hl7.org/fhir/StructureDefinition/humanname-mothers-family",
            "valueString": "Cevallos"
          }
        ]
      },
      "given": [
        "Luis",
        "Alberto"
      ]
    },
    {
      "use": "usual",
      "text": "Luis Paredes"
    }
  ]
}
```
<!-- /paso -->

En Ecuador usamos dos apellidos, pero `family` es un solo texto. FHIR lo
resuelve con **extensiones**, elementos adicionales definidos por HL7 para
lo que no está en el recurso base:

- `humanname-fathers-family`: apellido paterno.
- `humanname-mothers-family`: apellido materno.

Las extensiones de un valor simple como `family` van en un elemento hermano
con guion bajo: `_family`. Además agregamos un segundo nombre con
`use: "usual"`: *Luis Paredes*, como lo conocen todos.

### Paso 5 · Datos demográficos

<!-- paso 02a 5 -->
```json
{
  "active": true,
  "gender": "male",
  "birthDate": "1979-03-12"
}
```
<!-- /paso -->

- `gender` es un **code**: solo admite `male`, `female`, `other` o
  `unknown`, en inglés. `"masculino"` lo rechaza el servidor.
- `birthDate` es una **date**: siempre `AAAA-MM-DD`.
- `active: true` indica que el registro está en uso.

### Paso 6 · Dirección, idioma y lugar de nacimiento

<!-- paso 02a 6 -->
```json
{
  "address": [
    {
      "use": "home",
      "type": "physical",
      "line": [
        "Av. de los Ejemplos N00-00 y calle Ficticia"
      ],
      "city": "Quito",
      "district": "Quito",
      "state": "Pichincha",
      "country": "EC"
    }
  ],
  "communication": [
    {
      "language": {
        "coding": [
          {
            "system": "urn:ietf:bcp:47",
            "code": "es",
            "display": "Spanish"
          }
        ],
        "text": "Español"
      },
      "preferred": true
    }
  ],
  "extension": [
    {
      "url": "http://hl7.org/fhir/StructureDefinition/patient-birthPlace",
      "valueAddress": {
        "city": "Riobamba",
        "state": "Chimborazo",
        "country": "EC"
      }
    }
  ]
}
```
<!-- /paso -->

- `address`: `use` (domicilio) y `type` (dirección física), con calle,
  ciudad, provincia (`state`) y país (`EC`, código ISO).
- `communication.language`: el idioma con el código `es` de la norma BCP 47;
  `preferred: true` indica que es el que prefiere.
- `extension` con `patient-birthPlace`: el lugar de nacimiento no está en
  Patient, así que también se registra con una extensión estándar. Fíjate
  que va en `extension` del recurso, no en `_family`.

### Paso 7 · La narrativa

<!-- paso 02a 7 -->
```json
{
  "text": {
    "status": "generated",
    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><p>Luis Alberto Paredes Cevallos, hombre, nacido el 12 de marzo de 1979 en Riobamba.</p><p>Cédula ficticia 9900000017 · Historia clínica HC-000123.</p></div>"
  }
}
```
<!-- /paso -->

`text` es un resumen para personas en HTML. `status: "generated"` indica que
se generó a partir de los datos estructurados. El `div` debe llevar
`xmlns="http://www.w3.org/1999/xhtml"`. Con este paso el recurso queda
completo: es la solución [`02a_patient_crear.json`](soluciones/02a_patient_crear.json).

---

## Ejercicios en el servidor

### 02a · Crear el paciente

```http
POST {{FHIRURL}}/Patient
Content-Type: application/fhir+json

(el recurso del paso 7)
```

Respuesta esperada: **`201 Created`**. En el cuerpo verás el recurso con dos
cosas nuevas: `id` (por ejemplo `1000`) y `meta` (versión `1` y fecha). En
Postman, el `id` se guarda solo en la variable `patientId`.

### 02b · Leerlo

```http
GET {{FHIRURL}}/Patient/{{patientId}}
```

Compara lo que enviaste con lo que devuelve. ¿Está todo? ¿Qué agregó el
servidor?

### 02c · Buscarlo por cédula

```http
GET {{FHIRURL}}/Patient?identifier=https://f-slg.github.io/aprende-fhir/sid/cedula|9900000017
```

El parámetro `identifier` usa el formato `system|value`. Devuelve un `Bundle`
con un solo resultado.

### 02d · Buscarlo por nombre

```http
GET {{FHIRURL}}/Patient?family=Paredes&given=Luis
```

Los parámetros se combinan con `&` (y lógico). La búsqueda por texto no es
exacta: `family=Pare` también encuentra a Paredes. Por eso, para encontrar a
una persona concreta, la búsqueda segura es por identificador.

### 02e · Actualizarlo

Luis da su teléfono, `+593 99 000 0000`, y su estado civil: casado. Se envía
con `PUT` **el recurso completo**, con su `id`. Esto es lo que cambia
respecto del paso 7 (además de la narrativa):

<!-- diferencia 02e -->
```json
{
  "id": "{{patientId}}",
  "telecom": [
    {
      "system": "phone",
      "value": "+593 99 000 0000",
      "use": "mobile"
    }
  ],
  "maritalStatus": {
    "coding": [
      {
        "system": "http://terminology.hl7.org/CodeSystem/v3-MaritalStatus",
        "code": "M",
        "display": "Married"
      }
    ],
    "text": "Casado"
  }
}
```
<!-- /diferencia -->

```http
PUT {{FHIRURL}}/Patient/{{patientId}}
```

Solución completa: [`02e_patient_actualizar.json`](soluciones/02e_patient_actualizar.json).

> **`PUT` reemplaza todo.** Si en la actualización olvidas la dirección, el
> servidor guarda un paciente **sin dirección**. No es un error: es lo que le
> pediste.

### 02f · El historial

```http
GET {{FHIRURL}}/Patient/{{patientId}}/_history
```

Devuelve un `Bundle` de tipo `history` con las dos versiones. Mira
`meta.versionId` (`1` y `2`) y `meta.lastUpdated`. Nada se pierde: siempre
puedes saber qué decía el registro antes de un cambio.

### 02g · Error a propósito: la fecha con formato local

Envía ([`02e1_fecha_formato_local.json`](errores/02e1_fecha_formato_local.json)):

```json
{ "resourceType": "Patient", "name": [ { "text": "Luis Alberto Paredes Cevallos" } ], "birthDate": "12/03/1979" }
```

El servidor responde **`400`**:

```
HAPI-1821: [element="birthDate"] Invalid attribute value "12/03/1979": Invalid date/time format
```

En FHIR, las fechas siempre van como `1979-03-12`. Así no hay dudas de si
`12/03` es el 12 de marzo o el 3 de diciembre.

## Autoevaluación

<details><summary>1. ¿Por qué el nombre usa extensiones para los dos apellidos?</summary>

Porque `HumanName.family` es un solo texto. Las extensiones estándar
`humanname-fathers-family` y `humanname-mothers-family` permiten guardar cada
apellido por separado sin perder el texto completo.
</details>

<details><summary>2. Envías un <code>PUT</code> solo con el teléfono nuevo. ¿Qué pasa con el nombre y la cédula?</summary>

Se pierden: `PUT` reemplaza el recurso completo por lo que envíes. Siempre se
envía el recurso entero, con su `id`.
</details>

<details><summary>3. ¿Qué búsqueda usarías para no confundir a Luis con otro paciente del mismo nombre?</summary>

La búsqueda por identificador: `Patient?identifier=<system>|<valor de la cédula>`.
</details>

<details><summary>4. ¿Dónde registrarías que Luis es alérgico a la penicilina?</summary>

En un recurso **AllergyIntolerance** que apunte a Luis, no dentro del Patient
(módulo 07).
</details>

## Resumen

- **Patient** guarda la identidad y los datos administrativos; nada clínico.
- La pareja `system` + `value` del `identifier` identifica a la persona.
- Las **extensiones** agregan lo que el recurso base no tiene, como los dos
  apellidos o el lugar de nacimiento.
- `PUT` reemplaza el recurso completo y crea una nueva versión;
  `_history` muestra todas.

## Ejecutar este módulo

- **Postman:** carpeta *02 · Patient*.
- **curl:** `curl/taller.sh 02`
- **R:**

  ```r
  source("r/fhir.R")
  p <- fhir_crear("Patient", "modulos/02-patient/soluciones/02a_patient_crear.json",
                  guarda = "patientId")
  p$id
  fhir_actualizar("Patient/{{patientId}}", "modulos/02-patient/soluciones/02e_patient_actualizar.json")
  fhir_leer("Patient/{{patientId}}/_history")$total
  ```
