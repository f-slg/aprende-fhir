# Módulo 13 · Procedimientos

[← Módulo 11](../11-anatomia-patologica/README.md) · [Inicio](../../README.md) · [Módulo 15 →](../15-medicamentos/README.md)

> **Nivel:** intermedio · **Duración:** 40 minutos · **Necesitas:** módulo 11
>
> El módulo 12 (plan y consentimiento) está en preparación. Cuando esté
> listo, antes de la cirugía se registrará el plan del comité de tumores y el
> consentimiento informado.

## Lo que vas a aprender

1. Qué es **Procedure** y qué lo diferencia de una orden.
2. A enlazar un procedimiento con su **motivo** (`reasonReference`).
3. A completar el registro con el **resultado** y el **seguimiento**.

## La historia

El **10 de junio de 2025**, a las 08:00, se realiza una **mastectomía
parcial** de la mama izquierda. Al terminar se registra el procedimiento.
Después se agrega el resultado: exitoso, con márgenes quirúrgicos libres de
tumor, y el seguimiento: control de la herida en dos semanas y valoración por
oncología.

---

## Ficha del recurso: Procedure

**¿Qué es?** Algo que **se hizo** al paciente, o por el paciente: una
cirugía, una curación, la colocación de un catéter, una sesión de
fisioterapia, una consejería.

**¿Para qué se usa?** Para la historia quirúrgica y de intervenciones, y para
la estadística de producción (cirugías realizadas).

**¿Cuándo usar otro recurso?**

| Si es... | Usa |
|---|---|
| Algo que se **pide** hacer y aún no se hace | **ServiceRequest** (módulo 10) |
| Un medicamento administrado | **MedicationAdministration** (módulo 15) |
| Una vacuna aplicada | **Immunization** (módulo 08) |
| Una medición (la presión arterial) | **Observation** (módulo 06) |

**Elementos principales** (<https://hl7.org/fhir/R4/procedure.html>):

<!-- ficha Procedure -->
| Elemento | Card. | Tipo | Para qué sirve |
|---|---|---|---|
| `identifier` | 0..* | Identifier | Identificador del procedimiento. |
| `basedOn` | 0..* | Reference(CarePlan \| ServiceRequest) | La orden que lo pidió. |
| `partOf` | 0..* | Reference(Procedure \| Observation \| MedicationAdministration) | El procedimiento mayor del que forma parte. |
| `status` ⚑ | **1..1** | code | `preparation`, `in-progress`, `not-done`, `on-hold`, `stopped`, `completed`... |
| `statusReason` | 0..1 | CodeableConcept | Por qué no se hizo o se detuvo. |
| `category` | 0..1 | CodeableConcept | Clase: quirúrgico, diagnóstico, terapéutico. |
| `code` | 0..1 | CodeableConcept | **Qué** se hizo. |
| `subject` | **1..1** | Reference(Patient \| Group) | A quién. |
| `encounter` | 0..1 | Reference(Encounter) | En qué atención. |
| `performed[x]` | 0..1 | dateTime \| Period \| string \| Age \| … | Cuándo. |
| `recorder` | 0..1 | Reference(Patient \| RelatedPerson \| Practitioner \| PractitionerRole) | Quién lo registró. |
| `asserter` | 0..1 | Reference(Patient \| RelatedPerson \| Practitioner \| PractitionerRole) | Quién lo informa. |
| `performer` | 0..* | BackboneElement | Quiénes lo hicieron. |
| `performer.function` | 0..1 | CodeableConcept | Con qué rol: cirujano, anestesiólogo. |
| `performer.actor` | **1..1** | Reference(Practitioner \| PractitionerRole \| Organization \| Patient \| …) | La persona. |
| `performer.onBehalfOf` | 0..1 | Reference(Organization) | En nombre de qué organización. |
| `location` | 0..1 | Reference(Location) | Dónde: el quirófano. |
| `reasonCode` | 0..* | CodeableConcept | Por qué, codificado. |
| `reasonReference` | 0..* | Reference(Condition \| Observation \| Procedure \| DiagnosticReport \| …) | Por qué, como referencia a una Condition. |
| `bodySite` | 0..* | CodeableConcept | En qué parte del cuerpo. |
| `outcome` | 0..1 | CodeableConcept | El resultado. |
| `report` | 0..* | Reference(DiagnosticReport \| DocumentReference \| Composition) | Informes del procedimiento. |
| `complication` | 0..* | CodeableConcept | Complicaciones. |
| `followUp` | 0..* | CodeableConcept | Indicaciones de seguimiento. |
| `note` | 0..* | Annotation | Notas. |
<!-- /ficha -->

---

## Paso a paso: la cirugía

### Paso 1 · El mínimo: estado y paciente

<!-- paso 13a 1 -->
```json
{
  "resourceType": "Procedure",
  "status": "completed",
  "subject": {
    "reference": "Patient/{{patientId}}",
    "display": "Luis Alberto Paredes Cevallos"
  }
}
```
<!-- /paso -->

### Paso 2 · Qué se hizo y en qué parte del cuerpo

<!-- paso 13a 2 -->
```json
{
  "category": {
    "coding": [
      {
        "system": "http://snomed.info/sct",
        "code": "387713003",
        "display": "Surgical procedure"
      }
    ],
    "text": "Procedimiento quirúrgico"
  },
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
  "bodySite": [
    {
      "coding": [
        {
          "system": "http://snomed.info/sct",
          "code": "80248007",
          "display": "Left breast structure"
        }
      ],
      "text": "Mama izquierda"
    }
  ]
}
```
<!-- /paso -->

`category` SNOMED `387713003` *Surgical procedure* y `code` SNOMED `64368001`
*Partial mastectomy*.

### Paso 3 · Cuándo, quién y por qué

<!-- paso 13a 3 -->
```json
{
  "performedDateTime": "2025-06-10T08:00:00-05:00",
  "recorder": {
    "reference": "Practitioner/{{practitionerId}}",
    "display": "Dra. Andrea Lucía Salazar Moreno"
  },
  "performer": [
    {
      "actor": {
        "reference": "Practitioner/{{practitionerId}}",
        "display": "Dra. Andrea Lucía Salazar Moreno"
      },
      "onBehalfOf": {
        "reference": "Organization/{{hospitalId}}",
        "display": "Hospital General Docente Ejemplo"
      }
    }
  ],
  "reasonReference": [
    {
      "reference": "Condition/{{conditionCancerId}}",
      "display": "Carcinoma ductal infiltrante de mama izquierda"
    }
  ]
}
```
<!-- /paso -->

`performer.onBehalfOf`: la cirujana opera **en nombre del** hospital.
`reasonReference` apunta al diagnóstico de cáncer del módulo 11: la cirugía
tiene un motivo verificable.

### Paso 4 · Identificador y narrativa

<!-- paso 13a 4 -->
```json
{
  "identifier": [
    {
      "system": "https://f-slg.github.io/aprende-fhir/sid/procedimiento",
      "value": "PROC-2025-0001"
    }
  ],
  "text": {
    "status": "generated",
    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><p>Mastectomía parcial de mama izquierda, 10 de junio de 2025.</p></div>"
  }
}
```
<!-- /paso -->

Solución: [`13a_procedure_mastectomia.json`](soluciones/13a_procedure_mastectomia.json).

## El resultado y el seguimiento

Con `PUT` se agrega lo que se supo después. Lo que cambia:

<!-- diferencia 13b -->
```json
{
  "id": "{{procedureId}}",
  "outcome": {
    "coding": [
      {
        "system": "http://snomed.info/sct",
        "code": "385669000",
        "display": "Successful"
      }
    ],
    "text": "Exitoso"
  },
  "followUp": [
    {
      "text": "Control de herida quirúrgica en 2 semanas y valoración por oncología."
    }
  ],
  "note": [
    {
      "text": "Márgenes quirúrgicos libres de tumor."
    }
  ]
}
```
<!-- /diferencia -->

`outcome` SNOMED `385669000` *Successful*. Solución:
[`13b_procedure_actualizar.json`](soluciones/13b_procedure_actualizar.json).

---

## Ejercicios en el servidor

```http
POST {{FHIRURL}}/Procedure                       → procedureId
PUT  {{FHIRURL}}/Procedure/{{procedureId}}
```

### Reto · Los procedimientos por diagnóstico

Busca todos los procedimientos realizados por el cáncer de mama de Luis:

```http
GET {{FHIRURL}}/Procedure?subject=Patient/{{patientId}}&reason-reference=Condition/{{conditionCancerId}}
```

## Para pensar

En el caso, la cirujana es la misma médica de la consulta. En la realidad
operaría un equipo: cirujano, ayudante, anestesiólogo e instrumentista. ¿Cómo
lo registrarías? *(Pista: `performer` es una lista, y `performer.function`
dice el rol de cada uno.)*

## Autoevaluación

<details><summary>1. El cirujano pide una mastectomía para la próxima semana. ¿Procedure?</summary>

No: todavía no se hizo. Es una **ServiceRequest**. Cuando se realice, se
registra el Procedure, que puede apuntar a la orden con `basedOn`.
</details>

<details><summary>2. ¿Para qué sirve <code>reasonReference</code> si ya hay un <code>code</code>?</summary>

`code` dice **qué** se hizo; `reasonReference`, **por qué**, apuntando al
diagnóstico concreto del paciente. Permite responder "¿qué procedimientos se
hicieron por este cáncer?".
</details>

## Resumen

- **Procedure** registra algo que se hizo; una orden es una ServiceRequest.
- `reasonReference` enlaza el procedimiento con su diagnóstico.
- `outcome`, `followUp` y `complication` completan el registro.

## Ejecutar este módulo

- **Postman:** carpeta *13 · Procedimientos*.
- **curl:** `curl/taller.sh 13`
- **R:**

  ```r
  dir <- "modulos/13-procedimientos/soluciones/"
  fhir_crear("Procedure", paste0(dir, "13a_procedure_mastectomia.json"), guarda = "procedureId")
  fhir_actualizar("Procedure/{{procedureId}}", paste0(dir, "13b_procedure_actualizar.json"))$outcome$text
  ```
