# Módulo 12 · Plan y consentimiento

[← Módulo 11](../11-anatomia-patologica/README.md) · [Inicio](../../README.md) · [Módulo 13 →](../13-procedimientos/README.md)

> **Nivel:** intermedio · **Duración:** 75 minutos · **Necesitas:** módulos 10 y 11

## Lo que vas a aprender

1. A representar un **equipo** de atención con CareTeam.
2. A definir **metas** de tratamiento con Goal.
3. A registrar un **plan de tratamiento** con sus actividades (CarePlan).
4. A registrar un **consentimiento informado** (Consent).

## La historia

Con el diagnóstico confirmado (módulo 11), el **20 de mayo de 2025** se reúne
el **comité de tumores de mama** del hospital, coordinado por el Dr. Ruiz,
con la Dra. Salazar como médica de cabecera. El comité acuerda:

| Metas | Plan |
|---|---|
| Sin evidencia de enfermedad al terminar el tratamiento | 1. Mastectomía parcial |
| Mantener la funcionalidad (ECOG 0 a 1) | 2. Quimioterapia con doxorrubicina, 4 ciclos |
| | 3. Hormonoterapia con tamoxifeno, 5 años |

El **27 de mayo**, después de que el equipo le explicara la cirugía, sus
riesgos y sus alternativas, Luis **firma el consentimiento informado** para
la mastectomía parcial.

---

## Ficha del recurso: CareTeam

**¿Qué es?** Un **grupo de personas** que participa en la atención de un
paciente: un comité de tumores, el equipo de un programa de crónicos, el
equipo de cuidados paliativos. Puede incluir al paciente y a su familia.

**¿Para qué se usa?** Para decir **quiénes** son responsables de un paciente
o de un plan, y con qué rol cada uno.

**¿Cuándo usar otro recurso?** Un grupo de personas sin relación con un
paciente concreto (por ejemplo, "el personal de oncología") es un **Group** o
una **Organization**.

<!-- ficha CareTeam -->
| Elemento | Card. | Tipo | Para qué sirve |
|---|---|---|---|
| `identifier` | 0..* | Identifier | Identificador del equipo. |
| `status` ⚑ | 0..1 | code | `proposed`, `active`, `suspended`, `inactive` o `entered-in-error`. |
| `category` | 0..* | CodeableConcept | Clase de equipo. |
| `name` | 0..1 | string | Nombre. |
| `subject` | 0..1 | Reference(Patient \| Group) | El paciente que atiende. |
| `period` | 0..1 | Period | Desde y hasta cuándo funciona. |
| `participant` | 0..* | BackboneElement | Sus integrantes. |
| `participant.role` | 0..* | CodeableConcept | El rol de cada uno. |
| `participant.member` | 0..1 | Reference(Practitioner \| PractitionerRole \| RelatedPerson \| Patient \| …) | La persona o el rol profesional. |
| `reasonReference` | 0..* | Reference(Condition) | El problema de salud por el que existe el equipo. |
| `managingOrganization` | 0..* | Reference(Organization) | La organización responsable. |
| `note` | 0..* | Annotation | Notas. |
<!-- /ficha -->

## Ficha del recurso: Goal

**¿Qué es?** Un **resultado deseado** para el paciente: bajar la presión a
menos de 140/90, perder 5 kg, dejar de fumar, sin evidencia de enfermedad.

**¿Para qué se usa?** Para que el plan tenga **metas medibles** y se pueda
evaluar si se alcanzaron.

<!-- ficha Goal -->
| Elemento | Card. | Tipo | Para qué sirve |
|---|---|---|---|
| `identifier` | 0..* | Identifier | Identificador de la meta. |
| `lifecycleStatus` ⚑ | **1..1** | code | `proposed`, `planned`, `accepted`, `active`, `on-hold`, `completed`, `cancelled`... |
| `achievementStatus` | 0..1 | CodeableConcept | ¿Se está logrando? `in-progress`, `improving`, `worsening`, `achieved`, `not-achieved`... |
| `category` | 0..* | CodeableConcept | Clase de meta: tratamiento, dietética, conductual. |
| `priority` | 0..1 | CodeableConcept | Prioridad: alta, media o baja. |
| `description` | **1..1** | CodeableConcept | **Qué** se quiere lograr. |
| `subject` | **1..1** | Reference(Patient \| Group \| Organization) | Para quién. |
| `start[x]` | 0..1 | date \| CodeableConcept | Cuándo empieza. |
| `target` | 0..* | BackboneElement | El objetivo medible y su plazo. |
| `target.measure` | 0..1 | CodeableConcept | Qué se mide (por ejemplo, la presión sistólica). |
| `target.detail[x]` | 0..1 | Quantity \| Range \| CodeableConcept \| string \| … | El valor que se quiere alcanzar. |
| `target.due[x]` | 0..1 | date \| Duration | Para cuándo. |
| `expressedBy` | 0..1 | Reference(Patient \| Practitioner \| PractitionerRole \| RelatedPerson) | Quién propone la meta. |
| `addresses` | 0..* | Reference(Condition \| Observation \| MedicationStatement \| NutritionOrder \| …) | El problema de salud al que responde. |
| `outcomeReference` | 0..* | Reference(Observation) | Las observaciones que muestran el resultado. |
<!-- /ficha -->

`lifecycleStatus` (¿en qué etapa está la meta?) y `achievementStatus` (¿se
está cumpliendo?) son dos preguntas distintas, igual que los dos estados de
Condition (módulo 05).

## Ficha del recurso: CarePlan

**¿Qué es?** El **plan de atención** de un paciente: qué se va a hacer, para
qué problema, con qué metas y quiénes participan.

**¿Para qué se usa?** Para planes de tratamiento oncológico, planes de
enfermería, planes de control de crónicos, planes de rehabilitación. Las
órdenes y prescripciones que lo ejecutan pueden apuntar a él con `basedOn`.

<!-- ficha CarePlan -->
| Elemento | Card. | Tipo | Para qué sirve |
|---|---|---|---|
| `identifier` | 0..* | Identifier | Identificador del plan. |
| `status` ⚑ | **1..1** | code | `draft`, `active`, `on-hold`, `revoked`, `completed`, `entered-in-error`. |
| `intent` ⚑ | **1..1** | code | `proposal`, `plan`, `order` u `option`. |
| `category` | 0..* | CodeableConcept | Clase de plan. |
| `title` | 0..1 | string | Título. |
| `description` | 0..1 | string | Descripción. |
| `subject` | **1..1** | Reference(Patient \| Group) | Para quién. |
| `period` | 0..1 | Period | Periodo que cubre. |
| `created` | 0..1 | dateTime | Cuándo se creó. |
| `author` | 0..1 | Reference(Patient \| Practitioner \| PractitionerRole \| Device \| …) | Quién es responsable del plan. |
| `careTeam` | 0..* | Reference(CareTeam) | El equipo que lo ejecuta. |
| `addresses` | 0..* | Reference(Condition) | Los problemas de salud que atiende. |
| `goal` | 0..* | Reference(Goal) | Las metas. |
| `activity` | 0..* | BackboneElement | Las actividades. |
| `activity.reference` | 0..1 | Reference(Appointment \| CommunicationRequest \| DeviceRequest \| MedicationRequest \| …) | Una actividad como referencia a una orden ya creada. |
| `activity.detail` | 0..1 | BackboneElement | Una actividad descrita dentro del plan. |
| `activity.detail.kind` | 0..1 | code | Qué tipo de recurso sería: ServiceRequest, MedicationRequest... |
| `activity.detail.code` | 0..1 | CodeableConcept | Qué actividad es. |
| `activity.detail.status` ⚑ | **1..1** | code | Estado: `not-started`, `scheduled`, `in-progress`, `completed`... |
| `activity.detail.scheduled[x]` | 0..1 | Timing \| Period \| string | Cuándo. |
| `activity.detail.performer` | 0..* | Reference(Practitioner \| PractitionerRole \| Organization \| RelatedPerson \| …) | Quién la hace. |
| `activity.detail.description` | 0..1 | string | Descripción. |
| `note` | 0..* | Annotation | Notas. |
<!-- /ficha -->

Cada actividad se puede expresar de dos maneras: `activity.reference`, si la
orden ya existe, o `activity.detail`, describiéndola dentro del plan. Aquí
usamos `detail`, porque al momento del comité todavía no se han emitido las
órdenes.

## Ficha del recurso: Consent

**¿Qué es?** El registro de una **decisión del paciente** (o de su
representante) de permitir o negar algo: un tratamiento, el uso de sus datos,
participar en una investigación, una directiva anticipada.

**¿Para qué se usa?** Aquí, para el **consentimiento informado** de la
cirugía. También se usa para controlar quién puede ver qué información del
paciente.

<!-- ficha Consent -->
| Elemento | Card. | Tipo | Para qué sirve |
|---|---|---|---|
| `identifier` | 0..* | Identifier | Número del consentimiento. |
| `status` ⚑ | **1..1** | code | `draft`, `proposed`, `active`, `rejected`, `inactive` o `entered-in-error`. |
| `scope` ⚑ | **1..1** | CodeableConcept | Alcance: `treatment`, `patient-privacy`, `research` o `adr` (directiva anticipada). |
| `category` | **1..*** | CodeableConcept | Clase de documento de consentimiento. |
| `patient` | 0..1 | Reference(Patient) | El paciente. |
| `dateTime` | 0..1 | dateTime | Cuándo se otorgó. |
| `performer` | 0..* | Reference(Organization \| Patient \| Practitioner \| RelatedPerson \| …) | Quién lo otorga: el paciente o su representante. |
| `organization` | 0..* | Reference(Organization) | Ante qué organización. |
| `source[x]` | 0..1 | Attachment \| Reference(Consent \| DocumentReference \| Contract \| QuestionnaireResponse) | El documento firmado (un PDF escaneado, por ejemplo). |
| `policy` | 0..* | BackboneElement | Las normas en que se basa. |
| `policyRule` | 0..1 | CodeableConcept | La norma, codificada. |
| `provision` | 0..1 | BackboneElement | **Qué** se permite o se niega. |
| `provision.type` | 0..1 | code | `permit` (se permite) o `deny` (se niega). |
| `provision.period` | 0..1 | Period | Durante qué periodo. |
| `provision.actor` | 0..* | BackboneElement | A quién se le permite. |
| `provision.code` | 0..* | CodeableConcept | Sobre qué procedimiento o dato. |
<!-- /ficha -->

Una regla de Consent (`ppc-1`): debe tener `policy` o `policyRule`, es decir,
decir **según qué norma** se otorga.

---

## Paso a paso: el comité de tumores

### Paso 1 · El mínimo: estado, nombre y paciente

<!-- paso 12a 1 -->
```json
{
  "resourceType": "CareTeam",
  "status": "active",
  "name": "Comité de tumores de mama",
  "subject": {
    "reference": "Patient/{{patientId}}",
    "display": "Luis Alberto Paredes Cevallos"
  }
}
```
<!-- /paso -->

### Paso 2 · Quiénes lo integran y con qué rol

<!-- paso 12a 2 -->
```json
{
  "participant": [
    {
      "role": [
        {
          "text": "Oncólogo clínico, coordinador del comité"
        }
      ],
      "member": {
        "reference": "PractitionerRole/{{oncologistRoleId}}",
        "display": "Dr. Ruiz · Oncología clínica"
      }
    },
    {
      "role": [
        {
          "text": "Médica de cabecera"
        }
      ],
      "member": {
        "reference": "PractitionerRole/{{salazarRoleId}}",
        "display": "Dra. Salazar · Medicina general"
      }
    }
  ]
}
```
<!-- /paso -->

Cada `member` apunta a un **PractitionerRole** (módulo 10): no solo quién,
sino en qué puesto. El rol se escribe con `text` porque no hay un código
estándar para "coordinador del comité".

### Paso 3 · Desde cuándo, de qué organización y por qué

<!-- paso 12a 3 -->
```json
{
  "period": {
    "start": "2025-05-20"
  },
  "managingOrganization": [
    {
      "reference": "Organization/{{hospitalId}}",
      "display": "Hospital General Docente Ejemplo"
    }
  ],
  "reasonReference": [
    {
      "reference": "Condition/{{conditionCancerId}}",
      "display": "Carcinoma ductal infiltrante de mama izquierda"
    }
  ],
  "identifier": [
    {
      "system": "https://f-slg.github.io/aprende-fhir/sid/equipo",
      "value": "CT-MAMA-0001"
    }
  ],
  "text": {
    "status": "generated",
    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><p>Comité de tumores de mama del Hospital General Docente Ejemplo:</p><p>Dr. Ruiz (oncología clínica, coordinador) y Dra. Salazar (medicina general).</p></div>"
  }
}
```
<!-- /paso -->

Solución: [`12a_careteam_comite.json`](soluciones/12a_careteam_comite.json).

## Paso a paso: las metas

### Paso 1 · El mínimo: estado, descripción y paciente

<!-- paso 12b 1 -->
```json
{
  "resourceType": "Goal",
  "lifecycleStatus": "active",
  "description": {
    "text": "Sin evidencia de enfermedad al terminar el tratamiento"
  },
  "subject": {
    "reference": "Patient/{{patientId}}",
    "display": "Luis Alberto Paredes Cevallos"
  }
}
```
<!-- /paso -->

`description` es un CodeableConcept. Cuando no hay un código adecuado, basta
con `text`.

### Paso 2 · Avance, prioridad y plazo

<!-- paso 12b 2 -->
```json
{
  "achievementStatus": {
    "coding": [
      {
        "system": "http://terminology.hl7.org/CodeSystem/goal-achievement",
        "code": "in-progress",
        "display": "In Progress"
      }
    ],
    "text": "En curso"
  },
  "priority": {
    "coding": [
      {
        "system": "http://terminology.hl7.org/CodeSystem/goal-priority",
        "code": "high-priority",
        "display": "High Priority"
      }
    ],
    "text": "Alta"
  },
  "startDate": "2025-05-20",
  "target": [
    {
      "dueDate": "2026-06-30"
    }
  ]
}
```
<!-- /paso -->

`target.dueDate`: el plazo para evaluarla, junio de 2026.

### Paso 3 · A qué problema responde y quién la propone

<!-- paso 12b 3 -->
```json
{
  "addresses": [
    {
      "reference": "Condition/{{conditionCancerId}}",
      "display": "Carcinoma ductal infiltrante de mama izquierda"
    }
  ],
  "expressedBy": {
    "reference": "PractitionerRole/{{oncologistRoleId}}",
    "display": "Dr. Ruiz · Oncología clínica"
  },
  "identifier": [
    {
      "system": "https://f-slg.github.io/aprende-fhir/sid/meta",
      "value": "META-0001"
    }
  ],
  "text": {
    "status": "generated",
    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><p>Meta: sin evidencia de enfermedad al terminar el tratamiento.</p></div>"
  }
}
```
<!-- /paso -->

Solución: [`12b_goal_control_enfermedad.json`](soluciones/12b_goal_control_enfermedad.json).
La segunda meta cambia la descripción y la prioridad:

<!-- diferencia 12c -->
```json
{
  "identifier": [
    {
      "system": "https://f-slg.github.io/aprende-fhir/sid/meta",
      "value": "META-0002"
    }
  ],
  "priority": {
    "coding": [
      {
        "system": "http://terminology.hl7.org/CodeSystem/goal-priority",
        "code": "medium-priority",
        "display": "Medium Priority"
      }
    ],
    "text": "Media"
  },
  "description": {
    "text": "Mantener la funcionalidad durante el tratamiento (ECOG 0 a 1)"
  }
}
```
<!-- /diferencia -->

## Paso a paso: el plan de tratamiento

### Paso 1 · El mínimo: estado, intención y paciente

<!-- paso 12d 1 -->
```json
{
  "resourceType": "CarePlan",
  "status": "active",
  "intent": "plan",
  "subject": {
    "reference": "Patient/{{patientId}}",
    "display": "Luis Alberto Paredes Cevallos"
  }
}
```
<!-- /paso -->

`intent: plan`: es un plan acordado, no una orden. Las órdenes concretas
(la cirugía, las recetas) vendrán después.

### Paso 2 · Qué plan es, de cuándo y de quién

<!-- paso 12d 2 -->
```json
{
  "category": [
    {
      "text": "Plan de tratamiento oncológico"
    }
  ],
  "title": "Plan de tratamiento del cáncer de mama",
  "description": "Tratamiento acordado por el comité de tumores de mama.",
  "period": {
    "start": "2025-05-20",
    "end": "2030-10-31"
  },
  "created": "2025-05-20",
  "author": {
    "reference": "PractitionerRole/{{oncologistRoleId}}",
    "display": "Dr. Ruiz · Oncología clínica"
  }
}
```
<!-- /paso -->

### Paso 3 · El equipo, el problema y las metas

<!-- paso 12d 3 -->
```json
{
  "careTeam": [
    {
      "reference": "CareTeam/{{careTeamId}}",
      "display": "Comité de tumores de mama"
    }
  ],
  "addresses": [
    {
      "reference": "Condition/{{conditionCancerId}}",
      "display": "Carcinoma ductal infiltrante de mama izquierda"
    }
  ],
  "goal": [
    {
      "reference": "Goal/{{goalControlId}}",
      "display": "Sin evidencia de enfermedad"
    },
    {
      "reference": "Goal/{{goalQualityId}}",
      "display": "Mantener la funcionalidad"
    }
  ]
}
```
<!-- /paso -->

### Paso 4 · Las actividades: cirugía, quimioterapia y hormonoterapia

<!-- paso 12d 4 -->
```json
{
  "activity": [
    {
      "detail": {
        "kind": "ServiceRequest",
        "code": {
          "coding": [
            {
              "system": "http://snomed.info/sct",
              "code": "64368001",
              "display": "Partial mastectomy"
            }
          ],
          "text": "Mastectomía parcial"
        },
        "status": "scheduled",
        "scheduledPeriod": {
          "start": "2025-06-10",
          "end": "2025-06-10"
        },
        "performer": [
          {
            "reference": "PractitionerRole/{{oncologistRoleId}}",
            "display": "Dr. Ruiz · Oncología clínica"
          }
        ],
        "description": "Mastectomía parcial de la mama izquierda"
      }
    },
    {
      "detail": {
        "kind": "MedicationRequest",
        "code": {
          "coding": [
            {
              "system": "http://snomed.info/sct",
              "code": "367336001",
              "display": "Chemotherapy"
            }
          ],
          "text": "Quimioterapia"
        },
        "status": "not-started",
        "scheduledPeriod": {
          "start": "2025-07-01",
          "end": "2025-09-30"
        },
        "performer": [
          {
            "reference": "PractitionerRole/{{oncologistRoleId}}",
            "display": "Dr. Ruiz · Oncología clínica"
          }
        ],
        "description": "Doxorrubicina 60 mg/m² cada 21 días, 4 ciclos"
      }
    },
    {
      "detail": {
        "kind": "MedicationRequest",
        "code": {
          "coding": [
            {
              "system": "http://snomed.info/sct",
              "code": "169413002",
              "display": "Hormone therapy"
            }
          ],
          "text": "Hormonoterapia"
        },
        "status": "not-started",
        "scheduledPeriod": {
          "start": "2025-10-15",
          "end": "2030-10-15"
        },
        "performer": [
          {
            "reference": "PractitionerRole/{{oncologistRoleId}}",
            "display": "Dr. Ruiz · Oncología clínica"
          }
        ],
        "description": "Tamoxifeno 20 mg diarios por 5 años"
      }
    }
  ],
  "identifier": [
    {
      "system": "https://f-slg.github.io/aprende-fhir/sid/plan",
      "value": "PLAN-2025-0001"
    }
  ],
  "text": {
    "status": "generated",
    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><p>Plan de tratamiento del comité de tumores (20 de mayo de 2025):</p><p>1) mastectomía parcial; 2) quimioterapia con doxorrubicina, 4 ciclos; 3) hormonoterapia con tamoxifeno por 5 años.</p></div>"
  }
}
```
<!-- /paso -->

Cada actividad tiene su `kind` (qué recurso la ejecutará), su código SNOMED
CT, su estado y su periodo. La cirugía está `scheduled` (programada); las
otras dos, `not-started`. Solución:
[`12d_careplan_oncologico.json`](soluciones/12d_careplan_oncologico.json).

En el módulo 13, la cirugía tendrá `basedOn` apuntando a este plan.

## Paso a paso: el consentimiento informado

### Paso 1 · El mínimo: estado, alcance, categoría, paciente y norma

<!-- paso 12e 1 -->
```json
{
  "resourceType": "Consent",
  "status": "active",
  "scope": {
    "coding": [
      {
        "system": "http://terminology.hl7.org/CodeSystem/consentscope",
        "code": "treatment",
        "display": "Treatment"
      }
    ],
    "text": "Tratamiento"
  },
  "category": [
    {
      "coding": [
        {
          "system": "http://loinc.org",
          "code": "59284-0",
          "display": "Patient Consent"
        }
      ],
      "text": "Consentimiento del paciente"
    }
  ],
  "patient": {
    "reference": "Patient/{{patientId}}",
    "display": "Luis Alberto Paredes Cevallos"
  },
  "policyRule": {
    "text": "Consentimiento informado para procedimientos quirúrgicos (normativa nacional)"
  }
}
```
<!-- /paso -->

Seis elementos desde el inicio: `status`, `scope` y `category` son
obligatorios, y la regla `ppc-1` exige `policy` o `policyRule`. El alcance es
`treatment` y la categoría, LOINC `59284-0` *Patient Consent*.

> **Sobre un aviso del validador.** `policyRule` solo tiene `text` y el
> validador avisa: *"No code provided, and a code should be provided from the
> value set 'Consent PolicyRule Codes'"*. Esa lista (*extensible*, como en el
> módulo 02) tiene normas de otros países; la ecuatoriana no está. Un texto
> claro es mejor que un código equivocado.

### Paso 2 · Cuándo, quién lo otorga y ante qué organización

<!-- paso 12e 2 -->
```json
{
  "dateTime": "2025-05-27T10:00:00-05:00",
  "performer": [
    {
      "reference": "Patient/{{patientId}}",
      "display": "Luis Alberto Paredes Cevallos"
    }
  ],
  "organization": [
    {
      "reference": "Organization/{{hospitalId}}",
      "display": "Hospital General Docente Ejemplo"
    }
  ]
}
```
<!-- /paso -->

`performer` es el propio Luis: quien otorga el consentimiento.

### Paso 3 · Qué se autoriza: la disposición

<!-- paso 12e 3 -->
```json
{
  "provision": {
    "type": "permit",
    "period": {
      "start": "2025-05-27",
      "end": "2025-07-31"
    },
    "actor": [
      {
        "role": {
          "text": "Equipo quirúrgico tratante"
        },
        "reference": {
          "reference": "PractitionerRole/{{oncologistRoleId}}",
          "display": "Dr. Ruiz · Oncología clínica"
        }
      }
    ],
    "code": [
      {
        "coding": [
          {
            "system": "http://snomed.info/sct",
            "code": "64368001",
            "display": "Partial mastectomy"
          }
        ],
        "text": "Mastectomía parcial"
      }
    ]
  },
  "identifier": [
    {
      "system": "https://f-slg.github.io/aprende-fhir/sid/consentimiento",
      "value": "CI-2025-0007"
    }
  ],
  "text": {
    "status": "generated",
    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><p>Consentimiento informado para la mastectomía parcial de la mama izquierda,</p><p>firmado por el paciente el 27 de mayo de 2025.</p></div>"
  }
}
```
<!-- /paso -->

`provision.type: permit` (se autoriza), `code`: la mastectomía parcial,
`actor`: el equipo tratante, y `period`: hasta el 31 de julio. Solución:
[`12e_consent_cirugia.json`](soluciones/12e_consent_cirugia.json).

---

## Ejercicios en el servidor

| Paso | Petición | Guarda |
|---|---|---|
| 12a | `POST /CareTeam` | `careTeamId` |
| 12b | `POST /Goal` (sin evidencia de enfermedad) | `goalControlId` |
| 12c | `POST /Goal` (funcionalidad) | `goalQualityId` |
| 12d | `POST /CarePlan` | `carePlanId` |
| 12e | `POST /Consent` | `consentId` |

### 12f · El plan con sus metas y su equipo

```http
GET {{FHIRURL}}/CarePlan?subject=Patient/{{patientId}}&_include=CarePlan:goal&_include=CarePlan:care-team
```

Se pueden combinar **varios `_include`**. Verás el plan (`match`), el equipo
y las dos metas (`include`): todo el acuerdo del comité en una petición.

### 12g y 12h · Error a propósito: el consentimiento sin categoría

Envía ([`12e1_consentimiento_sin_categoria.json`](errores/12e1_consentimiento_sin_categoria.json))
un consentimiento sin `category`. **El servidor responde `201 Created`.** El
validador lo detecta:

```
Consent.category: minimum required = 1, but only found 0
```

Bórralo con `DELETE {{FHIRURL}}/Consent/{{errorConsentId}}`.

## Para pensar

El consentimiento firmado en papel sigue siendo el documento legal. ¿Cómo lo
vincularías a este recurso? *(Pista: `sourceAttachment`, con el PDF
escaneado, o `sourceReference` a un DocumentReference.)*

## Autoevaluación

<details><summary>1. ¿Qué diferencia hay entre un CarePlan con <code>intent: plan</code> y una ServiceRequest con <code>intent: order</code>?</summary>

El plan describe lo que se acordó hacer; la orden es el pedido concreto que
alguien debe cumplir. Del plan salen las órdenes, que pueden apuntar a él con
`basedOn`.
</details>

<details><summary>2. ¿Por qué Goal tiene dos estados?</summary>

`lifecycleStatus` dice en qué etapa está la meta (propuesta, activa,
completada); `achievementStatus`, si se está logrando (en curso, mejorando,
lograda, no lograda).
</details>

<details><summary>3. Luis decide no aceptar la quimioterapia. ¿Cómo se registra?</summary>

Con un Consent cuya `provision.type` sea `deny` para la quimioterapia, y
actualizando la actividad del plan a `cancelled`.
</details>

## Resumen

- **CareTeam** dice quiénes atienden al paciente y con qué rol.
- **Goal** define metas medibles con su plazo.
- **CarePlan** reúne el problema, las metas, el equipo y las actividades.
- **Consent** registra lo que el paciente permite o niega, según qué norma.

## Ejecutar este módulo

- **Postman:** carpeta *12 · Plan y consentimiento*.
- **curl:** `curl/taller.sh 12`
- **R:**

  ```r
  plan <- fhir_buscar("CarePlan?subject=Patient/{{patientId}}&_include=CarePlan:goal&_include=CarePlan:care-team")
  vapply(plan$entry, function(e) paste(e$resource$resourceType, e$search$mode), "")
  vapply(plan$entry[[1]]$resource$activity, function(a) a$detail$description, "")
  ```
