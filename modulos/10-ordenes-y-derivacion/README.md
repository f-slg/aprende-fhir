# Módulo 10 · Órdenes y derivación

[← Módulo 09](../09-documentos-clinicos/README.md) · [Inicio](../../README.md) · [Módulo 11 →](../11-anatomia-patologica/README.md)

> **Nivel:** intermedio · **Duración:** 90 minutos · **Necesitas:** módulos 04, 05 y 07

## Lo que vas a aprender

1. A modelar **dónde** se atiende (Location) y **en qué rol** trabaja un
   profesional (PractitionerRole).
2. A **pedir** un estudio o un procedimiento con ServiceRequest.
3. A **derivar** a un paciente a otro servicio.
4. A cerrar el ciclo **orden → resultado** con `basedOn`.
5. A buscar "hacia atrás" con `_revinclude`.

## La historia

El **22 de abril de 2025**, Luis vuelve al consultorio 3 de medicina general:
se palpó un **nódulo en la mama izquierda**. La Dra. Salazar encuentra un
nódulo de unos 2 cm en el cuadrante superior externo y pide una
**ecografía** urgente.

El 25 de abril la ecografía muestra un nódulo sólido e irregular de 2,4 cm:
**BI-RADS 4**, sospechoso. El 28 de abril la médica pide una **biopsia** y
**deriva a Luis a Oncología Clínica**, con el **Dr. Esteban Patricio Ruiz
Montalvo**. En la derivación menciona el antecedente que registró en el
módulo 07: la madre de Luis tuvo cáncer de mama.

---

## Ficha del recurso: Location

**¿Qué es?** Un **lugar físico** donde se prestan servicios: un consultorio,
una sala, una cama, un quirófano, un vacunatorio, una ambulancia.

**¿Para qué se usa?** Para decir **dónde** ocurrió una atención
(`Encounter.location`), dónde trabaja un profesional
(`PractitionerRole.location`) o dónde se agenda una cita (`Schedule.actor`).

**¿Cuándo usar otro recurso?** La **institución** es una **Organization**
(módulo 04). Location es el sitio; Organization, quien lo administra.

<!-- ficha Location -->
| Elemento | Card. | Tipo | Para qué sirve |
|---|---|---|---|
| `identifier` | 0..* | Identifier | Código del lugar. |
| `status` ⚑ | 0..1 | code | `active`, `suspended` o `inactive`. |
| `name` | 0..1 | string | Nombre. |
| `description` | 0..1 | string | Descripción. |
| `mode` | 0..1 | code | `instance` (un lugar concreto) o `kind` (una clase de lugar, como "ambulancia"). |
| `type` | 0..* | CodeableConcept | Qué servicio se presta: consulta, emergencia, oncología. |
| `telecom` | 0..* | ContactPoint | Teléfono o extensión. |
| `address` | 0..1 | Address | Dirección. |
| `physicalType` | 0..1 | CodeableConcept | Qué es físicamente: edificio, piso, sala, cama. |
| `position` | 0..1 | BackboneElement | Coordenadas geográficas. |
| `managingOrganization` | 0..1 | Reference(Organization) | La organización responsable. |
| `partOf` | 0..1 | Reference(Location) | El lugar más grande del que forma parte (la sala dentro del piso). |
| `hoursOfOperation` | 0..* | BackboneElement | Horario de atención. |
<!-- /ficha -->

## Ficha del recurso: PractitionerRole

**¿Qué es?** El **rol** que cumple un profesional en una organización: qué
hace, con qué especialidad, dónde y en qué horario.

**¿Para qué se usa?** Practitioner es la persona (módulo 04);
PractitionerRole, **la persona en un puesto**. La Dra. Salazar puede ser
médica general en este hospital y docente en una universidad: un
Practitioner y dos PractitionerRole. Muchos recursos aceptan una referencia
a PractitionerRole en lugar de Practitioner, y es mejor usarla: dice no solo
quién, sino **con qué rol y para qué organización**.

<!-- ficha PractitionerRole -->
| Elemento | Card. | Tipo | Para qué sirve |
|---|---|---|---|
| `active` | 0..1 | boolean | Si el rol está vigente. |
| `period` | 0..1 | Period | Desde y hasta cuándo. |
| `practitioner` | 0..1 | Reference(Practitioner) | La persona. |
| `organization` | 0..1 | Reference(Organization) | La organización. |
| `code` | 0..* | CodeableConcept | El rol: médico, enfermera, investigador. |
| `specialty` | 0..* | CodeableConcept | La especialidad. |
| `location` | 0..* | Reference(Location) | Dónde atiende. |
| `healthcareService` | 0..* | Reference(HealthcareService) | Los servicios que presta. |
| `telecom` | 0..* | ContactPoint | Contacto en ese puesto. |
| `availableTime` | 0..* | BackboneElement | Horario disponible. |
| `notAvailable` | 0..* | BackboneElement | Periodos en que no está disponible (vacaciones). |
<!-- /ficha -->

## Ficha del recurso: ServiceRequest

**¿Qué es?** Una **orden o solicitud** de que se haga algo: un examen de
laboratorio, un estudio de imagen, un procedimiento, una interconsulta, una
derivación, una terapia.

**¿Para qué se usa?** Para el circuito de pedidos: quién pide qué, para
quién, con qué prioridad y por qué. Cuando el servicio se cumple, el
resultado (DiagnosticReport, Procedure, Specimen) apunta a la orden con
`basedOn` o `request`, y así se sabe **qué orden se cumplió**.

**¿Cuándo usar otro recurso?**

| Si se pide... | Usa |
|---|---|
| Un medicamento | **MedicationRequest** (módulo 15) |
| Una dieta | **NutritionOrder** |
| Un dispositivo (silla de ruedas, glucómetro) | **DeviceRequest** |
| Cualquier otro servicio | **ServiceRequest** |

<!-- ficha ServiceRequest -->
| Elemento | Card. | Tipo | Para qué sirve |
|---|---|---|---|
| `identifier` | 0..* | Identifier | Número de la orden. |
| `basedOn` | 0..* | Reference(CarePlan \| ServiceRequest \| MedicationRequest) | El plan u otra orden de la que deriva. |
| `replaces` | 0..* | Reference(ServiceRequest) | La orden a la que reemplaza. |
| `requisition` | 0..1 | Identifier | Identificador común de varias órdenes pedidas juntas. |
| `status` ⚑ | **1..1** | code | `draft`, `active`, `on-hold`, `revoked`, `completed`, `entered-in-error`. |
| `intent` ⚑ | **1..1** | code | `proposal`, `plan`, `order`, `original-order`... |
| `category` | 0..* | CodeableConcept | Clase: laboratorio, imagen, derivación, consejería. |
| `priority` | 0..1 | code | `routine`, `urgent`, `asap` o `stat`. |
| `doNotPerform` ⚑ | 0..1 | boolean | `true` si es una orden de **no** hacer algo. |
| `code` | 0..1 | CodeableConcept | **Qué** se pide. |
| `subject` | **1..1** | Reference(Patient \| Group \| Location \| Device) | Para quién. |
| `encounter` | 0..1 | Reference(Encounter) | En qué atención se pidió. |
| `occurrence[x]` | 0..1 | dateTime \| Period \| Timing | Cuándo debe hacerse. |
| `authoredOn` | 0..1 | dateTime | Cuándo se pidió. |
| `requester` | 0..1 | Reference(Practitioner \| PractitionerRole \| Organization \| Patient \| …) | Quién lo pide. |
| `performerType` | 0..1 | CodeableConcept | Qué tipo de profesional o servicio debe hacerlo. |
| `performer` | 0..* | Reference(Practitioner \| PractitionerRole \| Organization \| CareTeam \| …) | Quién concretamente debe hacerlo. |
| `reasonCode` | 0..* | CodeableConcept | Por qué, codificado. |
| `reasonReference` | 0..* | Reference(Condition \| Observation \| DiagnosticReport \| DocumentReference) | Por qué, como referencia a una Condition, Observation o informe. |
| `supportingInfo` | 0..* | Reference(Resource) | Información adicional para quien lo hará. |
| `specimen` | 0..* | Reference(Specimen) | Las muestras, si ya se tomaron. |
| `bodySite` | 0..* | CodeableConcept | En qué parte del cuerpo. |
| `note` | 0..* | Annotation | Notas para quien lo hará. |
<!-- /ficha -->

`doNotPerform` y `status` son **modificadores** (⚑): una orden con
`doNotPerform: true` dice exactamente lo contrario que la misma orden sin él.

**El ciclo de una orden:**

```
ServiceRequest (ecografía, active) ──▶ se hace el estudio ──▶ DiagnosticReport.basedOn ──▶ orden
                                                            └──▶ la orden pasa a completed
```

---

## Paso a paso: el consultorio

### Paso 1 · El mínimo: nombre y estado

<!-- paso 10a 1 -->
```json
{
  "resourceType": "Location",
  "name": "Consultorio 3 de Medicina General",
  "status": "active"
}
```
<!-- /paso -->

### Paso 2 · Qué clase de lugar es

<!-- paso 10a 2 -->
```json
{
  "mode": "instance",
  "type": [
    {
      "coding": [
        {
          "system": "http://terminology.hl7.org/CodeSystem/v3-RoleCode",
          "code": "FMC",
          "display": "Family Medicine clinic"
        }
      ],
      "text": "Consulta de medicina general"
    }
  ],
  "physicalType": {
    "coding": [
      {
        "system": "http://terminology.hl7.org/CodeSystem/location-physical-type",
        "code": "ro",
        "display": "Room"
      }
    ],
    "text": "Sala"
  }
}
```
<!-- /paso -->

`mode: instance`: es **este** consultorio, no "los consultorios" en general.
`type` usa la tabla `v3-RoleCode` (`FMC`, consulta de medicina familiar y
general) y `physicalType`, la tabla `location-physical-type` (`ro`, una
sala).

### Paso 3 · Dónde está y quién lo administra

<!-- paso 10a 3 -->
```json
{
  "address": {
    "line": [
      "Av. Principal Ejemplo S00-00"
    ],
    "city": "Quito",
    "state": "Pichincha",
    "country": "EC"
  },
  "managingOrganization": {
    "reference": "Organization/{{hospitalId}}",
    "display": "Hospital General Docente Ejemplo"
  },
  "identifier": [
    {
      "system": "https://f-slg.github.io/aprende-fhir/sid/ubicacion",
      "value": "HGDE-CONS-03"
    }
  ],
  "text": {
    "status": "generated",
    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><p>Consultorio 3 de Medicina General, planta baja del Hospital General Docente Ejemplo.</p></div>"
  }
}
```
<!-- /paso -->

Solución: [`10a_location_consultorio.json`](soluciones/10a_location_consultorio.json).

## Paso a paso: el rol de la Dra. Salazar

### Paso 1 · El mínimo: quién y dónde trabaja

<!-- paso 10b 1 -->
```json
{
  "resourceType": "PractitionerRole",
  "practitioner": {
    "reference": "Practitioner/{{practitionerId}}",
    "display": "Dra. Andrea Lucía Salazar Moreno"
  },
  "organization": {
    "reference": "Organization/{{hospitalId}}",
    "display": "Hospital General Docente Ejemplo"
  }
}
```
<!-- /paso -->

### Paso 2 · Qué rol y qué especialidad

<!-- paso 10b 2 -->
```json
{
  "code": [
    {
      "coding": [
        {
          "system": "http://terminology.hl7.org/CodeSystem/practitioner-role",
          "code": "doctor",
          "display": "Doctor"
        }
      ],
      "text": "Médica"
    }
  ],
  "specialty": [
    {
      "coding": [
        {
          "system": "http://snomed.info/sct",
          "code": "394814009",
          "display": "General practice (specialty)"
        }
      ],
      "text": "Medicina general"
    }
  ]
}
```
<!-- /paso -->

`code` dice el rol (`doctor`) y `specialty`, la especialidad con SNOMED CT
(`394814009`, *General practice*).

### Paso 3 · En qué consultorio y en qué horario

<!-- paso 10b 3 -->
```json
{
  "active": true,
  "location": [
    {
      "reference": "Location/{{officeLocationId}}",
      "display": "Consultorio 3 de Medicina General"
    }
  ],
  "availableTime": [
    {
      "daysOfWeek": [
        "mon",
        "tue",
        "wed",
        "thu",
        "fri"
      ],
      "availableStartTime": "07:00:00",
      "availableEndTime": "13:00:00"
    }
  ],
  "text": {
    "status": "generated",
    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><p>Dra. Andrea Lucía Salazar Moreno: médica general en el Hospital General Docente Ejemplo,</p><p>consultorio 3, de lunes a viernes de 07:00 a 13:00.</p></div>"
  }
}
```
<!-- /paso -->

`availableTime`: de lunes a viernes (`daysOfWeek`) de 07:00 a 13:00. Solución:
[`10b_practitionerrole_medica_general.json`](soluciones/10b_practitionerrole_medica_general.json).

**El oncólogo.** Se crea su Practitioner
([`10c`](soluciones/10c_practitioner_oncologo.json)), igual que el de la
médica en el módulo 04, y su rol. Lo que cambia respecto del rol de la Dra.
Salazar:

<!-- diferencia 10d -->
```json
{
  "practitioner": {
    "reference": "Practitioner/{{oncologistId}}",
    "display": "Dr. Esteban Patricio Ruiz Montalvo"
  },
  "code": [
    {
      "coding": [
        {
          "system": "http://terminology.hl7.org/CodeSystem/practitioner-role",
          "code": "doctor",
          "display": "Doctor"
        }
      ],
      "text": "Médico"
    }
  ],
  "specialty": [
    {
      "coding": [
        {
          "system": "http://snomed.info/sct",
          "code": "394593009",
          "display": "Medical oncology"
        }
      ],
      "text": "Oncología clínica"
    }
  ]
}
```
<!-- /diferencia -->

## La consulta por el nódulo

Es un Encounter como el del módulo 05. Lo que cambia:

<!-- diferencia 10e -->
```json
{
  "identifier": [
    {
      "system": "https://f-slg.github.io/aprende-fhir/sid/encuentro",
      "value": "ENC-2025-0003"
    }
  ],
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
        "reference": "PractitionerRole/{{salazarRoleId}}",
        "display": "Dra. Salazar · Medicina general"
      }
    }
  ],
  "period": {
    "start": "2025-04-22T08:00:00-05:00",
    "end": "2025-04-22T08:30:00-05:00"
  },
  "reasonCode": [
    {
      "coding": [
        {
          "system": "http://snomed.info/sct",
          "code": "89164003",
          "display": "Breast lump"
        }
      ],
      "text": "Nódulo en la mama izquierda"
    }
  ],
  "location": [
    {
      "location": {
        "reference": "Location/{{officeLocationId}}",
        "display": "Consultorio 3 de Medicina General"
      }
    }
  ]
}
```
<!-- /diferencia -->

Dos novedades: `participant.individual` apunta al **rol** de la médica, no a
la persona, y `location` dice en qué consultorio fue. Solución:
[`10e_encounter_consulta_nodulo.json`](soluciones/10e_encounter_consulta_nodulo.json).

## Paso a paso: la orden de ecografía

### Paso 1 · El mínimo: estado, intención y paciente

<!-- paso 10f 1 -->
```json
{
  "resourceType": "ServiceRequest",
  "status": "completed",
  "intent": "order",
  "subject": {
    "reference": "Patient/{{patientId}}",
    "display": "Luis Alberto Paredes Cevallos"
  }
}
```
<!-- /paso -->

`status`, `intent` y `subject` son obligatorios. `intent: order` dice que es
una orden firme. La creamos directamente como `completed` porque en el taller
el estudio ya se hizo; en un sistema real nacería `active` y pasaría a
`completed` al cumplirse.

### Paso 2 · Qué se pide, con qué prioridad y de qué parte del cuerpo

<!-- paso 10f 2 -->
```json
{
  "category": [
    {
      "coding": [
        {
          "system": "http://snomed.info/sct",
          "code": "363679005",
          "display": "Imaging"
        }
      ],
      "text": "Imagenología"
    }
  ],
  "code": {
    "coding": [
      {
        "system": "http://snomed.info/sct",
        "code": "47079000",
        "display": "Ultrasonography of breast"
      }
    ],
    "text": "Ecografía de mama"
  },
  "priority": "urgent",
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

`code` con SNOMED CT (`47079000`, *Ultrasonography of breast*) y `priority`
es un **code** con cuatro valores posibles: `routine`, `urgent`, `asap` y
`stat`.

### Paso 3 · Quién lo pide, cuándo, en qué consulta y por qué

<!-- paso 10f 3 -->
```json
{
  "encounter": {
    "reference": "Encounter/{{noduleEncounterId}}",
    "display": "Consulta por nódulo mamario, 22 de abril de 2025"
  },
  "authoredOn": "2025-04-22T08:20:00-05:00",
  "requester": {
    "reference": "PractitionerRole/{{salazarRoleId}}",
    "display": "Dra. Salazar · Medicina general"
  },
  "reasonCode": [
    {
      "coding": [
        {
          "system": "http://snomed.info/sct",
          "code": "89164003",
          "display": "Breast lump"
        }
      ],
      "text": "Nódulo palpable en la mama izquierda"
    }
  ]
}
```
<!-- /paso -->

### Paso 4 · Identificador y narrativa

<!-- paso 10f 4 -->
```json
{
  "identifier": [
    {
      "system": "https://f-slg.github.io/aprende-fhir/sid/orden",
      "value": "ORD-2025-0101"
    }
  ],
  "text": {
    "status": "generated",
    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><p>Orden: ecografía de mama izquierda, prioridad urgente.</p><p>Motivo: nódulo palpable de 2 cm en el cuadrante superior externo.</p></div>"
  }
}
```
<!-- /paso -->

Solución: [`10f_servicerequest_ecografia.json`](soluciones/10f_servicerequest_ecografia.json).

## Paso a paso: el informe de la ecografía

Es un DiagnosticReport, como el de patología del módulo 11 (su ficha está
allí). Lo nuevo es `basedOn`: **cierra el ciclo** con la orden.

### Paso 1 · El mínimo: estado y código

<!-- paso 10g 1 -->
```json
{
  "resourceType": "DiagnosticReport",
  "status": "final",
  "code": {
    "coding": [
      {
        "system": "http://loinc.org",
        "code": "24601-7",
        "display": "US Breast"
      }
    ],
    "text": "Ecografía de mama"
  }
}
```
<!-- /paso -->

LOINC `24601-7`, *US Breast*.

### Paso 2 · De quién, cuándo y quién informa

<!-- paso 10g 2 -->
```json
{
  "category": [
    {
      "coding": [
        {
          "system": "http://terminology.hl7.org/CodeSystem/v2-0074",
          "code": "RAD",
          "display": "Radiology"
        }
      ],
      "text": "Imagenología"
    }
  ],
  "subject": {
    "reference": "Patient/{{patientId}}",
    "display": "Luis Alberto Paredes Cevallos"
  },
  "effectiveDateTime": "2025-04-25T10:00:00-05:00",
  "issued": "2025-04-25T12:00:00-05:00",
  "performer": [
    {
      "reference": "Organization/{{hospitalId}}",
      "display": "Hospital General Docente Ejemplo"
    }
  ]
}
```
<!-- /paso -->

`category` con `RAD` (*Radiology*) de la tabla `v2-0074`.

### Paso 3 · A qué orden responde

<!-- paso 10g 3 -->
```json
{
  "basedOn": [
    {
      "reference": "ServiceRequest/{{ultrasoundRequestId}}",
      "display": "Orden de ecografía de mama"
    }
  ]
}
```
<!-- /paso -->

### Paso 4 · La conclusión: BI-RADS 4

<!-- paso 10g 4 -->
```json
{
  "conclusion": "Nódulo sólido de bordes irregulares de 2,4 cm en el cuadrante superior externo de la mama izquierda. BI-RADS 4: sospechoso. Se recomienda biopsia.",
  "conclusionCode": [
    {
      "coding": [
        {
          "system": "http://snomed.info/sct",
          "code": "89164003",
          "display": "Breast lump"
        }
      ],
      "text": "Nódulo mamario sospechoso"
    }
  ],
  "identifier": [
    {
      "system": "https://f-slg.github.io/aprende-fhir/sid/informe",
      "value": "INF-IMG-2025-0212"
    }
  ],
  "text": {
    "status": "generated",
    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><p>Ecografía de mama izquierda (25 de abril de 2025): nódulo sólido, irregular, de 2,4 cm, BI-RADS 4.</p><p>Se recomienda biopsia.</p></div>"
  }
}
```
<!-- /paso -->

**BI-RADS** es la clasificación de los estudios de mama: 4 significa
"sospechoso", con indicación de biopsia. Solución:
[`10g_diagnosticreport_ecografia.json`](soluciones/10g_diagnosticreport_ecografia.json).

## La orden de biopsia y la derivación

Las dos se construyen como la orden de ecografía. Lo que cambia en la
**biopsia** ([`10h`](soluciones/10h_servicerequest_biopsia.json)):

<!-- diferencia 10h -->
```json
{
  "identifier": [
    {
      "system": "https://f-slg.github.io/aprende-fhir/sid/orden",
      "value": "ORD-2025-0102"
    }
  ],
  "category": [
    {
      "coding": [
        {
          "system": "http://snomed.info/sct",
          "code": "108252007",
          "display": "Laboratory procedure"
        }
      ],
      "text": "Procedimiento de laboratorio"
    }
  ],
  "code": {
    "coding": [
      {
        "system": "http://snomed.info/sct",
        "code": "122548005",
        "display": "Biopsy of breast"
      }
    ],
    "text": "Biopsia de mama"
  },
  "authoredOn": "2025-04-28T09:00:00-05:00",
  "reasonReference": [
    {
      "reference": "DiagnosticReport/{{ultrasoundReportId}}",
      "display": "Ecografía BI-RADS 4"
    }
  ]
}
```
<!-- /diferencia -->

Su motivo (`reasonReference`) es el informe de la ecografía: el BI-RADS 4
justifica la biopsia. En el módulo 11, la muestra (`Specimen.request`) y el
informe de patología (`DiagnosticReport.basedOn`) apuntarán a esta orden.

Lo que cambia en la **derivación** ([`10i`](soluciones/10i_servicerequest_derivacion.json)):

<!-- diferencia 10i -->
```json
{
  "identifier": [
    {
      "system": "https://f-slg.github.io/aprende-fhir/sid/orden",
      "value": "ORD-2025-0103"
    }
  ],
  "status": "active",
  "category": [
    {
      "coding": [
        {
          "system": "http://snomed.info/sct",
          "code": "3457005",
          "display": "Patient referral"
        }
      ],
      "text": "Derivación"
    }
  ],
  "code": {
    "coding": [
      {
        "system": "http://snomed.info/sct",
        "code": "3457005",
        "display": "Patient referral"
      }
    ],
    "text": "Derivación a Oncología Clínica"
  },
  "authoredOn": "2025-04-28T09:05:00-05:00",
  "performerType": {
    "coding": [
      {
        "system": "http://snomed.info/sct",
        "code": "394593009",
        "display": "Medical oncology"
      }
    ],
    "text": "Oncología clínica"
  },
  "performer": [
    {
      "reference": "PractitionerRole/{{oncologistRoleId}}",
      "display": "Dr. Ruiz · Oncología clínica"
    }
  ],
  "reasonReference": [
    {
      "reference": "DiagnosticReport/{{ultrasoundReportId}}",
      "display": "Ecografía BI-RADS 4"
    }
  ],
  "supportingInfo": [
    {
      "reference": "FamilyMemberHistory/{{motherHistoryId}}",
      "display": "Madre con cáncer de mama a los 52 años"
    }
  ],
  "note": [
    {
      "text": "Paciente varón de 46 años con nódulo sospechoso y madre con cáncer de mama. Se solicita valoración prioritaria."
    }
  ]
}
```
<!-- /diferencia -->

- `category` y `code` SNOMED `3457005`, *Patient referral*.
- `performerType` dice **a qué servicio** se deriva (oncología clínica) y
  `performer`, **a quién** concretamente: al rol del Dr. Ruiz.
- `supportingInfo` apunta al antecedente familiar del módulo 07: el oncólogo
  lo verá sin buscarlo.
- `status: active`: la derivación sigue abierta hasta que el oncólogo
  atienda a Luis.

---

## Ejercicios en el servidor

| Paso | Petición | Guarda |
|---|---|---|
| 10a | `POST /Location` | `officeLocationId` |
| 10b | `POST /PractitionerRole` (médica general) | `salazarRoleId` |
| 10c | `POST /Practitioner` (oncólogo) | `oncologistId` |
| 10d | `POST /PractitionerRole` (oncólogo) | `oncologistRoleId` |
| 10e | `POST /Encounter` | `noduleEncounterId` |
| 10f | `POST /ServiceRequest` (ecografía) | `ultrasoundRequestId` |
| 10g | `POST /DiagnosticReport` (ecografía) | `ultrasoundReportId` |
| 10h | `POST /ServiceRequest` (biopsia) | `biopsyRequestId` |
| 10i | `POST /ServiceRequest` (derivación) | `referralId` |

### 10j · Las órdenes del paciente

```http
GET {{FHIRURL}}/ServiceRequest?subject=Patient/{{patientId}}&_sort=authored
```

Devuelve las tres órdenes en orden cronológico: ecografía, biopsia y
derivación.

### 10k · ¿Qué se hizo con cada orden? `_revinclude`

```http
GET {{FHIRURL}}/ServiceRequest?subject=Patient/{{patientId}}&_revinclude=DiagnosticReport:based-on
```

`_include` (módulo 05) trae los recursos **a los que apuntan** los
resultados. `_revinclude` hace lo contrario: trae los recursos **que apuntan
a** los resultados. Aquí, los informes cuyo `basedOn` es alguna de las
órdenes. Verás las tres órdenes (`search.mode: match`) y dos informes
(`include`): el de la ecografía y, cuando hagas el módulo 11, el de
patología. La derivación no tiene informe: todavía está abierta.

### 10l · Los oncólogos del hospital

```http
GET {{FHIRURL}}/PractitionerRole?specialty=http://snomed.info/sct|394593009&_include=PractitionerRole:practitioner
```

Busca roles por especialidad e incluye a la persona de cada rol. Es la
búsqueda que haría un sistema para elegir a quién derivar.

### 10m · Error a propósito: la prioridad en español

Envía ([`10e1_prioridad_en_espanol.json`](errores/10e1_prioridad_en_espanol.json))
una orden con `"priority": "urgente"`. El servidor responde **`400`**:

```
HAPI-1821: [element="priority"] Invalid attribute value "urgente": Unknown ServiceRequestPriority code 'urgente'
```

## Para pensar

Una derivación en papel suele perderse: no se sabe si el paciente llegó, ni
qué dijo el especialista. Con FHIR, la derivación es un recurso con estado.
¿Qué búsqueda usarías para listar las derivaciones a oncología que llevan más
de 15 días en estado `active`? *(Pista: combina `status`, `performer` o
`category`, y `authored` con el prefijo `lt`, "menor que".)*

## Autoevaluación

<details><summary>1. ¿Practitioner o PractitionerRole en <code>ServiceRequest.requester</code>?</summary>

Mejor **PractitionerRole**: dice quién pide la orden, con qué rol y en qué
organización. Los dos están permitidos.
</details>

<details><summary>2. ¿Cómo sabe el sistema que el informe de la ecografía cumple esa orden?</summary>

Porque el DiagnosticReport tiene `basedOn` apuntando a la ServiceRequest. Con
`_revinclude=DiagnosticReport:based-on` se recupera desde la orden.
</details>

<details><summary>3. ¿Qué diferencia hay entre <code>performerType</code> y <code>performer</code>?</summary>

`performerType` dice qué **tipo** de profesional o servicio debe atender
(oncología clínica); `performer`, **quién** concretamente (el rol del Dr.
Ruiz). Se puede indicar solo el tipo y dejar que el servicio asigne a la
persona.
</details>

## Resumen

- **Location** es el lugar; **PractitionerRole**, el profesional en un puesto.
- **ServiceRequest** pide un servicio: estudio, procedimiento o derivación.
- Los resultados apuntan a la orden con `basedOn` (o `request` en Specimen).
- `_revinclude` trae los recursos que apuntan a los resultados de la búsqueda.

## Ejecutar este módulo

- **Postman:** carpeta *10 · Órdenes y derivación*.
- **curl:** `curl/taller.sh 10`
- **R:**

  ```r
  ordenes <- fhir_buscar("ServiceRequest?subject=Patient/{{patientId}}&_revinclude=DiagnosticReport:based-on")
  fhir_tabla(ordenes, list(
    tipo   = function(r) r$resourceType,
    que    = function(r) r$code$text,
    estado = function(r) r$status
  ))
  ```
