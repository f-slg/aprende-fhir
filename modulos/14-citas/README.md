# Módulo 14 · Citas

[← Módulo 13](../13-procedimientos/README.md) · [Inicio](../../README.md) · [Módulo 15 →](../15-medicamentos/README.md)

> **Nivel:** intermedio · **Duración:** 75 minutos · **Necesitas:** módulos 10 y 11

## Lo que vas a aprender

1. Cómo se modela una **agenda** en FHIR: Schedule, Slot y Appointment.
2. A **reservar** un cupo y confirmar la asistencia (AppointmentResponse).
3. El **ciclo de vida** de una cita: reservada, cumplida o cancelada.
4. Por qué un servidor puede devolver una búsqueda **desactualizada** (caché).

## La historia

Después de la cirugía (módulo 13), Luis empieza la quimioterapia en el
**Hospital de Día de Oncología**, que tiene una agenda de julio a
septiembre de 2025.

- El **20 de junio** se agenda el **ciclo 1** para el 2 de julio a las 09:00.
  El 30 de junio, Luis confirma por teléfono. El 2 de julio se cumple.
- Se agenda el **ciclo 2** para el 23 de julio. Pero el control de hemograma
  muestra **neutropenia** (pocos neutrófilos, un efecto de la
  quimioterapia), y la cita se **cancela** para reprogramarla.

> El prototipo [Agenda FHIR](https://github.com/f-slg/agenda-fhir-r) usa
> exactamente estos recursos en una aplicación de R y Shiny: verás el
> calendario que se construye con Schedule, Slot y Appointment.

---

## Cómo se modela una agenda

```
Schedule (la agenda del hospital de día, jul–sep)
   └── Slot (cupos: 2-jul 09:00–11:00, 23-jul 09:00–11:00, …)  free / busy
          └── Appointment (la cita de Luis en ese cupo)  booked → fulfilled / cancelled
                 └── AppointmentResponse (Luis confirma)
```

| Recurso | Responde a... |
|---|---|
| **Schedule** | ¿De quién es la agenda y para qué periodo? |
| **Slot** | ¿Qué cupos hay y si están libres u ocupados? |
| **Appointment** | ¿Quién viene, cuándo y a qué? |
| **AppointmentResponse** | ¿Qué respondió cada participante? |
| **Encounter** (módulo 05) | ¿Qué pasó realmente cuando vino? |

## Ficha del recurso: Schedule

**¿Qué es?** Un **contenedor de cupos**: la agenda de un profesional, de un
lugar, de un equipo (un ecógrafo) o de un servicio, para un periodo.

<!-- ficha Schedule -->
| Elemento | Card. | Tipo | Para qué sirve |
|---|---|---|---|
| `identifier` | 0..* | Identifier | Identificador de la agenda. |
| `active` ⚑ | 0..1 | boolean | Si está en uso. |
| `serviceCategory` | 0..* | CodeableConcept | Categoría de servicio. |
| `serviceType` | 0..* | CodeableConcept | Qué servicio se agenda. |
| `specialty` | 0..* | CodeableConcept | Especialidad. |
| `actor` | **1..*** | Reference(Patient \| Practitioner \| PractitionerRole \| RelatedPerson \| …) | **De quién** es la agenda: lugar, profesional, equipo. |
| `planningHorizon` | 0..1 | Period | El periodo que cubre. |
| `comment` | 0..1 | string | Comentarios. |
<!-- /ficha -->

## Ficha del recurso: Slot

**¿Qué es?** Un **intervalo de tiempo** de una agenda que puede reservarse.

<!-- ficha Slot -->
| Elemento | Card. | Tipo | Para qué sirve |
|---|---|---|---|
| `identifier` | 0..* | Identifier | Identificador del cupo. |
| `serviceType` | 0..* | CodeableConcept | Qué servicio se presta en el cupo. |
| `specialty` | 0..* | CodeableConcept | Especialidad. |
| `appointmentType` | 0..1 | CodeableConcept | Tipo de cita. |
| `schedule` | **1..1** | Reference(Schedule) | La agenda a la que pertenece. |
| `status` | **1..1** | code | `free`, `busy`, `busy-unavailable`, `busy-tentative` o `entered-in-error`. |
| `start` | **1..1** | instant | Inicio. |
| `end` | **1..1** | instant | Fin. |
| `overbooked` | 0..1 | boolean | Si se aceptó más de una cita en el cupo. |
| `comment` | 0..1 | string | Comentarios. |
<!-- /ficha -->

## Ficha del recurso: Appointment

**¿Qué es?** Una **cita**: el acuerdo de que ciertos participantes (paciente,
profesional, lugar) se reúnan en un momento para una atención.

**¿Para qué se usa?** Para agendar consultas, procedimientos, sesiones de
tratamiento. Cuando el paciente llega, la atención se registra como un
**Encounter**, que puede apuntar a la cita con `appointment`.

<!-- ficha Appointment -->
| Elemento | Card. | Tipo | Para qué sirve |
|---|---|---|---|
| `identifier` | 0..* | Identifier | Número de la cita. |
| `status` ⚑ | **1..1** | code | `proposed`, `pending`, `booked`, `arrived`, `fulfilled`, `cancelled`, `noshow`... |
| `cancelationReason` | 0..1 | CodeableConcept | Por qué se canceló. |
| `serviceType` | 0..* | CodeableConcept | Qué servicio. |
| `specialty` | 0..* | CodeableConcept | Especialidad. |
| `appointmentType` | 0..1 | CodeableConcept | Tipo de cita: primera vez, control, urgencia. |
| `reasonCode` | 0..* | CodeableConcept | Motivo, codificado. |
| `reasonReference` | 0..* | Reference(Condition \| Procedure \| Observation \| ImmunizationRecommendation) | Motivo, como referencia a una Condition. |
| `description` | 0..1 | string | Descripción breve. |
| `start` | 0..1 | instant | Inicio. |
| `end` | 0..1 | instant | Fin. |
| `slot` | 0..* | Reference(Slot) | Los cupos que ocupa. |
| `created` | 0..1 | dateTime | Cuándo se agendó. |
| `comment` | 0..1 | string | Comentarios. |
| `patientInstruction` | 0..1 | string | Indicaciones para el paciente (ayuno, documentos). |
| `basedOn` | 0..* | Reference(ServiceRequest) | La orden que la originó. |
| `participant` | **1..*** | BackboneElement | Los participantes. |
| `participant.actor` | 0..1 | Reference(Patient \| Practitioner \| PractitionerRole \| RelatedPerson \| …) | El paciente, el profesional, el lugar. |
| `participant.required` | 0..1 | code | Si su presencia es obligatoria. |
| `participant.status` | **1..1** | code | Si aceptó: `accepted`, `declined`, `tentative` o `needs-action`. |
<!-- /ficha -->

Una regla de Appointment (`app-3`): una cita que no está `proposed` ni
`cancelled` debe tener `start` y `end`. Una cita reservada sin hora no tiene
sentido.

## Ficha del recurso: AppointmentResponse

**¿Qué es?** La **respuesta** de un participante a una cita: la acepta, la
rechaza o propone otra hora.

<!-- ficha AppointmentResponse -->
| Elemento | Card. | Tipo | Para qué sirve |
|---|---|---|---|
| `appointment` | **1..1** | Reference(Appointment) | La cita. |
| `start` | 0..1 | instant | Una hora alternativa propuesta. |
| `end` | 0..1 | instant | Fin de la hora alternativa. |
| `actor` | 0..1 | Reference(Patient \| Practitioner \| PractitionerRole \| RelatedPerson \| …) | Quién responde. |
| `participantStatus` ⚑ | **1..1** | code | `accepted`, `declined`, `tentative` o `needs-action`. |
| `comment` | 0..1 | string | Comentario. |
<!-- /ficha -->

---

## El hospital de día

Es un Location como el consultorio del módulo 10. Lo que cambia:

<!-- diferencia 14a -->
```json
{
  "identifier": [
    {
      "system": "https://f-slg.github.io/aprende-fhir/sid/ubicacion",
      "value": "HGDE-HDO"
    }
  ],
  "name": "Hospital de Día de Oncología",
  "type": [
    {
      "coding": [
        {
          "system": "http://terminology.hl7.org/CodeSystem/v3-RoleCode",
          "code": "ONCL",
          "display": "Medical oncology clinic"
        }
      ],
      "text": "Hospital de día de oncología"
    }
  ],
  "physicalType": {
    "coding": [
      {
        "system": "http://terminology.hl7.org/CodeSystem/location-physical-type",
        "code": "wa",
        "display": "Ward"
      }
    ],
    "text": "Área"
  }
}
```
<!-- /diferencia -->

`ONCL` es una consulta de oncología y `wa` (*ward*), un área. Solución:
[`14a_location_hospital_dia.json`](soluciones/14a_location_hospital_dia.json).

## Paso a paso: la agenda

### Paso 1 · El mínimo: de quién es la agenda

<!-- paso 14b 1 -->
```json
{
  "resourceType": "Schedule",
  "actor": [
    {
      "reference": "Location/{{dayHospitalLocationId}}",
      "display": "Hospital de Día de Oncología"
    },
    {
      "reference": "PractitionerRole/{{oncologistRoleId}}",
      "display": "Dr. Ruiz · Oncología clínica"
    }
  ]
}
```
<!-- /paso -->

`actor` es lo único obligatorio: la agenda es del hospital de día **y** del
rol del oncólogo.

### Paso 2 · Qué servicio ofrece y en qué periodo

<!-- paso 14b 2 -->
```json
{
  "active": true,
  "serviceType": [
    {
      "text": "Quimioterapia ambulatoria"
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
  ],
  "planningHorizon": {
    "start": "2025-07-01T07:00:00-05:00",
    "end": "2025-09-30T19:00:00-05:00"
  }
}
```
<!-- /paso -->

### Paso 3 · Comentario, identificador y narrativa

<!-- paso 14b 3 -->
```json
{
  "comment": "Sillones de quimioterapia, de lunes a viernes de 07:00 a 19:00.",
  "identifier": [
    {
      "system": "https://f-slg.github.io/aprende-fhir/sid/agenda",
      "value": "AG-HDO-2025-3"
    }
  ],
  "text": {
    "status": "generated",
    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><p>Agenda de quimioterapia del Hospital de Día de Oncología, julio a septiembre de 2025.</p></div>"
  }
}
```
<!-- /paso -->

Solución: [`14b_schedule_quimioterapia.json`](soluciones/14b_schedule_quimioterapia.json).

## Paso a paso: el cupo

### Paso 1 · El mínimo: agenda, estado, inicio y fin

<!-- paso 14c 1 -->
```json
{
  "resourceType": "Slot",
  "schedule": {
    "reference": "Schedule/{{scheduleId}}",
    "display": "Agenda de quimioterapia"
  },
  "status": "free",
  "start": "2025-07-02T09:00:00-05:00",
  "end": "2025-07-02T11:00:00-05:00"
}
```
<!-- /paso -->

Un cupo **libre** (`free`) de dos horas.

### Paso 2 · Qué servicio y la narrativa

<!-- paso 14c 2 -->
```json
{
  "serviceType": [
    {
      "text": "Quimioterapia ambulatoria"
    }
  ],
  "text": {
    "status": "generated",
    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><p>Cupo libre: 2 de julio de 2025, 09:00 a 11:00.</p></div>"
  }
}
```
<!-- /paso -->

Solución: [`14c_slot_ciclo1.json`](soluciones/14c_slot_ciclo1.json).

## Paso a paso: la cita del ciclo 1

### Paso 1 · El mínimo: estado, participantes, inicio y fin

<!-- paso 14e 1 -->
```json
{
  "resourceType": "Appointment",
  "status": "booked",
  "participant": [
    {
      "actor": {
        "reference": "Patient/{{patientId}}",
        "display": "Luis Alberto Paredes Cevallos"
      },
      "required": "required",
      "status": "accepted"
    },
    {
      "actor": {
        "reference": "PractitionerRole/{{oncologistRoleId}}",
        "display": "Dr. Ruiz · Oncología clínica"
      },
      "required": "required",
      "status": "accepted"
    },
    {
      "actor": {
        "reference": "Location/{{dayHospitalLocationId}}",
        "display": "Hospital de Día de Oncología"
      },
      "required": "required",
      "status": "accepted"
    }
  ],
  "start": "2025-07-02T09:00:00-05:00",
  "end": "2025-07-02T11:00:00-05:00"
}
```
<!-- /paso -->

Tres participantes, todos `required` y `accepted`: el paciente, el rol del
oncólogo y el hospital de día. Por la regla `app-3`, una cita `booked` debe
tener `start` y `end` desde el inicio.

### Paso 2 · Qué cupo ocupa y cuándo se agendó

<!-- paso 14e 2 -->
```json
{
  "slot": [
    {
      "reference": "Slot/{{slot1Id}}",
      "display": "Cupo del ciclo 1"
    }
  ],
  "created": "2025-06-20T10:00:00-05:00"
}
```
<!-- /paso -->

### Paso 3 · Qué atención es y por qué

<!-- paso 14e 3 -->
```json
{
  "serviceType": [
    {
      "text": "Quimioterapia ambulatoria"
    }
  ],
  "appointmentType": {
    "coding": [
      {
        "system": "http://terminology.hl7.org/CodeSystem/v2-0276",
        "code": "FOLLOWUP",
        "display": "A follow up visit from a previous appointment"
      }
    ],
    "text": "Ciclo de tratamiento"
  },
  "reasonReference": [
    {
      "reference": "Condition/{{conditionCancerId}}",
      "display": "Carcinoma ductal infiltrante de mama izquierda"
    }
  ],
  "description": "Quimioterapia con doxorrubicina, ciclo 1 de 4",
  "identifier": [
    {
      "system": "https://f-slg.github.io/aprende-fhir/sid/cita",
      "value": "CITA-2025-QT1"
    }
  ],
  "text": {
    "status": "generated",
    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><p>Cita: quimioterapia ciclo 1 de 4, 2 de julio de 2025, 09:00.</p></div>"
  }
}
```
<!-- /paso -->

Solución: [`14e_appointment_ciclo1.json`](soluciones/14e_appointment_ciclo1.json).

**El cupo pasa a ocupado.** Reservar la cita **no** cambia el cupo
automáticamente: hay que actualizarlo con `PUT`. Lo que cambia:

<!-- diferencia 14d -->
```json
{
  "id": "{{slot1Id}}",
  "status": "busy"
}
```
<!-- /diferencia -->

## Paso a paso: la confirmación

### Paso 1 · El mínimo: la cita, quién responde y su respuesta

<!-- paso 14f 1 -->
```json
{
  "resourceType": "AppointmentResponse",
  "appointment": {
    "reference": "Appointment/{{appointment1Id}}",
    "display": "Quimioterapia ciclo 1"
  },
  "actor": {
    "reference": "Patient/{{patientId}}",
    "display": "Luis Alberto Paredes Cevallos"
  },
  "participantStatus": "accepted"
}
```
<!-- /paso -->

La regla `apr-1` exige decir quién responde (`actor`) o qué tipo de
participante es.

### Paso 2 · Un comentario y la narrativa

<!-- paso 14f 2 -->
```json
{
  "comment": "Confirmado por teléfono el 30 de junio de 2025.",
  "text": {
    "status": "generated",
    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><p>Luis confirma su asistencia a la cita del ciclo 1.</p></div>"
  }
}
```
<!-- /paso -->

Solución: [`14f_appointmentresponse_paciente.json`](soluciones/14f_appointmentresponse_paciente.json).

## El ciclo de vida de la cita

**Se cumple.** El 2 de julio Luis recibe el ciclo 1: la cita pasa a
`fulfilled`. Lo que cambia:

<!-- diferencia 14g -->
```json
{
  "id": "{{appointment1Id}}",
  "status": "fulfilled"
}
```
<!-- /diferencia -->

**Se cancela.** La cita del ciclo 2
([`14i`](soluciones/14i_appointment_ciclo2.json)) se cancela por neutropenia.
Lo que cambia:

<!-- diferencia 14j -->
```json
{
  "id": "{{appointment2Id}}",
  "status": "cancelled",
  "cancelationReason": {
    "text": "Neutropenia: el recuento de neutrófilos no permite administrar el ciclo"
  },
  "comment": "Se reprograma para el 30 de julio, con un nuevo control de hemograma."
}
```
<!-- /diferencia -->

`cancelationReason` con `text`, porque la lista de motivos de FHIR no tiene
uno clínico tan específico. La cita **no se borra**: queda como cancelada,
para saber qué pasó y medir, por ejemplo, cuántos ciclos se postergan por
toxicidad.

---

## Ejercicios en el servidor

| Paso | Petición | Guarda |
|---|---|---|
| 14a | `POST /Location` (hospital de día) | `dayHospitalLocationId` |
| 14b | `POST /Schedule` | `scheduleId` |
| 14c | `POST /Slot` (libre) | `slot1Id` |
| 14d | `GET /Slot?schedule=Schedule/{{scheduleId}}&status=free` | |
| 14e | `POST /Appointment` (ciclo 1) | `appointment1Id` |
| 14f | `PUT /Slot/{{slot1Id}}` (ocupado) | |
| 14g | `GET` cupos libres otra vez, sin caché (abajo) | |
| 14h | `POST /AppointmentResponse` | |
| 14i | `PUT /Appointment/{{appointment1Id}}` (cumplida) | |
| 14j | `POST /Slot` (ciclo 2, ocupado) | `slot2Id` |
| 14k | `POST /Appointment` (ciclo 2) | `appointment2Id` |
| 14l | `PUT /Appointment/{{appointment2Id}}` (cancelada) | |
| 14m | `GET /Appointment?patient=Patient/{{patientId}}&_sort=date` | |

### 14d y 14g · Los cupos libres, y la caché del servidor

En el paso 14d buscas los cupos libres: aparece el del 2 de julio. En 14e
reservas la cita y en 14f marcas el cupo como ocupado. Si repites
**exactamente** la misma búsqueda enseguida, HAPI puede devolver el cupo
**todavía como libre**.

No es un error del recurso: es la **caché de búsquedas** del servidor. Para
responder más rápido, HAPI reutiliza durante un minuto el resultado de una
búsqueda idéntica. Para pedir un resultado fresco se envía el encabezado
estándar de HTTP `Cache-Control: no-cache`:

```http
GET {{FHIRURL}}/Slot?schedule=Schedule/{{scheduleId}}&status=free
Cache-Control: no-cache
```

Ahora sí: **0 cupos libres**. Ten esto en cuenta en cualquier sistema que
consulte disponibilidad justo después de reservar.

### 14m · Las citas del paciente

Verás las dos: el 2 de julio `fulfilled` y el 23 de julio `cancelled`.

### 14n y 14o · Error a propósito: la cita sin participantes

Envía ([`14e1_cita_sin_participantes.json`](errores/14e1_cita_sin_participantes.json))
una cita con estado, hora y descripción, pero **sin `participant`**. **El
servidor responde `201 Created`.** El validador lo detecta:

```
Appointment.participant: minimum required = 1, but only found 0
```

Una cita sin participantes no dice quién viene. Bórrala con
`DELETE {{FHIRURL}}/Appointment/{{errorAppointmentId}}`.

## Para pensar

Para medir el **ausentismo** a las citas de quimioterapia, ¿qué búsqueda
harías? ¿Y para la **oportunidad** de la atención (días entre la derivación
del módulo 10 y la primera cita con oncología)? *(Pista: `status=noshow` y
los elementos `created` y `start`.)*

## Autoevaluación

<details><summary>1. ¿Qué diferencia hay entre un Slot y un Appointment?</summary>

El Slot es un intervalo disponible de una agenda; el Appointment es la cita
concreta de un paciente, que ocupa uno o más cupos.
</details>

<details><summary>2. Al reservar la cita, ¿cambia solo el estado del cupo?</summary>

No necesariamente. Muchos servidores no actualizan el Slot por su cuenta: el
sistema que agenda debe marcarlo como `busy`, como en el paso 14f.
</details>

<details><summary>3. ¿Appointment o Encounter para "Luis recibió el ciclo 1"?</summary>

Las dos cosas: la cita pasa a `fulfilled` y la atención se registra como un
Encounter (con la administración del medicamento del módulo 15).
</details>

## Resumen

- **Schedule** es la agenda; **Slot**, cada cupo; **Appointment**, la cita;
  **AppointmentResponse**, la respuesta de un participante.
- Una cita pasa de `booked` a `fulfilled`, `cancelled` o `noshow`; no se borra.
- El cupo se marca como ocupado por separado.
- Los servidores pueden reutilizar búsquedas recientes: usa
  `Cache-Control: no-cache` cuando necesites el dato fresco.

## Ejecutar este módulo

- **Postman:** carpeta *14 · Citas*.
- **curl:** `curl/taller.sh 14`
- **R:**

  ```r
  citas <- fhir_buscar("Appointment?patient=Patient/{{patientId}}&_sort=date")
  fhir_tabla(citas, list(
    fecha  = function(r) substr(r$start, 1, 16),
    que    = function(r) r$description,
    estado = function(r) r$status
  ))
  ```
