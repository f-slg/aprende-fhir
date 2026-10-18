# Módulo 15 · Medicamentos

[← Módulo 13](../13-procedimientos/README.md) · [Inicio](../../README.md)

> **Nivel:** intermedio · **Duración:** 90 minutos · **Necesitas:** módulos 06 y 11
>
> Los módulos 14 (citas), 16 (seguimiento) y 17 a 19 (nivel avanzado) están
> en preparación.

## Lo que vas a aprender

1. La diferencia entre **prescribir** (MedicationRequest) y **administrar**
   (MedicationAdministration).
2. A expresar una dosis con texto y con datos estructurados (`Dosage`).
3. A justificar una dosis con una observación (`supportingInformation`).
4. El **ciclo de vida** de una receta: activa → suspendida.
5. A recuperar todo el expediente con la operación **`$everything`**.

## La historia

**Quimioterapia.** El 1 de julio de 2025 se pesa y se mide a Luis: 72 kg y
1,57 m. Su **superficie corporal** es 1,77 m². La dosis de **doxorrubicina**
es 60 mg/m² × 1,77 m² = **106,2 mg** por vía intravenosa, cada 21 días, 4
ciclos. El primer ciclo se administra el 2 de julio, de 09:00 a 09:30. Dos
horas después, Luis tiene náuseas leves.

**Hormonoterapia.** Como el tumor es receptor de estrógeno positivo, el 15 de
octubre se prescribe **tamoxifeno** 20 mg diarios por vía oral, durante 5
años. Luis toma la primera dosis en casa al día siguiente. En febrero de
2026 se suspende por intolerancia: sofocos intensos y dolor articular.

> Antes de prescribir, el sistema puede revisar las alergias del módulo 07:
> Luis es alérgico a la penicilina, no a estos medicamentos.

---

## Ficha del recurso: MedicationRequest

**¿Qué es?** Una **orden o propuesta** de que el paciente reciba un
medicamento: la receta de un tratamiento ambulatorio o la indicación de un
paciente hospitalizado.

**¿Para qué se usa?** Para la **prescripción**: qué medicamento, cuánto,
cómo, por cuánto tiempo, quién lo ordena y por qué.

**¿Cuándo usar otro recurso?** Repasa la tabla del módulo 07:
MedicationStatement (lo que el paciente dice que toma), MedicationDispense
(lo que se entregó) y MedicationAdministration (lo que se administró).

**Elementos principales** (<https://hl7.org/fhir/R4/medicationrequest.html>):

<!-- ficha MedicationRequest -->
| Elemento | Card. | Tipo | Para qué sirve |
|---|---|---|---|
| `identifier` | 0..* | Identifier | Número de la receta. |
| `status` ⚑ | **1..1** | code | `active`, `on-hold`, `cancelled`, `completed`, `stopped`, `draft`... |
| `statusReason` | 0..1 | CodeableConcept | Por qué se suspendió o canceló. |
| `intent` ⚑ | **1..1** | code | `proposal`, `plan`, `order`, `original-order`... |
| `category` | 0..* | CodeableConcept | `inpatient`, `outpatient`, `community`, `discharge`. |
| `priority` | 0..1 | code | `routine`, `urgent`, `asap`, `stat`. |
| `medication[x]` | **1..1** | CodeableConcept \| Reference(Medication) | Qué medicamento. |
| `subject` | **1..1** | Reference(Patient \| Group) | Para quién. |
| `encounter` | 0..1 | Reference(Encounter) | En qué atención. |
| `supportingInformation` | 0..* | Reference(Resource) | Datos que justifican la orden: peso, superficie corporal. |
| `authoredOn` | 0..1 | dateTime | Cuándo se prescribió. |
| `requester` | 0..1 | Reference(Practitioner \| PractitionerRole \| Organization \| Patient \| …) | Quién prescribe. |
| `reasonCode` | 0..* | CodeableConcept | Por qué, codificado. |
| `reasonReference` | 0..* | Reference(Condition \| Observation) | Por qué, como referencia a una Condition. |
| `basedOn` | 0..* | Reference(CarePlan \| MedicationRequest \| ServiceRequest \| ImmunizationRecommendation) | El plan del que forma parte. |
| `note` | 0..* | Annotation | Notas. |
| `dosageInstruction` | 0..* | Dosage | Cómo tomarlo. |
| `dispenseRequest` | 0..1 | BackboneElement | Cuánto entregar en farmacia y cuántas veces. |
| `substitution` | 0..1 | BackboneElement | Si se permite el genérico. |
| `priorPrescription` | 0..1 | Reference(MedicationRequest) | La receta a la que reemplaza. |
<!-- /ficha -->

## Ficha del recurso: MedicationAdministration

**¿Qué es?** El registro de que un medicamento **se administró** a un
paciente: cuándo, cuánto, por qué vía y quién.

**¿Para qué se usa?** Para la hoja de administración de medicamentos de
enfermería, la quimioterapia, los tratamientos supervisados (como el de la
tuberculosis) y la trazabilidad de cada dosis.

**Elementos principales** (<https://hl7.org/fhir/R4/medicationadministration.html>):

<!-- ficha MedicationAdministration -->
| Elemento | Card. | Tipo | Para qué sirve |
|---|---|---|---|
| `status` ⚑ | **1..1** | code | `in-progress`, `not-done`, `on-hold`, `completed`, `entered-in-error`, `stopped`. |
| `statusReason` | 0..* | CodeableConcept | Por qué no se administró. |
| `category` | 0..1 | CodeableConcept | `inpatient`, `outpatient` o `community`. |
| `medication[x]` | **1..1** | CodeableConcept \| Reference(Medication) | Qué medicamento. |
| `subject` | **1..1** | Reference(Patient \| Group) | A quién. |
| `context` | 0..1 | Reference(Encounter \| EpisodeOfCare) | En qué atención. |
| `supportingInformation` | 0..* | Reference(Resource) | Datos que la justifican. |
| `effective[x]` | **1..1** | dateTime \| Period | Cuándo: un momento o un periodo (una infusión). |
| `performer` | 0..* | BackboneElement | Quién la administró. |
| `reasonCode` | 0..* | CodeableConcept | Por qué, codificado. |
| `reasonReference` | 0..* | Reference(Condition \| Observation \| DiagnosticReport) | Por qué, como referencia. |
| `request` | 0..1 | Reference(MedicationRequest) | La orden que se cumple. |
| `note` | 0..* | Annotation | Notas: eventos, observaciones. |
| `dosage` | 0..1 | BackboneElement | Lo que se administró realmente. |
| `dosage.route` | 0..1 | CodeableConcept | Por qué vía. |
| `dosage.dose` | 0..1 | Quantity | Cuánto. |
| `dosage.rate[x]` | 0..1 | Ratio \| Quantity | A qué velocidad (en una infusión). |
<!-- /ficha -->

**La estructura `Dosage`**, que se usa en MedicationRequest,
MedicationStatement y otros, combina siempre dos cosas:

- `text`: la indicación como la leería una persona ("20 mg por vía oral una
  vez al día, durante 5 años");
- datos estructurados para las máquinas: `timing` (frecuencia y duración),
  `route` (vía) y `doseAndRate` (dosis).

---

## Paso a paso: la superficie corporal

La dosis de quimioterapia depende de la superficie corporal, así que primero
se registra como observación (LOINC `8277-6`, categoría `vital-signs`). Ya
sabes construirla (módulo 06):
[`15a_observation_superficie_corporal.json`](soluciones/15a_observation_superficie_corporal.json).

## Paso a paso: la prescripción de doxorrubicina

### Paso 1 · El mínimo: estado, intención, medicamento y paciente

<!-- paso 15b 1 -->
```json
{
  "resourceType": "MedicationRequest",
  "status": "active",
  "intent": "order",
  "medicationCodeableConcept": {
    "coding": [
      {
        "system": "http://snomed.info/sct",
        "code": "372817009",
        "display": "Doxorubicin"
      }
    ],
    "text": "Doxorrubicina"
  },
  "subject": {
    "reference": "Patient/{{patientId}}",
    "display": "Luis Alberto Paredes Cevallos"
  }
}
```
<!-- /paso -->

`intent: order` dice que es una **orden** que se debe cumplir. Una propuesta
del comité de tumores sería `proposal`; un plan, `plan`.

### Paso 2 · Quién, cuándo y por qué

<!-- paso 15b 2 -->
```json
{
  "category": [
    {
      "coding": [
        {
          "system": "http://terminology.hl7.org/CodeSystem/medicationrequest-category",
          "code": "outpatient",
          "display": "Outpatient"
        }
      ]
    }
  ],
  "authoredOn": "2025-07-01",
  "requester": {
    "reference": "Practitioner/{{practitionerId}}",
    "display": "Dra. Andrea Lucía Salazar Moreno"
  },
  "reasonReference": [
    {
      "reference": "Condition/{{conditionCancerId}}",
      "display": "Carcinoma ductal infiltrante de mama izquierda"
    }
  ]
}
```
<!-- /paso -->

### Paso 3 · La dosis: texto y datos estructurados

<!-- paso 15b 3 -->
```json
{
  "dosageInstruction": [
    {
      "text": "60 mg/m² (106,2 mg) por vía intravenosa cada 21 días, 4 ciclos",
      "timing": {
        "repeat": {
          "count": 4,
          "frequency": 1,
          "period": 21,
          "periodUnit": "d"
        }
      },
      "route": {
        "coding": [
          {
            "system": "http://snomed.info/sct",
            "code": "47625008",
            "display": "Intravenous route"
          }
        ],
        "text": "Vía intravenosa"
      },
      "doseAndRate": [
        {
          "doseQuantity": {
            "value": 106.2,
            "unit": "mg",
            "system": "http://unitsofmeasure.org",
            "code": "mg"
          }
        }
      ]
    }
  ]
}
```
<!-- /paso -->

`timing.repeat`: una vez (`frequency: 1`) cada 21 días (`period: 21`,
`periodUnit: d`), 4 veces (`count: 4`). La vía intravenosa con SNOMED
`47625008` y la dosis con UCUM (`mg`).

### Paso 4 · La justificación: superficie corporal

<!-- paso 15b 4 -->
```json
{
  "supportingInformation": [
    {
      "reference": "Observation/{{obsBSAId}}",
      "display": "Superficie corporal 1,77 m²"
    }
  ],
  "identifier": [
    {
      "system": "https://f-slg.github.io/aprende-fhir/sid/receta",
      "value": "RX-2025-0101"
    }
  ],
  "text": {
    "status": "generated",
    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><p>Doxorrubicina 60 mg/m² (106,2 mg) IV cada 21 días, 4 ciclos.</p></div>"
  }
}
```
<!-- /paso -->

`supportingInformation` apunta a la observación de 1,77 m²: cualquiera puede
verificar el cálculo de 60 mg/m² × 1,77 m² = 106,2 mg. Solución:
[`15b_medicationrequest_doxorrubicina.json`](soluciones/15b_medicationrequest_doxorrubicina.json).

## Paso a paso: la administración del primer ciclo

### Paso 1 · El mínimo: estado, medicamento, paciente y momento

<!-- paso 15c 1 -->
```json
{
  "resourceType": "MedicationAdministration",
  "status": "completed",
  "medicationCodeableConcept": {
    "coding": [
      {
        "system": "http://snomed.info/sct",
        "code": "372817009",
        "display": "Doxorubicin"
      }
    ],
    "text": "Doxorrubicina"
  },
  "subject": {
    "reference": "Patient/{{patientId}}",
    "display": "Luis Alberto Paredes Cevallos"
  },
  "effectivePeriod": {
    "start": "2025-07-02T09:00:00-05:00",
    "end": "2025-07-02T09:30:00-05:00"
  }
}
```
<!-- /paso -->

`effectivePeriod`, no `effectiveDateTime`: una infusión dura un tiempo, de
09:00 a 09:30.

### Paso 2 · Quién la administró y por qué orden

<!-- paso 15c 2 -->
```json
{
  "category": {
    "coding": [
      {
        "system": "http://terminology.hl7.org/CodeSystem/medication-admin-category",
        "code": "outpatient",
        "display": "Outpatient"
      }
    ]
  },
  "performer": [
    {
      "actor": {
        "reference": "Practitioner/{{practitionerId}}",
        "display": "Dra. Andrea Lucía Salazar Moreno"
      }
    }
  ],
  "request": {
    "reference": "MedicationRequest/{{medReqDoxoId}}",
    "display": "Doxorrubicina 60 mg/m²"
  },
  "reasonReference": [
    {
      "reference": "Condition/{{conditionCancerId}}",
      "display": "Carcinoma ductal infiltrante de mama izquierda"
    }
  ],
  "supportingInformation": [
    {
      "reference": "Observation/{{obsBSAId}}",
      "display": "Superficie corporal 1,77 m²"
    }
  ]
}
```
<!-- /paso -->

`request` enlaza la administración con la receta: así se sabe qué orden se
está cumpliendo.

### Paso 3 · Cuánto y cómo se administró

<!-- paso 15c 3 -->
```json
{
  "dosage": {
    "text": "106,2 mg diluidos en 100 mL de solución salina, en 30 minutos",
    "route": {
      "coding": [
        {
          "system": "http://snomed.info/sct",
          "code": "47625008",
          "display": "Intravenous route"
        }
      ],
      "text": "Vía intravenosa"
    },
    "dose": {
      "value": 106.2,
      "unit": "mg",
      "system": "http://unitsofmeasure.org",
      "code": "mg"
    },
    "rateQuantity": {
      "value": 200,
      "unit": "mL/h",
      "system": "http://unitsofmeasure.org",
      "code": "mL/h"
    }
  },
  "text": {
    "status": "generated",
    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><p>Primer ciclo de doxorrubicina: 106,2 mg IV en 30 minutos, 2 de julio de 2025.</p></div>"
  }
}
```
<!-- /paso -->

`rateQuantity`: 200 mL/h, la velocidad de la infusión. Solución:
[`15c_medicationadministration_doxorrubicina.json`](soluciones/15c_medicationadministration_doxorrubicina.json).

**15d · El evento posterior.** Las náuseas se registran con una nota en la
misma administración. Lo que cambia:

<!-- diferencia 15d -->
```json
{
  "id": "{{medAdminDoxoId}}",
  "note": [
    {
      "time": "2025-07-02T11:00:00-05:00",
      "text": "Náuseas grado 1 dos horas después de la infusión; se administró ondansetrón 8 mg VO."
    }
  ]
}
```
<!-- /diferencia -->

## El tamoxifeno: otra receta, otro ciclo de vida

La receta de tamoxifeno sigue el mismo modelo que la de doxorrubicina. Lo que
cambia:

<!-- diferencia 15e -->
```json
{
  "identifier": [
    {
      "system": "https://f-slg.github.io/aprende-fhir/sid/receta",
      "value": "RX-2025-0207"
    }
  ],
  "medicationCodeableConcept": {
    "coding": [
      {
        "system": "http://snomed.info/sct",
        "code": "373345002",
        "display": "Tamoxifen"
      }
    ],
    "text": "Tamoxifeno"
  },
  "authoredOn": "2025-10-15",
  "dosageInstruction": [
    {
      "text": "20 mg por vía oral una vez al día, durante 5 años",
      "timing": {
        "repeat": {
          "frequency": 1,
          "period": 1,
          "periodUnit": "d",
          "boundsDuration": {
            "value": 5,
            "unit": "años",
            "system": "http://unitsofmeasure.org",
            "code": "a"
          }
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
            "value": 20,
            "unit": "mg",
            "system": "http://unitsofmeasure.org",
            "code": "mg"
          }
        }
      ]
    }
  ],
  "dispenseRequest": {
    "numberOfRepeatsAllowed": 11,
    "quantity": {
      "value": 30,
      "unit": "comprimidos"
    },
    "expectedSupplyDuration": {
      "value": 30,
      "unit": "días",
      "system": "http://unitsofmeasure.org",
      "code": "d"
    }
  }
}
```
<!-- /diferencia -->

Fíjate en `dispenseRequest`: 30 comprimidos por entrega, para 30 días, con 11
repeticiones (un año de tratamiento por receta). Solución:
[`15e_medicationrequest_tamoxifeno.json`](soluciones/15e_medicationrequest_tamoxifeno.json).

La primera dosis la toma **el propio Luis en su casa**: la administración
tiene `category: community` y `performer` es el paciente
([`15f_medicationadministration_tamoxifeno.json`](soluciones/15f_medicationadministration_tamoxifeno.json)).

**15g · Suspender.** En febrero de 2026 la receta se suspende. No se borra:
se actualiza con `status: stopped` y el motivo. Lo que cambia:

<!-- diferencia 15g -->
```json
{
  "id": "{{medReqTamoxId}}",
  "status": "stopped",
  "statusReason": {
    "text": "Intolerancia: sofocos intensos y dolor articular"
  },
  "note": [
    {
      "time": "2026-02-10T10:00:00-05:00",
      "text": "Se suspende el tamoxifeno por intolerancia; se valorará una alternativa en oncología."
    }
  ]
}
```
<!-- /diferencia -->

---

## Ejercicios en el servidor

| Paso | Petición | Guarda |
|---|---|---|
| 15a | `POST /Observation` (superficie corporal) | `obsBSAId` |
| 15b | `POST /MedicationRequest` (doxorrubicina) | `medReqDoxoId` |
| 15c | `POST /MedicationAdministration` | `medAdminDoxoId` |
| 15d | `PUT /MedicationAdministration/{{medAdminDoxoId}}` | |
| 15e | `POST /MedicationRequest` (tamoxifeno) | `medReqTamoxId` |
| 15f | `POST /MedicationAdministration` | `medAdminTamoxId` |
| 15g | `PUT /MedicationRequest/{{medReqTamoxId}}` (stopped) | |

### 15h y 15i · Error a propósito: la receta sin intención

Envía ([`15e1_receta_sin_intencion.json`](errores/15e1_receta_sin_intencion.json))
una receta sin `intent`. **El servidor responde `201 Created`.** El validador
lo detecta:

```
MedicationRequest.intent: minimum required = 1, but only found 0
```

¿Es una orden o una propuesta? Sin `intent`, una farmacia no sabe si debe
dispensar. Bórrala con `DELETE {{FHIRURL}}/MedicationRequest/{{errorMedReqId}}`.

### 15j · El expediente completo

```http
GET {{FHIRURL}}/Patient/{{patientId}}/$everything
```

`$everything` es una **operación**: las operaciones empiezan con `$` y hacen
algo más que leer o buscar. Esta devuelve el paciente y **todo** lo que se
relaciona con él. Cuenta cuántos recursos de cada tipo creaste durante el
taller.

## Autoevaluación

<details><summary>1. La enfermera registra que administró la dosis de las 08:00. ¿Qué recurso?</summary>

**MedicationAdministration**, con `request` apuntando a la MedicationRequest
que se cumple.
</details>

<details><summary>2. ¿Por qué no se borra la receta de tamoxifeno al suspenderla?</summary>

Porque es parte de la historia del paciente: se prescribió, se tomó y se
suspendió por intolerancia. Esa información sirve para no volver a
indicarlo. Se actualiza a `stopped` con su `statusReason`.
</details>

<details><summary>3. ¿Para qué sirve <code>supportingInformation</code> en la receta de doxorrubicina?</summary>

Para enlazar los datos que justifican la dosis (la superficie corporal), de
modo que se pueda verificar el cálculo.
</details>

## Resumen

- **MedicationRequest** es la orden; **MedicationAdministration**, lo que se
  administró; `request` las enlaza.
- `Dosage` combina un texto para personas y datos estructurados.
- Una receta se suspende con `stopped`, no se borra.
- `$everything` devuelve todo el expediente de un paciente.

## ¿Qué sigue?

Completaste los módulos disponibles. En las próximas etapas del taller:

- **10 · Órdenes y derivación:** ServiceRequest, PractitionerRole, Location.
- **12 · Plan y consentimiento:** CarePlan, Goal, Consent.
- **14 · Citas:** Schedule, Slot, Appointment (como en
  [Agenda FHIR](https://github.com/f-slg/agenda-fhir-r)).
- **16 · Seguimiento:** Questionnaire, QuestionnaireResponse.
- **17 a 19 · Avanzado:** búsquedas avanzadas, terminologías y perfiles, y
  el resumen internacional del paciente (IPS).

## Ejecutar este módulo

- **Postman:** carpeta *15 · Medicamentos*.
- **curl:** `curl/taller.sh` (todo el taller)
- **R:**

  ```r
  todo <- fhir_leer("Patient/{{patientId}}/$everything?_count=200")
  table(vapply(todo$entry, function(e) e$resource$resourceType, ""))
  ```
