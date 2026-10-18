# Módulo 05 · Diagnóstico y encuentro

[← Módulo 04](../04-profesionales-y-organizaciones/README.md) · [Inicio](../../README.md) · [Módulo 06 →](../06-observaciones/README.md)

> **Nivel:** básico · **Duración:** 60 minutos · **Necesitas:** módulos 02 y 04

## Lo que vas a aprender

1. Qué es **Condition** y cómo se codifica un diagnóstico con CIE-10 y SNOMED CT.
2. La diferencia entre el **estado clínico** y el **estado de verificación**.
3. Qué es **Encounter** y cómo representa una atención.
4. A traer recursos relacionados en una sola búsqueda con `_include`.

## La historia

El lunes 17 de marzo de 2025 Luis empieza con **dolor abdominal tipo cólico,
náuseas, vómito y diarrea**, después de comer en un puesto de comida. El
jueves 20 de marzo consulta en el hospital. De 07:15 a 08:15 lo atiende la
Dra. Salazar, que diagnostica una **intoxicación alimentaria bacteriana**,
de severidad moderada. Con hidratación y dieta, se resuelve el 24 de marzo.

Son dos cosas distintas que FHIR modela por separado:

- **la consulta** (cuándo, dónde, quién atendió): un **Encounter**;
- **el problema de salud** (qué tiene): una **Condition**.

---

## Ficha del recurso: Condition

**¿Qué es?** Un **problema de salud, diagnóstico o condición clínica**: una
enfermedad, un síndrome, un síntoma relevante, una lesión.

**¿Para qué se usa?** Para la **lista de problemas** del paciente (diabetes,
hipertensión) y para los **diagnósticos de una atención** (intoxicación
alimentaria en esta consulta). Es lo que alimenta la estadística de
morbilidad.

**¿Cuándo usar otro recurso?**

- Una alergia o intolerancia: **AllergyIntolerance** (módulo 07).
- Un antecedente de un familiar: **FamilyMemberHistory** (módulo 07).
- Una medición o un hallazgo puntual (presión arterial, resultado de
  laboratorio): **Observation** (módulo 06).
- Un procedimiento realizado: **Procedure** (módulo 13).

**Elementos principales** (<https://hl7.org/fhir/R4/condition.html>):

<!-- ficha Condition -->
| Elemento | Card. | Tipo | Para qué sirve |
|---|---|---|---|
| `identifier` | 0..* | Identifier | Identificador del registro. |
| `clinicalStatus` ⚑ | 0..1 | CodeableConcept | Cómo está hoy: `active`, `recurrence`, `relapse`, `inactive`, `remission`, `resolved`. |
| `verificationStatus` ⚑ | 0..1 | CodeableConcept | Qué tan seguro es: `confirmed`, `provisional`, `differential`, `refuted`, `entered-in-error`. |
| `category` | 0..* | CodeableConcept | `encounter-diagnosis` (diagnóstico de una atención) o `problem-list-item` (lista de problemas). |
| `severity` | 0..1 | CodeableConcept | Leve, moderada o severa. |
| `code` | 0..1 | CodeableConcept | **Qué** condición es: CIE-10, SNOMED CT. |
| `bodySite` | 0..* | CodeableConcept | Parte del cuerpo afectada. |
| `subject` | **1..1** | Reference(Patient \| Group) | De quién es la condición. |
| `encounter` | 0..1 | Reference(Encounter) | En qué atención se registró. |
| `onset[x]` | 0..1 | dateTime \| Age \| Period \| Range \| … | Cuándo empezó: fecha, edad, periodo o texto. |
| `abatement[x]` | 0..1 | dateTime \| Age \| Period \| Range \| … | Cuándo terminó. |
| `recordedDate` | 0..1 | dateTime | Cuándo se registró. |
| `recorder` | 0..1 | Reference(Practitioner \| PractitionerRole \| Patient \| RelatedPerson) | Quién lo registró en el sistema. |
| `asserter` | 0..1 | Reference(Practitioner \| PractitionerRole \| Patient \| RelatedPerson) | Quién afirma el diagnóstico. |
| `stage` | 0..* | BackboneElement | Estadio (en oncología, por ejemplo). |
| `evidence` | 0..* | BackboneElement | En qué se basa: síntomas, resultados, informes. |
| `note` | 0..* | Annotation | Notas. |
<!-- /ficha -->

`subject` es lo único obligatorio. Si `clinicalStatus` está presente, debe
ser coherente con `abatement[x]`: una condición resuelta puede tener fecha de
fin; una activa, no.

## Ficha del recurso: Encounter

**¿Qué es?** Una **interacción entre el paciente y los servicios de salud**:
una consulta, una atención de emergencia, una hospitalización, una visita
domiciliaria, una teleconsulta.

**¿Para qué se usa?** Es el **contexto** de casi todo lo clínico: los signos
vitales se toman *en* una consulta, el diagnóstico se hace *en* una consulta.
Por eso Observation, Condition y otros recursos lo referencian con
`encounter`. También es la base de la estadística de producción (número de
atenciones).

**¿Cuándo usar otro recurso?**

- Una cita **agendada** que aún no ocurre: **Appointment**.
- Un **episodio** que agrupa muchas atenciones (todo el tratamiento de un
  cáncer): **EpisodeOfCare**.

**Elementos principales** (<https://hl7.org/fhir/R4/encounter.html>):

<!-- ficha Encounter -->
| Elemento | Card. | Tipo | Para qué sirve |
|---|---|---|---|
| `identifier` | 0..* | Identifier | Número de la atención. |
| `status` ⚑ | **1..1** | code | `planned`, `arrived`, `in-progress`, `finished`, `cancelled`... |
| `class` | **1..1** | Coding | Modalidad: `AMB` ambulatoria, `EMER` emergencia, `IMP` hospitalización, `HH` domiciliaria, `VR` virtual. |
| `type` | 0..* | CodeableConcept | Tipo específico de atención. |
| `serviceType` | 0..1 | CodeableConcept | Servicio o especialidad: medicina general, pediatría... |
| `priority` | 0..1 | CodeableConcept | Urgencia: rutina, urgente, emergencia. |
| `subject` | 0..1 | Reference(Patient \| Group) | El paciente. |
| `episodeOfCare` | 0..* | Reference(EpisodeOfCare) | El episodio al que pertenece. |
| `basedOn` | 0..* | Reference(ServiceRequest) | La orden o derivación que la originó. |
| `participant` | 0..* | BackboneElement | Los profesionales que participaron y con qué rol. |
| `appointment` | 0..* | Reference(Appointment) | La cita que dio origen a la atención. |
| `period` | 0..1 | Period | Inicio y fin. |
| `reasonCode` | 0..* | CodeableConcept | Motivo de la atención, codificado. |
| `reasonReference` | 0..* | Reference(Condition \| Procedure \| Observation \| ImmunizationRecommendation) | Motivo como referencia a una Condition u Observation. |
| `diagnosis` | 0..* | BackboneElement | Diagnósticos de la atención, con su rol y orden. |
| `hospitalization` | 0..1 | BackboneElement | Datos de la internación: origen, destino, alta. |
| `location` | 0..* | BackboneElement | Dónde ocurrió: consultorio, cama, sala. |
| `serviceProvider` | 0..1 | Reference(Organization) | La organización responsable. |
<!-- /ficha -->

---

## Paso a paso: el diagnóstico

### Paso 1 · El mínimo: de quién es la condición

<!-- paso 05a 1 -->
```json
{
  "resourceType": "Condition",
  "subject": {
    "reference": "Patient/{{patientId}}",
    "display": "Luis Alberto Paredes Cevallos"
  }
}
```
<!-- /paso -->

Válido, pero sin saber qué condición es. `display` en una referencia es
opcional: ayuda a las personas a leer el JSON.

### Paso 2 · Qué condición es: el código CIE-10

<!-- paso 05a 2 -->
```json
{
  "code": {
    "coding": [
      {
        "system": "http://hl7.org/fhir/sid/icd-10",
        "code": "A05.9",
        "display": "Bacterial foodborne intoxication, unspecified"
      }
    ],
    "text": "Intoxicación alimentaria bacteriana, no especificada"
  }
}
```
<!-- /paso -->

`code` es un **CodeableConcept**: `coding` lleva el código para las máquinas
(`system` + `code` + `display`) y `text`, lo que lee la persona. El sistema de
la CIE-10 en FHIR es `http://hl7.org/fhir/sid/icd-10`. El `display` debe ser
el nombre **oficial** del código, en inglés: el validador lo comprueba.

### Paso 3 · Los dos estados: clínico y de verificación

<!-- paso 05a 3 -->
```json
{
  "clinicalStatus": {
    "coding": [
      {
        "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
        "code": "resolved",
        "display": "Resolved"
      }
    ]
  },
  "verificationStatus": {
    "coding": [
      {
        "system": "http://terminology.hl7.org/CodeSystem/condition-ver-status",
        "code": "confirmed",
        "display": "Confirmed"
      }
    ]
  },
  "category": [
    {
      "coding": [
        {
          "system": "http://terminology.hl7.org/CodeSystem/condition-category",
          "code": "encounter-diagnosis",
          "display": "Encounter Diagnosis"
        }
      ]
    }
  ]
}
```
<!-- /paso -->

Son dos preguntas distintas:

- `clinicalStatus`: **¿cómo está?** Ya pasó: `resolved`.
- `verificationStatus`: **¿qué tan seguros estamos?** Confirmado.

Una sospecha de dengue sería `active` + `provisional`; un dengue descartado,
`refuted`. Los dos estados son **modificadores** (⚑): un sistema que los
ignore podría tratar como activa una enfermedad resuelta o descartada.
`category` dice que es un diagnóstico de esta atención.

### Paso 4 · Severidad y fechas

<!-- paso 05a 4 -->
```json
{
  "severity": {
    "coding": [
      {
        "system": "http://snomed.info/sct",
        "code": "6736007",
        "display": "Moderate (severity modifier)"
      }
    ],
    "text": "Moderada"
  },
  "onsetDateTime": "2025-03-17",
  "abatementDateTime": "2025-03-24",
  "recordedDate": "2025-03-20"
}
```
<!-- /paso -->

La severidad usa **SNOMED CT** (`http://snomed.info/sct`). `onset[x]` es un
elemento **de elección**: el `[x]` se reemplaza por el tipo de dato que uses
(`onsetDateTime`, `onsetAge`, `onsetString`...). Aquí es una fecha, el 17 de
marzo, y `abatementDateTime` es el 24, cuando se resolvió.

### Paso 5 · Quién lo registró y la evidencia

<!-- paso 05a 5 -->
```json
{
  "identifier": [
    {
      "system": "https://f-slg.github.io/aprende-fhir/sid/condicion",
      "value": "COND-2025-0001"
    }
  ],
  "recorder": {
    "reference": "Practitioner/{{practitionerId}}",
    "display": "Dra. Andrea Lucía Salazar Moreno"
  },
  "asserter": {
    "reference": "Practitioner/{{practitionerId}}",
    "display": "Dra. Andrea Lucía Salazar Moreno"
  },
  "evidence": [
    {
      "code": [
        {
          "coding": [
            {
              "system": "http://snomed.info/sct",
              "code": "422587007",
              "display": "Nausea"
            }
          ],
          "text": "Náuseas"
        },
        {
          "coding": [
            {
              "system": "http://snomed.info/sct",
              "code": "422400008",
              "display": "Vomiting"
            }
          ],
          "text": "Vómito"
        },
        {
          "coding": [
            {
              "system": "http://snomed.info/sct",
              "code": "21522001",
              "display": "Abdominal pain"
            }
          ],
          "text": "Dolor abdominal"
        },
        {
          "coding": [
            {
              "system": "http://snomed.info/sct",
              "code": "62315008",
              "display": "Diarrhea"
            }
          ],
          "text": "Diarrea"
        }
      ]
    }
  ],
  "text": {
    "status": "generated",
    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><p>Intoxicación alimentaria bacteriana, no especificada (moderada).</p><p>Inicio: 17 de marzo de 2025. Resuelta.</p></div>"
  }
}
```
<!-- /paso -->

`recorder` es quien lo escribió en el sistema y `asserter`, quien afirma el
diagnóstico (aquí, la misma médica). `evidence` lista los síntomas que lo
sustentan, cada uno con su código SNOMED CT. Solución:
[`05a_condition_intoxicacion.json`](soluciones/05a_condition_intoxicacion.json).

## Paso a paso: el encuentro

### Paso 1 · El mínimo: estado y clase

<!-- paso 05b 1 -->
```json
{
  "resourceType": "Encounter",
  "status": "finished",
  "class": {
    "system": "http://terminology.hl7.org/CodeSystem/v3-ActCode",
    "code": "AMB",
    "display": "ambulatory"
  }
}
```
<!-- /paso -->

`status` y `class` son **obligatorios**. `class` es un `Coding` (no un
CodeableConcept) de la tabla `v3-ActCode`: `AMB` es ambulatoria.

### Paso 2 · Quién y cuándo

<!-- paso 05b 2 -->
```json
{
  "subject": {
    "reference": "Patient/{{patientId}}",
    "display": "Luis Alberto Paredes Cevallos"
  },
  "participant": [
    {
      "type": [
        {
          "coding": [
            {
              "system": "http://terminology.hl7.org/CodeSystem/v3-ParticipationType",
              "code": "ATND",
              "display": "attender"
            }
          ]
        }
      ],
      "individual": {
        "reference": "Practitioner/{{practitionerId}}",
        "display": "Dra. Andrea Lucía Salazar Moreno"
      }
    }
  ],
  "period": {
    "start": "2025-03-20T07:15:00-05:00",
    "end": "2025-03-20T08:15:00-05:00"
  }
}
```
<!-- /paso -->

`participant.type` con `ATND` (*attender*) indica que la Dra. Salazar es
quien atendió. `period` usa la hora de Ecuador continental (`-05:00`).

### Paso 3 · Qué tipo de atención fue

<!-- paso 05b 3 -->
```json
{
  "serviceType": {
    "coding": [
      {
        "system": "http://terminology.hl7.org/CodeSystem/service-type",
        "code": "124",
        "display": "General Practice"
      }
    ],
    "text": "Medicina general"
  },
  "priority": {
    "coding": [
      {
        "system": "http://terminology.hl7.org/CodeSystem/v3-ActPriority",
        "code": "R",
        "display": "routine"
      }
    ],
    "text": "Rutina"
  },
  "reasonCode": [
    {
      "coding": [
        {
          "system": "http://snomed.info/sct",
          "code": "21522001",
          "display": "Abdominal pain"
        }
      ],
      "text": "Dolor abdominal, náuseas y diarrea"
    }
  ]
}
```
<!-- /paso -->

### Paso 4 · Dónde y con qué diagnóstico

<!-- paso 05b 4 -->
```json
{
  "serviceProvider": {
    "reference": "Organization/{{hospitalId}}",
    "display": "Hospital General Docente Ejemplo"
  },
  "diagnosis": [
    {
      "condition": {
        "reference": "Condition/{{conditionIntoxId}}",
        "display": "Intoxicación alimentaria bacteriana"
      },
      "use": {
        "coding": [
          {
            "system": "http://terminology.hl7.org/CodeSystem/diagnosis-role",
            "code": "DD",
            "display": "Discharge diagnosis"
          }
        ]
      },
      "rank": 1
    }
  ]
}
```
<!-- /paso -->

`diagnosis` enlaza la Condition del paso anterior. `use` con `DD`
(*discharge diagnosis*) indica que es el diagnóstico de egreso de la
atención, y `rank: 1`, que es el principal.

### Paso 5 · Identificador y narrativa

<!-- paso 05b 5 -->
```json
{
  "identifier": [
    {
      "system": "https://f-slg.github.io/aprende-fhir/sid/encuentro",
      "value": "ENC-2025-0001"
    }
  ],
  "text": {
    "status": "generated",
    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><p>Consulta ambulatoria por dolor abdominal, náuseas y diarrea.</p><p>20 de marzo de 2025, 07:15 a 08:15 · Hospital General Docente Ejemplo · Dra. Andrea Lucía Salazar Moreno.</p></div>"
  }
}
```
<!-- /paso -->

Solución: [`05b_encounter_crear.json`](soluciones/05b_encounter_crear.json).

---

## Ejercicios en el servidor

### 05a y 05b · Crear el diagnóstico y el encuentro

```http
POST {{FHIRURL}}/Condition       → guarda conditionIntoxId
POST {{FHIRURL}}/Encounter       → guarda encounterId
```

La condición va primero porque el encuentro la referencia en `diagnosis`.

### 05c · Todo junto con `_include`

```http
GET {{FHIRURL}}/Encounter?subject=Patient/{{patientId}}&_include=Encounter:diagnosis
```

`_include` agrega al resultado los recursos a los que apunta cada encuentro
por `diagnosis`. En el Bundle verás el Encounter con `search.mode: match` (el
que buscaste) y la Condition con `search.mode: include` (el que se agregó).
Así obtienes todo en una petición, en lugar de dos.

### 05d · Error a propósito: el estado en español

Envía ([`05e1_estado_en_espanol.json`](errores/05e1_estado_en_espanol.json))
un Encounter con `"status": "terminado"`. El servidor responde **`400`**:

```
HAPI-1821: [element="status"] Invalid attribute value "terminado": Unknown EncounterStatus code 'terminado'
```

`status` es un **code** con una lista cerrada (*binding required*): solo se
aceptan los valores de la especificación, en inglés. El correcto es
`finished`.

## Autoevaluación

<details><summary>1. Sospechas un dengue y pides la prueba. ¿Qué estados tiene la Condition?</summary>

`clinicalStatus: active` y `verificationStatus: provisional`. Si la prueba
sale negativa, se actualiza a `refuted`.
</details>

<details><summary>2. ¿La Condition debe apuntar al Encounter o el Encounter a la Condition?</summary>

Pueden hacerlo los dos: `Condition.encounter` dice en qué atención se
registró el diagnóstico, y `Encounter.diagnosis` lista los diagnósticos de la
atención, con su rol y orden. En el taller usamos `Encounter.diagnosis`.
</details>

<details><summary>3. ¿Qué significa el <code>[x]</code> en <code>onset[x]</code>?</summary>

Que el elemento admite varios tipos de dato y el nombre cambia según el
tipo: `onsetDateTime`, `onsetAge`, `onsetPeriod`, `onsetString`... Solo se
usa uno.
</details>

## Resumen

- **Condition** es el problema de salud; **Encounter**, la atención.
- Los diagnósticos se codifican con **CIE-10** y **SNOMED CT** en un
  `CodeableConcept`.
- `clinicalStatus` (¿cómo está?) y `verificationStatus` (¿qué tan seguro?)
  son modificadores.
- `_include` trae en una búsqueda los recursos referenciados.

## Ejecutar este módulo

- **Postman:** carpeta *05 · Diagnóstico y encuentro*.
- **curl:** `curl/taller.sh 05`
- **R:**

  ```r
  dir <- "modulos/05-diagnostico-y-encuentro/soluciones/"
  fhir_crear("Condition", paste0(dir, "05a_condition_intoxicacion.json"), guarda = "conditionIntoxId")
  fhir_crear("Encounter", paste0(dir, "05b_encounter_crear.json"), guarda = "encounterId")
  r <- fhir_buscar("Encounter?subject=Patient/{{patientId}}&_include=Encounter:diagnosis")
  vapply(r$entry, function(e) paste(e$resource$resourceType, e$search$mode), "")
  ```
