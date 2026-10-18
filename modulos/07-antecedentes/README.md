# Módulo 07 · Antecedentes: alergias, medicación habitual y familia

[← Módulo 06](../06-observaciones/README.md) · [Inicio](../../README.md) · [Módulo 08 →](../08-vacunacion/README.md)

> **Nivel:** intermedio · **Duración:** 75 minutos · **Necesitas:** módulos 05 y 06

## Lo que vas a aprender

1. A registrar una **alergia** con AllergyIntolerance, incluida su reacción.
2. A registrar la **medicación que el paciente ya toma** con MedicationStatement.
3. A registrar **antecedentes familiares** con FamilyMemberHistory.
4. Por qué cada uno de estos datos es un recurso aparte y no un texto en la
   historia clínica.

## La historia

En la misma consulta del 20 de marzo, la Dra. Salazar completa la anamnesis.
Luis le cuenta tres cosas:

- **Es alérgico a la penicilina.** En la adolescencia, a las pocas horas de
  una inyección, le salieron ronchas en todo el cuerpo.
- **Toma losartán 50 mg** todos los días desde junio de 2021, por
  hipertensión arterial.
- **Su madre, Rosa Cevallos, tuvo cáncer de mama** a los 52 años y falleció
  a los 60 por esa causa. **Su padre** tiene diabetes tipo 2 desde los 55.

Todavía no lo sabe nadie, pero el antecedente de su madre será importante
en el módulo 11.

---

## Ficha del recurso: AllergyIntolerance

**¿Qué es?** El registro de que una persona tiene **riesgo de una reacción
adversa** al exponerse a una sustancia: un medicamento, un alimento, una
sustancia del ambiente (látex, polen) o una picadura.

**¿Para qué se usa?** Para la **seguridad del paciente**: los sistemas de
prescripción revisan las alergias antes de recetar. Si la alergia a la
penicilina está bien codificada, el sistema puede alertar cuando alguien
prescriba amoxicilina. Si solo está escrita en una nota, no.

**¿Cuándo usar otro recurso?**

- Una reacción que ocurrió en un momento concreto y que se investiga como
  evento adverso: **AdverseEvent**.
- Un efecto secundario esperado de un tratamiento (las náuseas de la
  quimioterapia, módulo 15): una nota o una **Observation**, no una alergia.

**Elementos principales** (<https://hl7.org/fhir/R4/allergyintolerance.html>):

<!-- ficha AllergyIntolerance -->
| Elemento | Card. | Tipo | Para qué sirve |
|---|---|---|---|
| `identifier` | 0..* | Identifier | Identificador del registro. |
| `clinicalStatus` ⚑ | 0..1 | CodeableConcept | `active`, `inactive` o `resolved`. |
| `verificationStatus` ⚑ | 0..1 | CodeableConcept | `unconfirmed`, `confirmed`, `refuted` o `entered-in-error`. |
| `type` | 0..1 | code | `allergy` (mecanismo inmunológico) o `intolerance` (no inmunológico). |
| `category` | 0..* | code | `food`, `medication`, `environment` o `biologic`. |
| `criticality` | 0..1 | code | Riesgo de una reacción grave: `low`, `high` o `unable-to-assess`. |
| `code` | 0..1 | CodeableConcept | **A qué** es alérgico. |
| `patient` | **1..1** | Reference(Patient) | El paciente. |
| `encounter` | 0..1 | Reference(Encounter) | En qué atención se registró. |
| `onset[x]` | 0..1 | dateTime \| Age \| Period \| Range \| … | Cuándo empezó. |
| `recordedDate` | 0..1 | dateTime | Cuándo se registró. |
| `recorder` | 0..1 | Reference(Practitioner \| PractitionerRole \| Patient \| RelatedPerson) | Quién lo registró. |
| `asserter` | 0..1 | Reference(Patient \| RelatedPerson \| Practitioner \| PractitionerRole) | Quién lo informa: el paciente, un familiar, un profesional. |
| `lastOccurrence` | 0..1 | dateTime | La última vez que tuvo una reacción. |
| `note` | 0..* | Annotation | Notas. |
| `reaction` | 0..* | BackboneElement | Cada reacción que tuvo. |
| `reaction.substance` | 0..1 | CodeableConcept | La sustancia concreta que la causó. |
| `reaction.manifestation` | **1..*** | CodeableConcept | Qué le pasó: urticaria, anafilaxia, edema. |
| `reaction.severity` | 0..1 | code | Gravedad de **esa** reacción: `mild`, `moderate` o `severe`. |
| `reaction.description` | 0..1 | string | La reacción contada en palabras. |
<!-- /ficha -->

**`criticality` no es lo mismo que `reaction.severity`.** La criticidad es el
**riesgo futuro** de una reacción grave (alto, en una alergia a la
penicilina con urticaria generalizada). La severidad describe **una reacción
que ya ocurrió** (fue moderada).

## Ficha del recurso: MedicationStatement

**¿Qué es?** La afirmación de que el paciente **está tomando, tomó o tomará**
un medicamento, según lo que informa él mismo, un familiar, otro profesional
o un registro.

**¿Para qué se usa?** Para la **conciliación de medicamentos**: saber qué toma
el paciente antes de indicar algo nuevo, para evitar interacciones y
duplicaciones.

**¿Cuándo usar otro recurso?** Es fácil confundirlos:

| Recurso | Responde a... | Ejemplo |
|---|---|---|
| **MedicationRequest** | ¿Qué se **ordenó**? | La receta de tamoxifeno (módulo 15) |
| **MedicationDispense** | ¿Qué se **entregó** en la farmacia? | 30 comprimidos entregados |
| **MedicationAdministration** | ¿Qué se **administró**, cuándo y quién? | La dosis de doxorrubicina de hoy (módulo 15) |
| **MedicationStatement** | ¿Qué **toma** el paciente, según alguien? | "Tomo losartán todos los días" |

**Elementos principales** (<https://hl7.org/fhir/R4/medicationstatement.html>):

<!-- ficha MedicationStatement -->
| Elemento | Card. | Tipo | Para qué sirve |
|---|---|---|---|
| `status` ⚑ | **1..1** | code | `active`, `completed`, `stopped`, `not-taken`, `intended`... |
| `medication[x]` | **1..1** | CodeableConcept \| Reference(Medication) | Qué medicamento: un código o una referencia a un Medication. |
| `subject` | **1..1** | Reference(Patient \| Group) | Quién lo toma. |
| `context` | 0..1 | Reference(Encounter \| EpisodeOfCare) | En qué atención se registró. |
| `effective[x]` | 0..1 | dateTime \| Period | Desde cuándo y hasta cuándo lo toma. |
| `dateAsserted` | 0..1 | dateTime | Cuándo se obtuvo la información. |
| `informationSource` | 0..1 | Reference(Patient \| Practitioner \| PractitionerRole \| RelatedPerson \| …) | Quién lo informa. |
| `reasonCode` | 0..* | CodeableConcept | Por qué lo toma. |
| `dosage` | 0..* | Dosage | Cómo lo toma: dosis, vía, frecuencia. |
| `note` | 0..* | Annotation | Notas. |
<!-- /ficha -->

## Ficha del recurso: FamilyMemberHistory

**¿Qué es?** Los **antecedentes de salud de un familiar** del paciente: quién
es el familiar y qué enfermedades tuvo o tiene.

**¿Para qué se usa?** Para estimar **riesgos**: antecedentes de cáncer, de
enfermedad cardiovascular temprana o de diabetes cambian el tamizaje y el
seguimiento que se indica al paciente.

**¿Cuándo usar otro recurso?** Las enfermedades del **propio** paciente van en
**Condition**. Un familiar que además es paciente del mismo sistema puede
tener su propio Patient, pero FamilyMemberHistory sigue siendo la forma de
registrar el antecedente en la historia de Luis.

**Elementos principales** (<https://hl7.org/fhir/R4/familymemberhistory.html>):

<!-- ficha FamilyMemberHistory -->
| Elemento | Card. | Tipo | Para qué sirve |
|---|---|---|---|
| `status` ⚑ | **1..1** | code | `partial`, `completed`, `entered-in-error` o `health-unknown`. |
| `patient` | **1..1** | Reference(Patient) | El paciente cuyo antecedente es. |
| `date` | 0..1 | dateTime | Cuándo se registró. |
| `name` | 0..1 | string | Nombre del familiar. |
| `relationship` | **1..1** | CodeableConcept | Parentesco: madre, padre, hermano... |
| `sex` | 0..1 | CodeableConcept | Sexo del familiar. |
| `born[x]` | 0..1 | Period \| date \| string | Cuándo nació. |
| `age[x]` | 0..1 | Age \| Range \| string | Edad actual. |
| `deceased[x]` | 0..1 | boolean \| Age \| Range \| date \| … | Si falleció: sí o no, edad o fecha. |
| `note` | 0..* | Annotation | Notas. |
| `condition` | 0..* | BackboneElement | Cada enfermedad del familiar. |
| `condition.code` | **1..1** | CodeableConcept | Qué enfermedad. |
| `condition.outcome` | 0..1 | CodeableConcept | Cómo terminó. |
| `condition.contributedToDeath` | 0..1 | boolean | Si contribuyó a su muerte. |
| `condition.onset[x]` | 0..1 | Age \| Range \| Period \| string | A qué edad o cuándo empezó. |
<!-- /ficha -->

**Un recurso por familiar.** La madre y el padre son dos FamilyMemberHistory
distintos; cada uno puede tener varias enfermedades en `condition`.

---

## Paso a paso: la alergia a la penicilina

### Paso 1 · El mínimo válido: paciente, sustancia y estados

<!-- paso 07a 1 -->
```json
{
  "resourceType": "AllergyIntolerance",
  "patient": {
    "reference": "Patient/{{patientId}}",
    "display": "Luis Alberto Paredes Cevallos"
  },
  "code": {
    "coding": [
      {
        "system": "http://snomed.info/sct",
        "code": "764146007",
        "display": "Penicillin"
      }
    ],
    "text": "Penicilina"
  },
  "clinicalStatus": {
    "coding": [
      {
        "system": "http://terminology.hl7.org/CodeSystem/allergyintolerance-clinical",
        "code": "active",
        "display": "Active"
      }
    ]
  },
  "verificationStatus": {
    "coding": [
      {
        "system": "http://terminology.hl7.org/CodeSystem/allergyintolerance-verification",
        "code": "confirmed",
        "display": "Confirmed"
      }
    ]
  }
}
```
<!-- /paso -->

Aunque solo `patient` es obligatorio, AllergyIntolerance tiene una regla
(`ait-1`): **`clinicalStatus` debe estar presente** salvo que el registro sea
un error. Sin él, el validador responde:

```
Constraint failed: ait-1: 'AllergyIntolerance.clinicalStatus SHALL be present if verificationStatus is not entered-in-error.'
```

La sustancia se codifica con SNOMED CT: `764146007` *Penicillin*.

### Paso 2 · Tipo, categoría y criticidad

<!-- paso 07a 2 -->
```json
{
  "type": "allergy",
  "category": [
    "medication"
  ],
  "criticality": "high"
}
```
<!-- /paso -->

Es una alergia (`allergy`), a un medicamento (`medication`), con riesgo
**alto** (`high`) de reacción grave en una nueva exposición. `category` es
una lista porque una sustancia puede ser de varias categorías.

### Paso 3 · La reacción

<!-- paso 07a 3 -->
```json
{
  "reaction": [
    {
      "substance": {
        "coding": [
          {
            "system": "http://snomed.info/sct",
            "code": "764146007",
            "display": "Penicillin"
          }
        ],
        "text": "Penicilina"
      },
      "manifestation": [
        {
          "coding": [
            {
              "system": "http://snomed.info/sct",
              "code": "126485001",
              "display": "Urticaria"
            }
          ],
          "text": "Urticaria generalizada"
        }
      ],
      "severity": "moderate",
      "description": "Ronchas en todo el cuerpo a las pocas horas de una inyección de penicilina."
    }
  ]
}
```
<!-- /paso -->

`manifestation` es lo que le pasó: urticaria (SNOMED `126485001`). `severity`
es la gravedad de **esa** reacción, moderada. `description` lo cuenta con las
palabras del paciente.

### Paso 4 · Cuándo empezó, quién lo registró y quién lo informó

<!-- paso 07a 4 -->
```json
{
  "identifier": [
    {
      "system": "https://f-slg.github.io/aprende-fhir/sid/alergia",
      "value": "AL-2025-0001"
    }
  ],
  "encounter": {
    "reference": "Encounter/{{encounterId}}",
    "display": "Consulta por dolor abdominal"
  },
  "onsetString": "En la adolescencia",
  "recordedDate": "2025-03-20",
  "recorder": {
    "reference": "Practitioner/{{practitionerId}}",
    "display": "Dra. Andrea Lucía Salazar Moreno"
  },
  "asserter": {
    "reference": "Patient/{{patientId}}",
    "display": "Luis Alberto Paredes Cevallos"
  },
  "text": {
    "status": "generated",
    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><p>Alergia a la penicilina (criticidad alta): urticaria generalizada en la adolescencia.</p></div>"
  }
}
```
<!-- /paso -->

`onsetString` porque Luis no recuerda la fecha exacta: "en la adolescencia".
`asserter` es el propio Luis (quien lo informa) y `recorder`, la médica (quien
lo registra). Solución:
[`07a_allergyintolerance_penicilina.json`](soluciones/07a_allergyintolerance_penicilina.json).

## Paso a paso: el losartán

### Paso 1 · El mínimo: estado, medicamento y paciente

<!-- paso 07b 1 -->
```json
{
  "resourceType": "MedicationStatement",
  "status": "active",
  "medicationCodeableConcept": {
    "coding": [
      {
        "system": "http://snomed.info/sct",
        "code": "373567002",
        "display": "Losartan"
      }
    ],
    "text": "Losartán"
  },
  "subject": {
    "reference": "Patient/{{patientId}}",
    "display": "Luis Alberto Paredes Cevallos"
  }
}
```
<!-- /paso -->

`medicationCodeableConcept` es la forma `[x]` de `medication[x]` con un
código. Para describir un producto concreto (marca, concentración, forma
farmacéutica) se usaría `medicationReference` apuntando a un recurso
**Medication**.

### Paso 2 · Desde cuándo y quién lo informa

<!-- paso 07b 2 -->
```json
{
  "effectivePeriod": {
    "start": "2021-06"
  },
  "dateAsserted": "2025-03-20",
  "informationSource": {
    "reference": "Patient/{{patientId}}",
    "display": "Luis Alberto Paredes Cevallos"
  },
  "context": {
    "reference": "Encounter/{{encounterId}}",
    "display": "Consulta por dolor abdominal"
  }
}
```
<!-- /paso -->

`effectivePeriod` sin fecha de fin: lo sigue tomando. `start` acepta solo año
y mes (`2021-06`) cuando no se sabe el día.

### Paso 3 · Por qué lo toma y cómo

<!-- paso 07b 3 -->
```json
{
  "reasonCode": [
    {
      "coding": [
        {
          "system": "http://snomed.info/sct",
          "code": "38341003",
          "display": "Hypertensive disorder, systemic arterial"
        }
      ],
      "text": "Hipertensión arterial"
    }
  ],
  "dosage": [
    {
      "text": "50 mg por vía oral una vez al día",
      "timing": {
        "repeat": {
          "frequency": 1,
          "period": 1,
          "periodUnit": "d"
        }
      },
      "route": {
        "coding": [
          {
            "system": "http://snomed.info/sct",
            "code": "26643006",
            "display": "Oral route"
          }
        ],
        "text": "Vía oral"
      },
      "doseAndRate": [
        {
          "doseQuantity": {
            "value": 50,
            "unit": "mg",
            "system": "http://unitsofmeasure.org",
            "code": "mg"
          }
        }
      ]
    }
  ],
  "text": {
    "status": "generated",
    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><p>Toma losartán 50 mg por vía oral una vez al día para la hipertensión, desde 2021.</p></div>"
  }
}
```
<!-- /paso -->

`dosage` tiene la misma estructura que la indicación de una receta: `text`
para personas y `timing`, `route` y `doseAndRate` para las máquinas. Una vez
al día es `frequency: 1` cada `period: 1` `periodUnit: d`. Solución:
[`07b_medicationstatement_losartan.json`](soluciones/07b_medicationstatement_losartan.json).

## Paso a paso: los antecedentes de la madre

### Paso 1 · El mínimo: estado, paciente y parentesco

<!-- paso 07c 1 -->
```json
{
  "resourceType": "FamilyMemberHistory",
  "status": "completed",
  "patient": {
    "reference": "Patient/{{patientId}}",
    "display": "Luis Alberto Paredes Cevallos"
  },
  "relationship": {
    "coding": [
      {
        "system": "http://terminology.hl7.org/CodeSystem/v3-RoleCode",
        "code": "MTH",
        "display": "mother"
      }
    ],
    "text": "Madre"
  }
}
```
<!-- /paso -->

`relationship` usa la tabla `v3-RoleCode`: `MTH` es madre, `FTH` padre, `SIS`
hermana, `BRO` hermano...

### Paso 2 · Quién es el familiar

<!-- paso 07c 2 -->
```json
{
  "name": "Rosa Cevallos (madre)",
  "sex": {
    "coding": [
      {
        "system": "http://hl7.org/fhir/administrative-gender",
        "code": "female",
        "display": "Female"
      }
    ],
    "text": "Femenino"
  },
  "date": "2025-03-20",
  "deceasedAge": {
    "value": 60,
    "unit": "años",
    "system": "http://unitsofmeasure.org",
    "code": "a"
  }
}
```
<!-- /paso -->

`deceasedAge` es la forma `[x]` de `deceased[x]` con una edad: falleció a los
60 años. La edad es un `Quantity` con la unidad UCUM `a` (años).

### Paso 3 · Su enfermedad

<!-- paso 07c 3 -->
```json
{
  "condition": [
    {
      "code": {
        "coding": [
          {
            "system": "http://snomed.info/sct",
            "code": "254837009",
            "display": "Malignant neoplasm of breast"
          }
        ],
        "text": "Cáncer de mama"
      },
      "contributedToDeath": true,
      "onsetAge": {
        "value": 52,
        "unit": "años",
        "system": "http://unitsofmeasure.org",
        "code": "a"
      }
    }
  ],
  "text": {
    "status": "generated",
    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><p>Madre: cáncer de mama diagnosticado a los 52 años; falleció a los 60.</p></div>"
  }
}
```
<!-- /paso -->

`condition.onsetAge`: el cáncer de mama empezó a los 52 años, y
`contributedToDeath: true`: fue la causa de su muerte. Solución:
[`07c_familymemberhistory_madre.json`](soluciones/07c_familymemberhistory_madre.json).

### El padre: otro recurso, otro parentesco

Lo que cambia en el antecedente del padre:

<!-- diferencia 07d -->
```json
{
  "relationship": {
    "coding": [
      {
        "system": "http://terminology.hl7.org/CodeSystem/v3-RoleCode",
        "code": "FTH",
        "display": "father"
      }
    ],
    "text": "Padre"
  },
  "sex": {
    "coding": [
      {
        "system": "http://hl7.org/fhir/administrative-gender",
        "code": "male",
        "display": "Male"
      }
    ],
    "text": "Masculino"
  },
  "deceasedBoolean": false,
  "condition": [
    {
      "code": {
        "coding": [
          {
            "system": "http://snomed.info/sct",
            "code": "44054006",
            "display": "Diabetes mellitus type 2"
          }
        ],
        "text": "Diabetes mellitus tipo 2"
      },
      "onsetAge": {
        "value": 55,
        "unit": "años",
        "system": "http://unitsofmeasure.org",
        "code": "a"
      }
    }
  ]
}
```
<!-- /diferencia -->

Está vivo: `deceasedBoolean: false`. Solución:
[`07d_familymemberhistory_padre.json`](soluciones/07d_familymemberhistory_padre.json).

---

## Ejercicios en el servidor

### 07a a 07d · Registrar los antecedentes

```http
POST {{FHIRURL}}/AllergyIntolerance
POST {{FHIRURL}}/MedicationStatement
POST {{FHIRURL}}/FamilyMemberHistory     (madre)
POST {{FHIRURL}}/FamilyMemberHistory     (padre)
```

### 07e · Las alergias activas

```http
GET {{FHIRURL}}/AllergyIntolerance?patient=Patient/{{patientId}}&clinical-status=active
```

Es la búsqueda que hace un sistema de prescripción antes de recetar. Fíjate
que el parámetro de búsqueda se escribe `clinical-status`, con guion, aunque
el elemento se llama `clinicalStatus`: los parámetros de búsqueda tienen sus
propios nombres, y están en la especificación de cada recurso.

### 07f · Los antecedentes familiares

```http
GET {{FHIRURL}}/FamilyMemberHistory?patient=Patient/{{patientId}}
```

### 07g · Error a propósito: la criticidad en español

Envía ([`07e1_criticidad_en_espanol.json`](errores/07e1_criticidad_en_espanol.json))
una alergia con `"criticality": "alta"`. El servidor responde **`400`**:

```
HAPI-1821: [element="criticality"] Invalid attribute value "alta": Unknown AllergyIntoleranceCriticality code 'alta'
```

El validador, además, detecta que falta `clinicalStatus` (regla `ait-1`).

## Para pensar

El cáncer de mama en hombres es poco frecuente. Cuando aparece, y más con una
madre que lo tuvo joven, se recomienda evaluar el **riesgo hereditario**
(por ejemplo, variantes en el gen *BRCA2*). ¿Cómo ayudaría que el antecedente
de la madre esté codificado (SNOMED `254837009`, edad de inicio 52) y no
escrito en una nota? Piensa en un sistema que identifique automáticamente a
quién derivar a consejería genética.

## Autoevaluación

<details><summary>1. ¿Qué diferencia hay entre <code>criticality</code> y <code>reaction.severity</code>?</summary>

La criticidad es el riesgo de una reacción grave en el futuro. La severidad
describe una reacción concreta que ya ocurrió.
</details>

<details><summary>2. Luis dice "tomo losartán". ¿MedicationStatement o MedicationRequest?</summary>

**MedicationStatement**: es lo que el paciente informa que toma. Una
MedicationRequest es una orden de un prescriptor.
</details>

<details><summary>3. Luis tiene dos hermanos con hipertensión. ¿Cuántos FamilyMemberHistory registras?</summary>

Dos: uno por cada familiar. Si un hermano tuviera también diabetes, iría
como otra `condition` en su mismo recurso.
</details>

## Resumen

- **AllergyIntolerance** registra el riesgo de reacción a una sustancia, con
  su criticidad y sus reacciones.
- **MedicationStatement** registra lo que el paciente toma, según quien lo
  informa; no es una receta.
- **FamilyMemberHistory** registra un familiar y sus enfermedades: un
  recurso por familiar.
- Codificar los antecedentes permite usarlos para alertas y para estimar
  riesgos.

## Ejecutar este módulo

- **Postman:** carpeta *07 · Antecedentes*.
- **curl:** `curl/taller.sh 07`
- **R:**

  ```r
  alergias <- fhir_buscar("AllergyIntolerance?patient=Patient/{{patientId}}&clinical-status=active")
  fhir_tabla(alergias, list(
    sustancia   = function(r) r$code$text,
    criticidad  = function(r) r$criticality,
    reaccion    = function(r) r$reaction[[1]]$manifestation[[1]]$text
  ))
  ```
