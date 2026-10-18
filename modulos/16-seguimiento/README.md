# Módulo 16 · Seguimiento: cuestionarios y resultados informados por el paciente

[← Módulo 15](../15-medicamentos/README.md) · [Inicio](../../README.md) · [Módulo 17 →](../17-busquedas-y-versiones/README.md)

> **Nivel:** intermedio · **Duración:** 75 minutos · **Necesitas:** módulos 06 y 15

## Lo que vas a aprender

1. A **definir un formulario** con Questionnaire.
2. A registrar las **respuestas** de un paciente con QuestionnaireResponse.
3. A convertir una respuesta en un **dato analizable** (Observation con
   `derivedFrom`).

## La historia

Durante la hormonoterapia, Luis responde un cuestionario breve en cada
control: dolor, funcionalidad (ECOG), sofocos y dolor articular.

| Fecha | Dolor (0 a 10) | Actividad (ECOG) | Sofocos | Dolor articular |
|---|---|---|---|---|
| 28-oct-2025 | 2 | 0 · vida normal | no | no |
| 27-ene-2026 | **6** | 1 · trabajos ligeros | **sí** | **sí** |

En enero cuenta: *"Los bochornos no me dejan dormir y me duelen las rodillas
y las manos."* Son efectos conocidos del tamoxifeno. Con esa información, en
febrero de 2026 el oncólogo **suspende el tamoxifeno** (módulo 15) para
valorar una alternativa.

Este tipo de datos se llaman **resultados informados por el paciente**
(PRO, por sus siglas en inglés): lo que solo el paciente puede contar.

---

## Ficha del recurso: Questionnaire

**¿Qué es?** La **definición de un formulario**: sus preguntas, en qué orden,
de qué tipo es cada respuesta y cuáles son obligatorias. No tiene datos de
ningún paciente: es la plantilla.

**¿Para qué se usa?** Para escalas clínicas (dolor, depresión, riesgo de
caídas), encuestas de satisfacción, fichas de notificación epidemiológica,
formularios de ingreso. Al ser un recurso, el mismo formulario se puede
compartir entre sistemas.

**¿Cuándo usar otro recurso?** Si solo necesitas registrar un dato puntual
(la presión arterial), usa **Observation**. Questionnaire es para conjuntos
de preguntas que se responden juntas.

<!-- ficha Questionnaire -->
| Elemento | Card. | Tipo | Para qué sirve |
|---|---|---|---|
| `url` | 0..1 | uri | La dirección única que identifica el cuestionario en todas partes. |
| `identifier` | 0..* | Identifier | Otros identificadores. |
| `version` | 0..1 | string | La versión. |
| `name` | 0..1 | string | Nombre para máquinas, sin espacios. |
| `title` | 0..1 | string | Título para personas. |
| `status` ⚑ | **1..1** | code | `draft`, `active`, `retired` o `unknown`. |
| `subjectType` | 0..* | code | A quién se aplica: Patient, Practitioner... |
| `date` | 0..1 | dateTime | Fecha de la versión. |
| `publisher` | 0..1 | string | Quién lo publica. |
| `description` | 0..1 | markdown | Para qué sirve. |
| `item` | 0..* | BackboneElement | Las preguntas. |
| `item.linkId` | **1..1** | string | El identificador de la pregunta: enlaza pregunta y respuesta. |
| `item.code` | 0..* | Coding | Código de la pregunta (LOINC, por ejemplo). |
| `item.text` | 0..1 | string | El texto de la pregunta. |
| `item.type` | **1..1** | code | Tipo de respuesta: `boolean`, `integer`, `string`, `text`, `choice`, `date`, `group`... |
| `item.enableWhen` ⚑ | 0..* | BackboneElement | Mostrar la pregunta solo si otra tiene cierta respuesta. |
| `item.required` | 0..1 | boolean | Si es obligatoria. |
| `item.repeats` | 0..1 | boolean | Si admite varias respuestas. |
| `item.answerOption` | 0..* | BackboneElement | Las opciones, en una pregunta `choice`. |
| `item.item` | 0..* |  | Preguntas anidadas dentro de un grupo. |
<!-- /ficha -->

**`url` es clave.** Es el identificador **canónico** del cuestionario: no
importa en qué servidor esté guardado, las respuestas apuntan a esa `url`.

## Ficha del recurso: QuestionnaireResponse

**¿Qué es?** Las **respuestas** de una persona a un cuestionario, en un
momento.

<!-- ficha QuestionnaireResponse -->
| Elemento | Card. | Tipo | Para qué sirve |
|---|---|---|---|
| `identifier` | 0..1 | Identifier | Identificador. |
| `basedOn` | 0..* | Reference(CarePlan \| ServiceRequest) | La orden o el plan que pidió aplicarlo. |
| `questionnaire` | 0..1 | canonical | El cuestionario que se respondió (su `url`). |
| `status` ⚑ | **1..1** | code | `in-progress`, `completed`, `amended`, `entered-in-error` o `stopped`. |
| `subject` | 0..1 | Reference(Resource) | Sobre quién trata. |
| `encounter` | 0..1 | Reference(Encounter) | En qué atención. |
| `authored` | 0..1 | dateTime | Cuándo se respondió. |
| `author` | 0..1 | Reference(Device \| Practitioner \| PractitionerRole \| Patient \| …) | Quién escribió las respuestas. |
| `source` | 0..1 | Reference(Patient \| Practitioner \| PractitionerRole \| RelatedPerson) | Quién dio la información. |
| `item` | 0..* | BackboneElement | Las respuestas. |
| `item.linkId` | **1..1** | string | La pregunta a la que responde (el mismo `linkId` del cuestionario). |
| `item.text` | 0..1 | string | El texto de la pregunta, igual al del cuestionario. |
| `item.answer` | 0..* | BackboneElement | La respuesta. |
| `item.answer.value[x]` | 0..1 | boolean \| decimal \| integer \| date \| … | El valor, del tipo que pide la pregunta. |
| `item.item` | 0..* |  | Respuestas anidadas. |
<!-- /ficha -->

**Pregunta y respuesta se enlazan por `linkId`.** Y el tipo de la respuesta
debe coincidir con el `type` de la pregunta: a una pregunta `integer` se
responde con `valueInteger`; a una `boolean`, con `valueBoolean`.

---

## Paso a paso: el cuestionario

### Paso 1 · El mínimo: el estado

<!-- paso 16a 1 -->
```json
{
  "resourceType": "Questionnaire",
  "status": "active"
}
```
<!-- /paso -->

### Paso 2 · Cómo se identifica: url, versión, nombre y título

<!-- paso 16a 2 -->
```json
{
  "url": "https://f-slg.github.io/aprende-fhir/Questionnaire/seguimiento-oncologico",
  "version": "1.0.0",
  "name": "SeguimientoOncologico",
  "title": "Cuestionario de seguimiento oncológico",
  "date": "2025-09-01",
  "publisher": "Aprende FHIR desde cero (ejemplo didáctico)",
  "description": "Cuestionario breve para el control de pacientes en tratamiento oncológico.",
  "subjectType": [
    "Patient"
  ]
}
```
<!-- /paso -->

`name` es para las máquinas (sin espacios) y `title`, para las personas.
`publisher` aclara que es un ejemplo didáctico: no es una escala validada.

### Paso 3 · La primera pregunta: el dolor

<!-- paso 16a 3 -->
```json
{
  "item": [
    {
      "linkId": "dolor",
      "text": "En una escala de 0 (sin dolor) a 10 (el peor dolor imaginable), ¿cuánto dolor tuvo en la última semana?",
      "type": "integer",
      "required": true,
      "code": [
        {
          "system": "http://loinc.org",
          "code": "72514-3",
          "display": "Pain severity - 0-10 verbal numeric rating [Score] - Reported"
        }
      ]
    }
  ]
}
```
<!-- /paso -->

`type: integer` y `required: true`. El `code` LOINC `72514-3` (*Pain
severity - 0-10 verbal numeric rating*) dice qué mide la pregunta: así otro
sistema sabe que esta respuesta es una escala de dolor estándar, aunque el
texto esté en español.

### Paso 4 · Las demás preguntas

<!-- paso 16a 4 -->
```json
{
  "item": [
    {
      "linkId": "dolor",
      "text": "En una escala de 0 (sin dolor) a 10 (el peor dolor imaginable), ¿cuánto dolor tuvo en la última semana?",
      "type": "integer",
      "required": true,
      "code": [
        {
          "system": "http://loinc.org",
          "code": "72514-3",
          "display": "Pain severity - 0-10 verbal numeric rating [Score] - Reported"
        }
      ]
    },
    {
      "linkId": "ecog",
      "text": "¿Cuál de estas frases describe mejor su actividad habitual?",
      "type": "choice",
      "required": true,
      "answerOption": [
        {
          "valueString": "0 · Hago mi vida normal sin limitaciones"
        },
        {
          "valueString": "1 · Tengo síntomas, pero hago trabajos ligeros"
        },
        {
          "valueString": "2 · No puedo trabajar, pero me valgo por mí mismo"
        },
        {
          "valueString": "3 · Paso más de la mitad del día en cama o sentado"
        },
        {
          "valueString": "4 · Estoy en cama todo el día"
        }
      ]
    },
    {
      "linkId": "sofocos",
      "text": "¿Ha tenido sofocos (bochornos) en la última semana?",
      "type": "boolean"
    },
    {
      "linkId": "articular",
      "text": "¿Ha tenido dolor en las articulaciones en la última semana?",
      "type": "boolean"
    },
    {
      "linkId": "comentarios",
      "text": "¿Algo más que quiera contarnos?",
      "type": "text"
    }
  ],
  "text": {
    "status": "generated",
    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><p>Cuestionario de seguimiento oncológico: dolor (0 a 10), funcionalidad (ECOG),</p><p>sofocos, dolor articular y comentarios.</p></div>"
  }
}
```
<!-- /paso -->

- **ECOG** es `choice`: una opción de una lista (`answerOption`).
- **Sofocos** y **dolor articular** son `boolean`: sí o no.
- **Comentarios** es `text`: texto libre de varias líneas.

Solución: [`16a_questionnaire_seguimiento.json`](soluciones/16a_questionnaire_seguimiento.json).

## Paso a paso: la respuesta de octubre

### Paso 1 · El mínimo: qué cuestionario, todavía en curso

<!-- paso 16b 1 -->
```json
{
  "resourceType": "QuestionnaireResponse",
  "questionnaire": "https://f-slg.github.io/aprende-fhir/Questionnaire/seguimiento-oncologico",
  "status": "in-progress"
}
```
<!-- /paso -->

`questionnaire` es la `url` del cuestionario, no una referencia del
servidor. El estado empieza en `in-progress`: si lo marcaras `completed` sin
respuestas, el validador te diría que faltan las preguntas obligatorias:

```
No response answer found for required item 'dolor'
```

### Paso 2 · De quién, cuándo y quién respondió

<!-- paso 16b 2 -->
```json
{
  "subject": {
    "reference": "Patient/{{patientId}}",
    "display": "Luis Alberto Paredes Cevallos"
  },
  "authored": "2025-10-28T09:30:00-05:00",
  "author": {
    "reference": "Patient/{{patientId}}",
    "display": "Luis Alberto Paredes Cevallos"
  },
  "source": {
    "reference": "Patient/{{patientId}}",
    "display": "Luis Alberto Paredes Cevallos"
  }
}
```
<!-- /paso -->

`author` (quién escribió las respuestas) y `source` (quién dio la
información) son el propio Luis. Si una enfermera llenara el cuestionario
preguntándole, `author` sería la enfermera y `source` seguiría siendo Luis.

### Paso 3 · Las respuestas: ya se puede marcar como completo

<!-- paso 16b 3 -->
```json
{
  "item": [
    {
      "linkId": "dolor",
      "text": "En una escala de 0 (sin dolor) a 10 (el peor dolor imaginable), ¿cuánto dolor tuvo en la última semana?",
      "answer": [
        {
          "valueInteger": 2
        }
      ]
    },
    {
      "linkId": "ecog",
      "text": "¿Cuál de estas frases describe mejor su actividad habitual?",
      "answer": [
        {
          "valueString": "0 · Hago mi vida normal sin limitaciones"
        }
      ]
    },
    {
      "linkId": "sofocos",
      "text": "¿Ha tenido sofocos (bochornos) en la última semana?",
      "answer": [
        {
          "valueBoolean": false
        }
      ]
    },
    {
      "linkId": "articular",
      "text": "¿Ha tenido dolor en las articulaciones en la última semana?",
      "answer": [
        {
          "valueBoolean": false
        }
      ]
    },
    {
      "linkId": "comentarios",
      "text": "¿Algo más que quiera contarnos?",
      "answer": [
        {
          "valueString": "Me siento bien, ya volví al trabajo."
        }
      ]
    }
  ],
  "status": "completed",
  "text": {
    "status": "generated",
    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><p>Respuesta del 28 de octubre de 2025: dolor 2/10, ECOG 0, sin sofocos ni dolor articular.</p></div>"
  }
}
```
<!-- /paso -->

Cada `item` repite el `linkId` y el texto de su pregunta, y lleva la
respuesta del tipo correcto. El texto debe ser **idéntico** al del
cuestionario: si el validador tiene el cuestionario, lo comprueba. Solución:
[`16b_questionnaireresponse_octubre.json`](soluciones/16b_questionnaireresponse_octubre.json).

**La respuesta de enero.** Lo que cambia:

<!-- diferencia 16c -->
```json
{
  "authored": "2026-01-27T09:30:00-05:00",
  "item": [
    {
      "linkId": "dolor",
      "text": "En una escala de 0 (sin dolor) a 10 (el peor dolor imaginable), ¿cuánto dolor tuvo en la última semana?",
      "answer": [
        {
          "valueInteger": 6
        }
      ]
    },
    {
      "linkId": "ecog",
      "text": "¿Cuál de estas frases describe mejor su actividad habitual?",
      "answer": [
        {
          "valueString": "1 · Tengo síntomas, pero hago trabajos ligeros"
        }
      ]
    },
    {
      "linkId": "sofocos",
      "text": "¿Ha tenido sofocos (bochornos) en la última semana?",
      "answer": [
        {
          "valueBoolean": true
        }
      ]
    },
    {
      "linkId": "articular",
      "text": "¿Ha tenido dolor en las articulaciones en la última semana?",
      "answer": [
        {
          "valueBoolean": true
        }
      ]
    },
    {
      "linkId": "comentarios",
      "text": "¿Algo más que quiera contarnos?",
      "answer": [
        {
          "valueString": "Los bochornos no me dejan dormir y me duelen las rodillas y las manos."
        }
      ]
    }
  ]
}
```
<!-- /diferencia -->

## Paso a paso: del cuestionario a un dato analizable

Las respuestas de un cuestionario son difíciles de analizar: para graficar
el dolor de muchos pacientes habría que abrir cada formulario. Por eso el
dato clave se **extrae** como una Observation, que apunta a su origen con
`derivedFrom`.

### Paso 1 · El mínimo: estado y código

<!-- paso 16d 1 -->
```json
{
  "resourceType": "Observation",
  "status": "final",
  "code": {
    "coding": [
      {
        "system": "http://loinc.org",
        "code": "72514-3",
        "display": "Pain severity - 0-10 verbal numeric rating [Score] - Reported"
      }
    ],
    "text": "Intensidad del dolor (0 a 10)"
  }
}
```
<!-- /paso -->

El mismo LOINC `72514-3` que la pregunta.

### Paso 2 · El resultado: 6 de 10

<!-- paso 16d 2 -->
```json
{
  "category": [
    {
      "coding": [
        {
          "system": "http://terminology.hl7.org/CodeSystem/observation-category",
          "code": "survey",
          "display": "Survey"
        }
      ]
    }
  ],
  "subject": {
    "reference": "Patient/{{patientId}}",
    "display": "Luis Alberto Paredes Cevallos"
  },
  "effectiveDateTime": "2026-01-27T09:30:00-05:00",
  "performer": [
    {
      "reference": "Patient/{{patientId}}",
      "display": "Luis Alberto Paredes Cevallos"
    }
  ],
  "valueInteger": 6
}
```
<!-- /paso -->

`valueInteger`, categoría `survey` (lo informa el paciente) y `performer`, el
propio Luis.

### Paso 3 · De dónde sale: el cuestionario

<!-- paso 16d 3 -->
```json
{
  "derivedFrom": [
    {
      "reference": "QuestionnaireResponse/{{responseJanuaryId}}",
      "display": "Cuestionario del 27 de enero de 2026"
    }
  ],
  "text": {
    "status": "generated",
    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><p>Dolor 6/10 (escala numérica), informado por el paciente el 27 de enero de 2026.</p></div>"
  }
}
```
<!-- /paso -->

Solución: [`16d_observation_dolor.json`](soluciones/16d_observation_dolor.json).

---

## Ejercicios en el servidor

| Paso | Petición | Guarda |
|---|---|---|
| 16a | `POST /Questionnaire` con `If-None-Exist` (abajo) | `questionnaireId` |
| 16b | `POST /QuestionnaireResponse` (octubre) | `responseOctoberId` |
| 16c | `POST /QuestionnaireResponse` (enero) | `responseJanuaryId` |
| 16d | `POST /Observation` (dolor 6/10) | |

### 16a · Un solo cuestionario por `url`: creación condicional

Cada paciente crea su propio Patient, pero el cuestionario es **uno solo**
para todos: su `url` lo identifica en todas partes. Si cada persona que hace
el taller lo creara de nuevo, el servidor tendría muchas copias con la misma
`url`. Por eso se crea con el encabezado `If-None-Exist`:

```http
POST {{FHIRURL}}/Questionnaire
If-None-Exist: url=https://f-slg.github.io/aprende-fhir/Questionnaire/seguimiento-oncologico
```

Es la misma **creación condicional** del módulo 03 (`ifNoneExist` en una
transacción), ahora como encabezado HTTP. La primera vez el servidor lo crea
(`201`); las siguientes devuelve el que ya existe (`200`). Si hubiera **más
de uno** con esa `url`, respondería `412`: no sabría cuál elegir.

### 16e · Las respuestas del paciente a este cuestionario

```http
GET {{FHIRURL}}/QuestionnaireResponse?subject=Patient/{{patientId}}&questionnaire=https://f-slg.github.io/aprende-fhir/Questionnaire/seguimiento-oncologico&_sort=authored
```

Se busca por la `url` del cuestionario. Verás octubre (dolor 2) y enero
(dolor 6).

### 16f · Error a propósito: un número escrito en letras

Envía ([`16e1_respuesta_con_texto.json`](errores/16e1_respuesta_con_texto.json))
una respuesta con `"valueInteger": "seis"`. El servidor responde **`400`**:

```
HAPI-1821: [element="valueInteger"] Invalid attribute value "seis": java.lang.NumberFormatException: For input string: "seis"
```

## Para pensar

Si todos los pacientes en hormonoterapia respondieran este cuestionario en
cada control, ¿cómo encontrarías a los que tienen dolor de 6 o más?

Lo natural sería buscar `Observation?code=http://loinc.org|72514-3&value-quantity=ge6`
("mayor o igual a 6"), pero **no devuelve nada**: en FHIR R4 el parámetro
`value-quantity` solo busca en `valueQuantity`, y aquí el dolor está en
`valueInteger`. Por eso muchas implementaciones guardan los puntajes como
`valueQuantity` con la unidad UCUM `{score}`. ¿Qué ventajas y desventajas
tiene cada opción? Es un buen ejemplo de por qué las **guías de
implementación** (módulo 18) fijan estas decisiones para todos.

## Autoevaluación

<details><summary>1. ¿Qué diferencia hay entre Questionnaire y QuestionnaireResponse?</summary>

Questionnaire es la plantilla (las preguntas); QuestionnaireResponse, las
respuestas de una persona en un momento.
</details>

<details><summary>2. ¿Cómo se sabe a qué pregunta corresponde cada respuesta?</summary>

Por el `linkId`, que es el mismo en la pregunta y en la respuesta.
</details>

<details><summary>3. ¿Para qué sirve extraer el dolor como una Observation?</summary>

Para poder buscarlo, graficarlo y analizarlo como cualquier otro dato
clínico, sin abrir cada formulario. `derivedFrom` conserva el vínculo con la
respuesta original.
</details>

## Resumen

- **Questionnaire** define las preguntas; su `url` lo identifica en todas
  partes.
- **QuestionnaireResponse** guarda las respuestas, enlazadas por `linkId` y
  con el tipo que pide cada pregunta.
- Los datos clave se extraen como **Observation** con `derivedFrom`.

## Ejecutar este módulo

- **Postman:** carpeta *16 · Seguimiento*.
- **curl:** `curl/taller.sh 16`
- **R:**

  ```r
  dolor <- fhir_buscar("Observation?subject=Patient/{{patientId}}&code=http://loinc.org|72514-3")
  fhir_tabla(dolor, list(fecha = function(r) substr(r$effectiveDateTime, 1, 10),
                         dolor = function(r) r$valueInteger))
  ```
