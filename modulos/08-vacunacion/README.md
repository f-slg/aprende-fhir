# Módulo 08 · Vacunación

[← Módulo 07](../07-antecedentes/README.md) · [Inicio](../../README.md) · [Módulo 09 →](../09-documentos-clinicos/README.md)

> **Nivel:** intermedio · **Duración:** 60 minutos · **Necesitas:** módulos 04 y 05

## Lo que vas a aprender

1. Qué es el recurso **Immunization** y qué datos de una vacunación registra.
2. A registrar una vacuna **no aplicada** y su motivo (`not-done`).
3. A codificar las vacunas con **CVX** y la dosis del esquema con
   `protocolApplied`.
4. A obtener el **carné de vacunación** de un paciente con una búsqueda.

## La historia

En la consulta del 20 de marzo, la Dra. Salazar revisa el esquema de
vacunación de Luis: le falta la **vacuna contra la influenza** de la campaña
de este año y el **refuerzo de Td** (tétanos y difteria), que en adultos se
aplica cada 10 años. Pero Luis tiene **38,4 °C**: una enfermedad aguda con
fiebre es motivo para **diferir** la vacunación. La médica registra que no se
vacunó y por qué, y le indica volver cuando esté bien.

El **3 de abril de 2025**, ya recuperado, Luis va al vacunatorio. La
**Lcda. Rosa Elena Quishpe Tenesaca** le aplica las dos vacunas.

---

## Ficha del recurso: Immunization

**¿Qué es?** El registro de **una dosis de vacuna**: aplicada, o que se
decidió no aplicar. Cada dosis es un Immunization.

**¿Para qué se usa?** Para el **carné de vacunación** del paciente, para
calcular **coberturas** de los programas de inmunización y para la vigilancia
de **eventos supuestamente atribuibles a la vacunación** (ESAVI).

**¿Cuándo usar otro recurso?**

- La **recomendación** de qué vacunas le tocan: **ImmunizationRecommendation**.
- La **evaluación** de si una dosis cuenta para el esquema:
  **ImmunizationEvaluation**.
- Una **orden** de vacunar que todavía no se cumple: **MedicationRequest** o
  **ServiceRequest**.

**Elementos principales** (<https://hl7.org/fhir/R4/immunization.html>):

<!-- ficha Immunization -->
| Elemento | Card. | Tipo | Para qué sirve |
|---|---|---|---|
| `identifier` | 0..* | Identifier | Identificador del registro. |
| `status` ⚑ | **1..1** | code | `completed`, `entered-in-error` o `not-done`. |
| `statusReason` | 0..1 | CodeableConcept | Por qué **no** se aplicó. |
| `vaccineCode` | **1..1** | CodeableConcept | Qué vacuna: un código CVX, SNOMED CT o del catálogo nacional. |
| `patient` | **1..1** | Reference(Patient) | A quién. |
| `encounter` | 0..1 | Reference(Encounter) | En qué atención. |
| `occurrence[x]` | **1..1** | dateTime \| string | Cuándo se aplicó (o cuándo se decidió no aplicarla). |
| `recorded` | 0..1 | dateTime | Cuándo se registró. |
| `primarySource` | 0..1 | boolean | `true` si lo registra quien vacunó; `false` si viene de un carné u otro registro. |
| `location` | 0..1 | Reference(Location) | Dónde se vacunó. |
| `manufacturer` | 0..1 | Reference(Organization) | Fabricante. |
| `lotNumber` | 0..1 | string | Número de lote: clave para rastrear un ESAVI. |
| `expirationDate` | 0..1 | date | Fecha de vencimiento del lote. |
| `site` | 0..1 | CodeableConcept | Sitio de aplicación: brazo izquierdo, muslo derecho... |
| `route` | 0..1 | CodeableConcept | Vía: intramuscular, subcutánea, oral, intradérmica. |
| `doseQuantity` | 0..1 | Quantity | Cantidad aplicada: 0,5 mL. |
| `performer` | 0..* | BackboneElement | Quién vacunó. |
| `note` | 0..* | Annotation | Notas. |
| `reasonCode` | 0..* | CodeableConcept | Por qué se vacunó. |
| `isSubpotent` ⚑ | 0..1 | boolean | Si la dosis no cuenta (se aplicó mal, cadena de frío rota). |
| `reaction` | 0..* | BackboneElement | Reacciones posteriores. |
| `protocolApplied` | 0..* | BackboneElement | Qué dosis del esquema es. |
| `protocolApplied.series` | 0..1 | string | El esquema o la campaña. |
| `protocolApplied.targetDisease` | 0..* | CodeableConcept | Contra qué enfermedad. |
| `protocolApplied.doseNumber[x]` | **1..1** | positiveInt \| string | Número de dosis. |
| `protocolApplied.seriesDoses[x]` | 0..1 | positiveInt \| string | Cuántas dosis tiene el esquema. |
<!-- /ficha -->

**CVX** es la terminología de vacunas de los CDC de Estados Unidos, la más
usada en FHIR (`http://hl7.org/fhir/sid/cvx`). Cada país puede usar además
su propio catálogo de vacunas.

---

## Paso a paso: la vacuna diferida

### Paso 1 · El mínimo: estado, vacuna, paciente y fecha

<!-- paso 08a 1 -->
```json
{
  "resourceType": "Immunization",
  "status": "not-done",
  "vaccineCode": {
    "coding": [
      {
        "system": "http://hl7.org/fhir/sid/cvx",
        "code": "141",
        "display": "Influenza, split virus, trivalent, preservative"
      }
    ],
    "text": "Influenza estacional"
  },
  "patient": {
    "reference": "Patient/{{patientId}}",
    "display": "Luis Alberto Paredes Cevallos"
  },
  "occurrenceDateTime": "2025-03-20T08:00:00-05:00"
}
```
<!-- /paso -->

`occurrence[x]` es **obligatorio**, aunque la vacuna no se aplique: es la
fecha en que se decidió no aplicarla. `status: not-done` es un **modificador**
(⚑): un sistema que lo ignore contaría esta vacuna como aplicada.

### Paso 2 · Por qué no se aplicó

<!-- paso 08a 2 -->
```json
{
  "statusReason": {
    "coding": [
      {
        "system": "http://terminology.hl7.org/CodeSystem/v3-ActReason",
        "code": "MEDPREC",
        "display": "medical precaution"
      }
    ],
    "text": "Precaución médica: enfermedad aguda con fiebre"
  },
  "note": [
    {
      "text": "Se indica volver al vacunatorio cuando esté sin fiebre."
    }
  ]
}
```
<!-- /paso -->

`statusReason` usa la tabla `v3-ActReason`: `MEDPREC` es *medical
precaution*, precaución médica por la fiebre. Otros motivos posibles son
`PATOBJ` (el paciente se niega) o `IMMUNE` (ya es inmune).

### Paso 3 · En qué consulta y quién lo informa

<!-- paso 08a 3 -->
```json
{
  "encounter": {
    "reference": "Encounter/{{encounterId}}",
    "display": "Consulta por dolor abdominal"
  },
  "recorded": "2025-03-20",
  "primarySource": true,
  "text": {
    "status": "generated",
    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><p>Vacuna contra la influenza NO aplicada el 20 de marzo de 2025: se difiere por fiebre (38,4 °C).</p></div>"
  }
}
```
<!-- /paso -->

Solución: [`08a_immunization_diferida.json`](soluciones/08a_immunization_diferida.json).

## La enfermera y la atención en el vacunatorio

Antes de registrar las vacunas, crea a la enfermera
([`08b_practitioner_enfermera.json`](soluciones/08b_practitioner_enfermera.json))
y la atención del 3 de abril
([`08c_encounter_vacunacion.json`](soluciones/08c_encounter_vacunacion.json)).
Ya sabes construirlos (módulos 04 y 05). Fíjate en dos detalles:

- Cada visita es **un Encounter nuevo**: la consulta del 20 de marzo y la
  vacunación del 3 de abril son dos atenciones distintas.
- En la enfermera, `qualification.code` solo tiene `text`: cuando no hay un
  código adecuado, un texto es mejor que un código equivocado.

## Paso a paso: la vacuna contra la influenza

### Paso 1 · El mínimo: estado, vacuna, paciente y fecha

<!-- paso 08d 1 -->
```json
{
  "resourceType": "Immunization",
  "status": "completed",
  "vaccineCode": {
    "coding": [
      {
        "system": "http://hl7.org/fhir/sid/cvx",
        "code": "141",
        "display": "Influenza, split virus, trivalent, preservative"
      }
    ],
    "text": "Influenza estacional"
  },
  "patient": {
    "reference": "Patient/{{patientId}}",
    "display": "Luis Alberto Paredes Cevallos"
  },
  "occurrenceDateTime": "2025-04-03T10:10:00-05:00"
}
```
<!-- /paso -->

CVX `141` es la vacuna inyectable de influenza estacional. El `display` debe
ser el nombre oficial de CVX, en inglés.

### Paso 2 · Dónde y quién la registra

<!-- paso 08d 2 -->
```json
{
  "encounter": {
    "reference": "Encounter/{{vaccinationEncounterId}}",
    "display": "Vacunatorio, 3 de abril de 2025"
  },
  "recorded": "2025-04-03",
  "primarySource": true
}
```
<!-- /paso -->

`primarySource: true`: la registra quien la aplicó. Si la vacuna se
transcribiera de un carné de papel, sería `false`.

### Paso 3 · El producto: lote y vencimiento

<!-- paso 08d 3 -->
```json
{
  "lotNumber": "FLU-25-0417",
  "expirationDate": "2025-12-31"
}
```
<!-- /paso -->

Si hubiera un ESAVI, el **lote** permite saber qué otras personas recibieron
el mismo producto.

### Paso 4 · Cómo se aplicó: sitio, vía y dosis

<!-- paso 08d 4 -->
```json
{
  "site": {
    "coding": [
      {
        "system": "http://snomed.info/sct",
        "code": "368208006",
        "display": "Left upper arm structure"
      }
    ],
    "text": "Brazo izquierdo"
  },
  "route": {
    "coding": [
      {
        "system": "http://terminology.hl7.org/CodeSystem/v3-RouteOfAdministration",
        "code": "IM",
        "display": "Injection, intramuscular"
      }
    ],
    "text": "Intramuscular"
  },
  "doseQuantity": {
    "value": 0.5,
    "unit": "mL",
    "system": "http://unitsofmeasure.org",
    "code": "mL"
  }
}
```
<!-- /paso -->

El sitio con SNOMED CT (`368208006` *Left upper arm structure*), la vía con la
tabla `v3-RouteOfAdministration` (`IM`, intramuscular) y la dosis con UCUM
(`mL`).

### Paso 5 · Quién vacunó y qué dosis del esquema es

<!-- paso 08d 5 -->
```json
{
  "performer": [
    {
      "function": {
        "coding": [
          {
            "system": "http://terminology.hl7.org/CodeSystem/v2-0443",
            "code": "AP",
            "display": "Administering Provider"
          }
        ],
        "text": "Vacunadora"
      },
      "actor": {
        "reference": "Practitioner/{{nursePractitionerId}}",
        "display": "Lcda. Rosa Elena Quishpe Tenesaca"
      }
    }
  ],
  "protocolApplied": [
    {
      "series": "Campaña de influenza 2025",
      "targetDisease": [
        {
          "coding": [
            {
              "system": "http://snomed.info/sct",
              "code": "6142004",
              "display": "Influenza"
            }
          ],
          "text": "Influenza"
        }
      ],
      "doseNumberPositiveInt": 1
    }
  ],
  "text": {
    "status": "generated",
    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><p>Vacuna contra la influenza estacional, 0,5 mL IM en el brazo izquierdo, lote FLU-25-0417.</p></div>"
  }
}
```
<!-- /paso -->

`performer.function` con `AP` (*Administering Provider*) indica que la
enfermera es quien la aplicó. `protocolApplied` dice que es la dosis 1 de la
campaña 2025, contra la influenza. Solución:
[`08d_immunization_influenza.json`](soluciones/08d_immunization_influenza.json).

## El refuerzo de Td: otra vacuna, otro esquema

Lo que cambia en la vacuna Td:

<!-- diferencia 08e -->
```json
{
  "vaccineCode": {
    "coding": [
      {
        "system": "http://hl7.org/fhir/sid/cvx",
        "code": "09",
        "display": "Td (adult), 2 Lf tetanus toxoid, preservative free, adsorbed"
      }
    ],
    "text": "Td (tétanos y difteria, adultos)"
  },
  "lotNumber": "TD-24-1180",
  "expirationDate": "2026-06-30",
  "site": {
    "coding": [
      {
        "system": "http://snomed.info/sct",
        "code": "368209003",
        "display": "Right upper arm structure"
      }
    ],
    "text": "Brazo derecho"
  },
  "protocolApplied": [
    {
      "series": "Esquema de adultos (refuerzo cada 10 años)",
      "targetDisease": [
        {
          "coding": [
            {
              "system": "http://snomed.info/sct",
              "code": "76902006",
              "display": "Tetanus"
            }
          ],
          "text": "Tétanos"
        }
      ],
      "doseNumberPositiveInt": 4,
      "seriesDosesPositiveInt": 4
    }
  ]
}
```
<!-- /diferencia -->

Es la **cuarta dosis** de un esquema de cuatro (`doseNumberPositiveInt: 4`,
`seriesDosesPositiveInt: 4`), en el brazo derecho. Solución:
[`08e_immunization_td.json`](soluciones/08e_immunization_td.json).

---

## Ejercicios en el servidor

### 08a a 08e · Registrar la vacunación

```http
POST {{FHIRURL}}/Immunization        (vacuna diferida)
POST {{FHIRURL}}/Practitioner        → nursePractitionerId
POST {{FHIRURL}}/Encounter           → vaccinationEncounterId
POST {{FHIRURL}}/Immunization        (influenza)
POST {{FHIRURL}}/Immunization        (Td)
```

### 08f · El carné de vacunación

```http
GET {{FHIRURL}}/Immunization?patient=Patient/{{patientId}}&_sort=date
```

`_sort=date` ordena por fecha. Verás las tres: la diferida del 20 de marzo y
las dos del 3 de abril. Para el carné solo cuentan las aplicadas: agrega
`&status=completed`.

### 08g y 08h · Error a propósito: la vacuna sin fecha

Envía ([`08e1_vacuna_sin_fecha.json`](errores/08e1_vacuna_sin_fecha.json)) una
vacuna con estado, código y paciente, pero **sin `occurrenceDateTime`**. **El
servidor responde `201 Created`.** El validador sí lo detecta:

```
Immunization.occurrence[x]: minimum required = 1, but only found 0
```

Una vacuna sin fecha no sirve para el esquema: no se sabe si la siguiente
dosis toca ya o en diez años. Bórrala con
`DELETE {{FHIRURL}}/Immunization/{{errorImmId}}`.

## Para pensar

Para calcular la **cobertura de vacunación contra la influenza** de una
provincia necesitas el numerador (personas vacunadas) y el denominador
(población objetivo). ¿Qué búsqueda FHIR te daría el numerador? ¿De dónde
sacarías el denominador? *(Pista: las proyecciones de población por
provincia y edad del INEC.)*

## Autoevaluación

<details><summary>1. ¿Por qué se registra una vacuna que no se aplicó?</summary>

Para que quede constancia de que se ofreció y por qué no se aplicó. Sirve
para el seguimiento del paciente y para analizar oportunidades perdidas de
vacunación.
</details>

<details><summary>2. Una vacuna se transcribe de un carné de papel. ¿Qué cambia?</summary>

`primarySource: false`, y se puede indicar el origen con `reportOrigin`. No
se conoce, en general, el lote ni quién vacunó.
</details>

<details><summary>3. ¿Por qué <code>status</code> es un modificador?</summary>

Porque `not-done` invierte el significado: el resto del recurso describe una
vacuna que **no** se aplicó. Un sistema que ignore el estado la contaría como
aplicada.
</details>

## Resumen

- **Immunization** registra una dosis: aplicada (`completed`) o no
  (`not-done`, con su `statusReason`).
- El **lote**, el sitio, la vía y quién vacunó son clave para la seguridad.
- `protocolApplied` dice qué dosis del esquema es.
- Cada visita es un **Encounter** distinto.

## Ejecutar este módulo

- **Postman:** carpeta *08 · Vacunación*.
- **curl:** `curl/taller.sh 08`
- **R:**

  ```r
  carne <- fhir_buscar("Immunization?patient=Patient/{{patientId}}&_sort=date")
  fhir_tabla(carne, list(
    fecha  = function(r) substr(r$occurrenceDateTime, 1, 10),
    vacuna = function(r) r$vaccineCode$text,
    estado = function(r) r$status,
    lote   = function(r) r$lotNumber
  ))
  ```
