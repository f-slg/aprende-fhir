# Módulo 01 · Fundamentos

[← Inicio](../../README.md) · [Módulo 02 →](../02-patient/README.md)

> **Nivel:** básico · **Duración:** 45 minutos · **Necesitas:** Postman, R o una
> terminal con curl (ver [Elige tu camino](../../README.md#elige-tu-camino))

## Lo que vas a aprender

1. Qué es HL7 FHIR y qué problema resuelve.
2. Qué es un **recurso** y cómo se lee en JSON.
3. Los **tipos de datos** que se repiten en todos los recursos.
4. Cómo leer la **cardinalidad** (`0..1`, `1..*`) en la especificación.
5. Las operaciones **REST**: crear, leer, actualizar, buscar y borrar.
6. Cómo interpretar las respuestas del servidor, incluidos los errores.

---

## 1. ¿Qué es FHIR y para qué sirve?

Un hospital, un centro de salud, un laboratorio y el sistema de vigilancia
epidemiológica guardan información del mismo paciente, cada uno en su propio
sistema. Para que esa información viaje de uno a otro sin volver a
digitarla, los sistemas necesitan hablar un **idioma común**: qué datos se
envían, con qué nombres, con qué códigos y cómo se piden. Eso es la
**interoperabilidad**.

**HL7 FHIR** (*Fast Healthcare Interoperability Resources*, se pronuncia
"fáier") es ese idioma común. Lo publica HL7 International y hoy es el
estándar más usado en el mundo para intercambiar información de salud. Se
basa en tres ideas:

| Idea | Qué significa |
|---|---|
| **Recursos** | La información se divide en piezas pequeñas y reutilizables: un paciente, una consulta, una presión arterial, una vacuna. |
| **Web** | Los recursos se piden y se envían por internet, igual que una página web, con una API REST. |
| **Terminologías** | Los datos clínicos se codifican con vocabularios estándar (LOINC, SNOMED CT, CIE-10) para que todos entiendan lo mismo. |

FHIR tiene varias versiones. Este taller usa **R4 (4.0.1)**, la más
implementada en el mundo. La especificación completa está en
<https://hl7.org/fhir/R4/>.

## 2. Los recursos

Un **recurso** es la unidad básica de información. FHIR R4 define más de 140,
agrupados por tema:

| Grupo | Ejemplos | En este taller |
|---|---|---|
| Administración | Patient, Practitioner, PractitionerRole, Organization, Location, Encounter | Módulos 02, 04, 05, 10 |
| Agenda | Schedule, Slot, Appointment, AppointmentResponse | Módulo 14 |
| Clínicos | Condition, AllergyIntolerance, FamilyMemberHistory, Procedure | Módulos 05, 07, 13 |
| Planificación | ServiceRequest, CarePlan, CareTeam, Goal | Módulos 10, 12 |
| Diagnóstico | Observation, DiagnosticReport, Specimen, BodyStructure | Módulos 06, 10, 11 |
| Medicación | MedicationRequest, MedicationAdministration, MedicationStatement, Immunization | Módulos 07, 08, 15 |
| Documentos y formularios | Composition, Bundle, Questionnaire, QuestionnaireResponse, Consent | Módulos 03, 09, 12, 16 |
| Infraestructura | CapabilityStatement, OperationOutcome | Este módulo |

Todos los recursos comparten la misma **anatomía**:

```json
{
  "resourceType": "Patient",
  "id": "1000",
  "meta": { "versionId": "2", "lastUpdated": "2025-03-20T08:15:00-05:00" },
  "text": { "status": "generated", "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\">Luis Paredes</div>" },
  "identifier": [ { "system": "https://…/cedula", "value": "9900000017" } ],
  "name": [ { "family": "Paredes Cevallos", "given": ["Luis", "Alberto"] } ]
}
```

| Parte | Quién la pone | Para qué |
|---|---|---|
| `resourceType` | Tú | Dice qué tipo de recurso es. Siempre va y debe estar escrito exactamente así. |
| `id` | El servidor | El identificador del recurso **dentro de ese servidor**. Lo asigna al crearlo. |
| `meta` | El servidor | Versión, fecha de la última modificación y perfiles. |
| `text` | Tú | La **narrativa**: un resumen en HTML para personas. Los sistemas lo muestran cuando no entienden el resto. |
| `identifier` | Tú | Identificadores del **mundo real**: cédula, historia clínica, número de muestra. |
| El resto | Tú | Los datos propios de cada recurso. |

> **`id` no es lo mismo que `identifier`.** El `id` (`1000`) solo vale en un
> servidor; si el paciente se registra en otro, tendrá otro `id`. El
> `identifier` (la cédula) es el mismo en todas partes. Por eso para
> encontrar a una persona se busca por `identifier`.

Los recursos se **enlazan** con referencias. Así una observación dice de
qué paciente es:

```json
"subject": { "reference": "Patient/1000", "display": "Luis Alberto Paredes Cevallos" }
```

En el taller verás referencias como `"Patient/{{patientId}}"`. `{{patientId}}`
es un **marcador**: Postman, R y curl lo reemplazan por el `id` real que
devolvió el servidor al crear el paciente.

## 3. Los tipos de datos

Los elementos de los recursos usan unos pocos **tipos de datos** que se
repiten en todas partes. Conocerlos es la mitad del camino.

**Tipos simples (primitivos):**

| Tipo | Ejemplo | Cuidado con... |
|---|---|---|
| `string` | `"Luis"` | Texto libre. |
| `boolean` | `true` | Sin comillas. |
| `integer`, `decimal` | `20`, `38.4` | Sin comillas y con **punto** decimal, nunca coma. |
| `date` | `"1979-03-12"` | Siempre año-mes-día. También vale `"1979-03"` o `"1979"`. |
| `dateTime` | `"2025-03-20T07:15:00-05:00"` | Con hora debe llevar la zona horaria (Ecuador continental: `-05:00`). |
| `code` | `"male"` | Un valor de una lista cerrada, escrito exactamente como dice la especificación (en inglés). |
| `uri` | `"http://loinc.org"` | Una dirección que identifica algo; no tiene que abrirse en el navegador. |

**Tipos compuestos:**

| Tipo | Para qué | Ejemplo |
|---|---|---|
| `Identifier` | Un identificador del mundo real | `{"system": "https://…/cedula", "value": "9900000017"}` |
| `HumanName` | Un nombre de persona | `{"family": "Paredes Cevallos", "given": ["Luis", "Alberto"]}` |
| `Address`, `ContactPoint` | Dirección, teléfono o correo | `{"system": "phone", "value": "+593 99 000 0000"}` |
| `Coding` | **Un** código de una terminología | `{"system": "http://loinc.org", "code": "8310-5", "display": "Body temperature"}` |
| `CodeableConcept` | Un concepto: uno o varios `Coding` más un texto | `{"coding": [ … ], "text": "Temperatura corporal"}` |
| `Quantity` | Una cantidad con unidad | `{"value": 38.4, "unit": "°C", "system": "http://unitsofmeasure.org", "code": "Cel"}` |
| `Reference` | Un enlace a otro recurso | `{"reference": "Patient/1000"}` |
| `Period` | Un intervalo de tiempo | `{"start": "2025-03-20T07:15:00-05:00", "end": "…"}` |

`CodeableConcept` es el tipo más importante de FHIR: es la forma de registrar
casi todo lo clínico. Tiene un `text` para lo que lee la persona y uno o
varios `coding` para lo que entienden las máquinas.

## 4. Cómo leer la cardinalidad

En la especificación, y en las fichas de cada módulo de este taller, cada
elemento tiene una **cardinalidad**: cuántas veces puede aparecer.

| Cardinalidad | Significa | En JSON |
|---|---|---|
| `0..1` | Opcional, como mucho una vez | un valor: `"gender": "male"` |
| `1..1` | **Obligatorio**, exactamente una vez | un valor que no puede faltar |
| `0..*` | Opcional, puede repetirse | una **lista** entre corchetes: `"name": [ … ]` |
| `1..*` | **Obligatorio**, al menos uno | una lista que no puede estar vacía |

En las fichas, los elementos obligatorios aparecen en **negrita** y los
marcados con ⚑ son **modificadores**: cambian el significado de todo el
recurso. Por ejemplo, `status = "entered-in-error"` significa que el registro
fue un error, y un sistema que lo ignore entendería lo contrario.

Dos reglas de JSON en FHIR que evitan muchos errores:

- Si un elemento no tiene valor, **no se escribe**: nada de `""`, `null` ni `[]`.
- Si la cardinalidad termina en `*`, el valor va **siempre** entre corchetes,
  aunque sea uno solo.

## 5. La API REST

Cada tipo de recurso tiene su dirección en el servidor. Las operaciones son
los métodos de HTTP:

| Quiero... | Método y ruta | Cuerpo | Respuesta si sale bien |
|---|---|---|---|
| Crear | `POST /Patient` | El recurso, sin `id` | `201 Created` y el recurso con su `id` |
| Leer | `GET /Patient/1000` | — | `200 OK` |
| Actualizar | `PUT /Patient/1000` | El recurso **completo**, con su `id` | `200 OK` y una nueva versión |
| Borrar | `DELETE /Patient/1000` | — | `200 OK` |
| Buscar | `GET /Patient?family=Paredes` | — | `200 OK` y un `Bundle` con los resultados |
| Ver el historial | `GET /Patient/1000/_history` | — | `200 OK` y todas las versiones |
| Ver qué sabe hacer el servidor | `GET /metadata` | — | `200 OK` y un `CapabilityStatement` |

En todas las peticiones se envía el encabezado
`Accept: application/fhir+json`, y en las que llevan cuerpo,
`Content-Type: application/fhir+json`. Postman, R y curl ya lo hacen por ti.

**Códigos de respuesta** que verás:

| Código | Significa |
|---|---|
| `200 OK` | La operación salió bien. |
| `201 Created` | Se creó el recurso. Mira el `id` en la respuesta. |
| `400 Bad Request` | El servidor no aceptó lo que enviaste: JSON mal formado, un valor inválido o una referencia a algo que no existe. |
| `404 Not Found` | No existe un recurso con ese `id`. |
| `410 Gone` | El recurso existió pero fue borrado. |
| `422 Unprocessable Entity` | El recurso se entendió pero no cumple las reglas del servidor. |

Cuando algo sale mal, el servidor responde con un **`OperationOutcome`**: un
recurso que explica el problema.

```json
{
  "resourceType": "OperationOutcome",
  "issue": [ {
    "severity": "error",
    "code": "processing",
    "diagnostics": "HAPI-1814: Incorrect resource type found, expected \"Patient\" but found \"Paciente\""
  } ]
}
```

Lee siempre `issue[].diagnostics`: casi siempre dice exactamente qué está mal.

---

## Ejercicios

### 01a · ¿Qué sabe hacer el servidor?

```http
GET {{FHIRURL}}/metadata
```

La respuesta es un **CapabilityStatement**: la "hoja de vida" del servidor.
Búscalo en la respuesta:

1. `fhirVersion`: ¿qué versión de FHIR implementa? Debe decir `4.0.1`.
2. `software.name`: ¿qué programa es?
3. En `rest[0].resource`, busca el que tiene `"type": "Patient"`. En
   `interaction` verás las operaciones que admite (`read`, `create`,
   `update`, `delete`, `search-type`...) y en `searchParam`, los parámetros
   de búsqueda (`family`, `birthdate`, `identifier`...).

### 01b · Tu primera búsqueda

```http
GET {{FHIRURL}}/Patient?_count=5
```

La respuesta es un `Bundle` de tipo `searchset`:

- `total`: cuántos pacientes hay en el servidor (algunos servidores no lo informan);
- `link`: las direcciones para ver la página siguiente (`next`);
- `entry`: los resultados; cada uno tiene `fullUrl` y `resource`.

`_count` empieza con guion bajo porque es un parámetro **general**: sirve en
cualquier tipo de recurso, igual que `_id`, `_sort` o `_include`.

> **En un servidor público verás pacientes de otras personas,** y todo lo que
> subas lo verán los demás. Usa solo datos ficticios, como los de este
> taller.

### 01c · Error a propósito: el tipo de recurso en español

Envía con `POST {{FHIRURL}}/Patient` este recurso
([`01e1_resourcetype_en_espanol.json`](errores/01e1_resourcetype_en_espanol.json)):

```json
{ "resourceType": "Paciente", "gender": "male" }
```

El servidor responde **`400`**:

```
HAPI-1814: Incorrect resource type found, expected "Patient" but found "Paciente"
```

Los nombres de recursos, elementos y códigos de FHIR son **siempre en
inglés** y distinguen mayúsculas: `Patient`, no `Paciente` ni `patient`. Lo
que sí va en español es el contenido: nombres, textos, narrativa.

### 01d y 01e · Error a propósito: un elemento en español

Ahora envía ([`01e2_elemento_en_espanol.json`](errores/01e2_elemento_en_espanol.json)):

```json
{ "resourceType": "Patient", "nombre": [ { "text": "Luis Alberto Paredes Cevallos" } ], "gender": "male" }
```

**El servidor responde `201 Created`.** Parece que salió bien, pero lee lo
que guardó con `GET {{FHIRURL}}/Patient/{{errorPatientId}}`: el paciente
**no tiene nombre**. El servidor ignoró `nombre` porque no es un elemento de
FHIR, y no avisó.

Esta es la lección más importante del módulo: **que el servidor acepte un
recurso no significa que el recurso sea correcto.** Muchos servidores son
tolerantes y descartan en silencio lo que no entienden. Por eso, antes de
enviar algo, se **valida** con el validador oficial de HL7, que sí detecta el
problema:

```
Patient | Unrecognized property 'nombre'
```

Puedes validar cualquier recurso pegándolo en <https://validator.fhir.org/>,
o todos los del taller con `herramientas/validar.sh` (ver
[Validar tus recursos](../../README.md#validar-tus-recursos)).

### 01f · Borrar el paciente de prueba

```http
DELETE {{FHIRURL}}/Patient/{{errorPatientId}}
```

Si después intentas leerlo, el servidor responde `410 Gone`: el recurso
existió, pero se borró.

## Dos tipos de errores

A lo largo del taller, cada módulo tiene un **error a propósito**. Son de dos
tipos, y conviene distinguirlos desde ahora:

| | El servidor... | Ejemplos | Cómo se detecta |
|---|---|---|---|
| **Error de formato** | lo rechaza con `400` | tipo de recurso mal escrito, fecha `12/03/1979`, decimal `38,4`, un código que no existe | lo ves en la respuesta |
| **Error de contenido** | lo **acepta** | elemento desconocido, falta un elemento obligatorio, código con nombre equivocado | solo con el **validador** |

## Autoevaluación

<details><summary>1. ¿Qué diferencia hay entre <code>id</code> e <code>identifier</code>?</summary>

El `id` lo asigna el servidor y solo vale en ese servidor. El `identifier`
es un identificador del mundo real (cédula, historia clínica) que es el
mismo en todos los sistemas.
</details>

<details><summary>2. Un elemento tiene cardinalidad <code>0..*</code>. ¿Cómo se escribe si tiene un solo valor?</summary>

Como lista: `"name": [ { … } ]`. Los elementos que pueden repetirse van
siempre entre corchetes.
</details>

<details><summary>3. ¿Cómo se escribe la temperatura 38,4 °C en un <code>valueQuantity</code>?</summary>

`{"value": 38.4, "unit": "°C", "system": "http://unitsofmeasure.org", "code": "Cel"}`:
número con punto decimal y sin comillas.
</details>

<details><summary>4. El servidor respondió <code>201 Created</code>. ¿Ya sé que mi recurso es correcto?</summary>

No. Solo sabes que el servidor lo guardó. Puede haber descartado elementos o
aceptado un recurso al que le falta algo obligatorio. Para saberlo hay que
validarlo.
</details>

## Resumen

- FHIR divide la información de salud en **recursos** que se enlazan con
  **referencias** y se intercambian por una **API REST**.
- Todo recurso tiene `resourceType`; el servidor agrega `id` y `meta`.
- Los tipos de datos más usados son `CodeableConcept`, `Identifier`,
  `Reference` y `Quantity`.
- La cardinalidad dice si un elemento es obligatorio y si se repite.
- Los nombres de FHIR van en inglés y los contenidos en español.
- Un `201` no garantiza que el recurso sea correcto: **valida siempre**.

## Ejecutar este módulo

- **Postman:** carpeta *01 · Fundamentos*.
- **curl:** `curl/taller.sh 01`
- **R:**

  ```r
  source("r/fhir.R")
  capacidades <- fhir_leer("metadata")
  capacidades$fhirVersion
  capacidades$software$name
  ```
