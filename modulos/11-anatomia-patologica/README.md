# Módulo 11 · Anatomía patológica

[← Módulo 10](../10-ordenes-y-derivacion/README.md) · [Inicio](../../README.md) · [Módulo 12 →](../12-plan-y-consentimiento/README.md)

> **Nivel:** intermedio · **Duración:** 90 minutos · **Necesitas:** módulos 05, 06 y 10

## Lo que vas a aprender

1. A describir una lesión con **BodyStructure** y una muestra con **Specimen**.
2. A registrar resultados y **corregirlos** dejando rastro (`amended`).
3. A agrupar los resultados en un **DiagnosticReport**.
4. A registrar un diagnóstico basado en un informe.

## La historia

En abril de 2025, Luis nota un **nódulo en la mama izquierda**. El cáncer de
mama en hombres es poco frecuente (alrededor del 1 % de los casos), pero
existe, y Luis tiene un antecedente importante: su madre lo tuvo a los 52
años (módulo 07).

- **6 de mayo:** se toma la **biopsia** que se pidió en el módulo 10.
- **8 de mayo:** el patólogo informa un tumor de **2,5 cm**. Al revisar la
  pieza, corrige la medida a **3,5 cm**.
- **12 de mayo:** la inmunohistoquímica muestra **receptor de estrógeno
  positivo** (90 % de las células, Allred 8).
- **13 de mayo:** el informe concluye **carcinoma ductal infiltrante** de la
  mama izquierda, y se registra el diagnóstico.

> En el caso, la misma Dra. Salazar figura como responsable de todo, para no
> multiplicar los profesionales. En la realidad, el patólogo sería otro
> Practitioner.

---

## Ficha del recurso: BodyStructure

**¿Qué es?** Una **estructura anatómica concreta del paciente**: este tumor,
esta lesión, este lunar. No una parte del cuerpo en general, sino una que se
identifica y se sigue en el tiempo.

**¿Para qué se usa?** Para que varias observaciones, procedimientos e
imágenes se refieran a **la misma lesión**. El tamaño medido hoy y el de
dentro de tres meses apuntan al mismo BodyStructure (con `focus`).

**¿Cuándo usar otro recurso?** Si solo necesitas decir dónde se hizo algo
("mama izquierda"), basta con el elemento `bodySite` del recurso, con un
código SNOMED CT.

<!-- ficha BodyStructure -->
| Elemento | Card. | Tipo | Para qué sirve |
|---|---|---|---|
| `identifier` | 0..* | Identifier | Identificador de la estructura. |
| `active` ⚑ | 0..1 | boolean | Si el registro está en uso. |
| `morphology` | 0..1 | CodeableConcept | Qué tipo de estructura es: un carcinoma, un quiste... |
| `location` | 0..1 | CodeableConcept | Dónde está. |
| `locationQualifier` | 0..* | CodeableConcept | Precisión de la ubicación: lado, cuadrante. |
| `description` | 0..1 | string | Descripción en texto. |
| `image` | 0..* | Attachment | Imágenes. |
| `patient` | **1..1** | Reference(Patient) | De quién. |
<!-- /ficha -->

## Ficha del recurso: Specimen

**¿Qué es?** Una **muestra** obtenida del paciente para analizarla: sangre,
orina, tejido de una biopsia, un hisopado.

**¿Para qué se usa?** Para saber **de qué muestra** sale cada resultado,
cuándo y cómo se tomó y en qué estado está.

<!-- ficha Specimen -->
| Elemento | Card. | Tipo | Para qué sirve |
|---|---|---|---|
| `identifier` | 0..* | Identifier | Número de la muestra. |
| `accessionIdentifier` | 0..1 | Identifier | Número que le asigna el laboratorio al recibirla. |
| `status` ⚑ | 0..1 | code | `available`, `unavailable`, `unsatisfactory` o `entered-in-error`. |
| `type` | 0..1 | CodeableConcept | Qué muestra es: sangre, tejido tumoral... |
| `subject` | 0..1 | Reference(Patient \| Group \| Device \| Substance \| …) | De quién. |
| `receivedTime` | 0..1 | dateTime | Cuándo llegó al laboratorio. |
| `parent` | 0..* | Reference(Specimen) | La muestra de la que se obtuvo (una alícuota). |
| `request` | 0..* | Reference(ServiceRequest) | La orden que pidió el análisis. |
| `collection` | 0..1 | BackboneElement | La toma. |
| `collection.collector` | 0..1 | Reference(Practitioner \| PractitionerRole) | Quién la tomó. |
| `collection.collected[x]` | 0..1 | dateTime \| Period | Cuándo. |
| `collection.method` | 0..1 | CodeableConcept | Cómo: biopsia, punción, venopunción. |
| `collection.bodySite` | 0..1 | CodeableConcept | De qué parte del cuerpo. |
| `processing` | 0..* | BackboneElement | Procesamiento: fijación, tinción. |
| `container` | 0..* | BackboneElement | Recipiente. |
| `note` | 0..* | Annotation | Notas. |
<!-- /ficha -->

## Ficha del recurso: DiagnosticReport

**¿Qué es?** El **informe** de un estudio diagnóstico: un hemograma, una
radiografía, una anatomía patológica. Agrupa los resultados (Observation), la
muestra, la interpretación y la conclusión.

**¿Para qué se usa?** Para entregar un resultado **completo y firmado**: no
solo las mediciones sueltas, sino lo que significan juntas.

**¿Cuándo usar otro recurso?** Una medición suelta, sin informe, es una
**Observation**. Un informe que ya existe como PDF se adjunta en
`presentedForm` o con un **DocumentReference**.

<!-- ficha DiagnosticReport -->
| Elemento | Card. | Tipo | Para qué sirve |
|---|---|---|---|
| `identifier` | 0..* | Identifier | Número del informe. |
| `basedOn` | 0..* | Reference(CarePlan \| ImmunizationRecommendation \| MedicationRequest \| NutritionOrder \| …) | La orden que lo pidió. |
| `status` ⚑ | **1..1** | code | `registered`, `partial`, `preliminary`, `final`, `amended`... |
| `category` | 0..* | CodeableConcept | Servicio que lo emite: laboratorio, imagen, patología. |
| `code` | **1..1** | CodeableConcept | Qué estudio es: un código LOINC. |
| `subject` | 0..1 | Reference(Patient \| Group \| Device \| Location) | De quién. |
| `encounter` | 0..1 | Reference(Encounter) | En qué atención. |
| `effective[x]` | 0..1 | dateTime \| Period | A qué momento se refieren los resultados. |
| `issued` | 0..1 | instant | Cuándo se emitió el informe. |
| `performer` | 0..* | Reference(Practitioner \| PractitionerRole \| Organization \| CareTeam) | Quién es responsable del informe. |
| `resultsInterpreter` | 0..* | Reference(Practitioner \| PractitionerRole \| Organization \| CareTeam) | Quién interpretó los resultados. |
| `specimen` | 0..* | Reference(Specimen) | Las muestras analizadas. |
| `result` | 0..* | Reference(Observation) | Las observaciones del informe. |
| `conclusion` | 0..1 | string | La conclusión en texto. |
| `conclusionCode` | 0..* | CodeableConcept | La conclusión codificada. |
| `presentedForm` | 0..* | Attachment | El informe como archivo (PDF). |
<!-- /ficha -->

**Cómo se enlaza todo:**

```
Condition (cáncer de mama) ──evidence──▶ DiagnosticReport (informe)
                                           │ result            │ specimen
                                           ▼                   ▼
                        Observation (tamaño, receptor) ──▶ Specimen (biopsia)
                                           │ focus
                                           ▼
                                     BodyStructure (tumor)
```

---

## Paso a paso: el tumor

### Paso 1 · El mínimo: de quién es

<!-- paso 11a 1 -->
```json
{
  "resourceType": "BodyStructure",
  "patient": {
    "reference": "Patient/{{patientId}}",
    "display": "Luis Alberto Paredes Cevallos"
  }
}
```
<!-- /paso -->

### Paso 2 · Qué es y dónde está

<!-- paso 11a 2 -->
```json
{
  "morphology": {
    "coding": [
      {
        "system": "http://snomed.info/sct",
        "code": "82711006",
        "display": "Infiltrating duct carcinoma"
      }
    ],
    "text": "Carcinoma ductal infiltrante"
  },
  "location": {
    "coding": [
      {
        "system": "http://snomed.info/sct",
        "code": "80248007",
        "display": "Left breast structure"
      }
    ],
    "text": "Mama izquierda"
  },
  "description": "Carcinoma ductal infiltrante primario de mama izquierda"
}
```
<!-- /paso -->

La morfología con SNOMED CT: `82711006` *Infiltrating duct carcinoma*. La
ubicación: `80248007` *Left breast structure*.

### Paso 3 · Identificador, estado y narrativa

<!-- paso 11a 3 -->
```json
{
  "identifier": [
    {
      "system": "https://f-slg.github.io/aprende-fhir/sid/estructura-corporal",
      "value": "EC-2025-0001"
    }
  ],
  "active": true,
  "text": {
    "status": "generated",
    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><p>Tumor primario en mama izquierda: carcinoma ductal infiltrante.</p></div>"
  }
}
```
<!-- /paso -->

Solución: [`11a_bodystructure_tumor.json`](soluciones/11a_bodystructure_tumor.json).

**11b · Precisar la ubicación.** Con `PUT`, se agrega la lateralidad y el
cuadrante. Lo que cambia:

<!-- diferencia 11b -->
```json
{
  "id": "{{bodyStructureId}}",
  "description": "Carcinoma ductal infiltrante primario de mama izquierda, cuadrante superior externo",
  "locationQualifier": [
    {
      "coding": [
        {
          "system": "http://snomed.info/sct",
          "code": "7771000",
          "display": "Left"
        }
      ],
      "text": "Izquierdo"
    }
  ]
}
```
<!-- /diferencia -->

## Paso a paso: la biopsia

### Paso 1 · Qué muestra es y de quién

<!-- paso 11c 1 -->
```json
{
  "resourceType": "Specimen",
  "type": {
    "coding": [
      {
        "system": "http://snomed.info/sct",
        "code": "258435002",
        "display": "Tumor tissue sample"
      }
    ],
    "text": "Tejido tumoral"
  },
  "subject": {
    "reference": "Patient/{{patientId}}",
    "display": "Luis Alberto Paredes Cevallos"
  }
}
```
<!-- /paso -->

SNOMED `258435002` *Tumor tissue sample*. Más específico que "muestra" en
general: el laboratorio sabe qué recibe.

### Paso 2 · Cómo, cuándo y dónde se tomó

<!-- paso 11c 2 -->
```json
{
  "collection": {
    "collector": {
      "reference": "Practitioner/{{practitionerId}}",
      "display": "Dra. Andrea Lucía Salazar Moreno"
    },
    "collectedDateTime": "2025-05-06T09:00:00-05:00",
    "method": {
      "coding": [
        {
          "system": "http://snomed.info/sct",
          "code": "129314006",
          "display": "Biopsy - action"
        }
      ],
      "text": "Biopsia"
    },
    "bodySite": {
      "coding": [
        {
          "system": "http://snomed.info/sct",
          "code": "80248007",
          "display": "Left breast structure"
        }
      ],
      "text": "Mama izquierda"
    }
  }
}
```
<!-- /paso -->

### Paso 3 · Identificador, estado, recepción y la orden

<!-- paso 11c 3 -->
```json
{
  "identifier": [
    {
      "system": "https://f-slg.github.io/aprende-fhir/sid/muestra",
      "value": "AP-2025-0457"
    }
  ],
  "status": "available",
  "receivedTime": "2025-05-06T10:30:00-05:00",
  "text": {
    "status": "generated",
    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><p>Biopsia de tejido tumoral de mama izquierda (AP-2025-0457). Estado: available.</p></div>"
  },
  "request": [
    {
      "reference": "ServiceRequest/{{biopsyRequestId}}",
      "display": "Orden de biopsia de mama"
    }
  ]
}
```
<!-- /paso -->

`request` apunta a la orden de biopsia del módulo 10: así el laboratorio
sabe qué se pidió con esta muestra. Solución:
[`11c_specimen_crear.json`](soluciones/11c_specimen_crear.json).

**11d · La muestra se agota.** Tras la inmunohistoquímica no queda tejido.
Lo que cambia:

<!-- diferencia 11d -->
```json
{
  "id": "{{specimenId}}",
  "status": "unavailable",
  "note": [
    {
      "text": "Muestra agotada tras los estudios de inmunohistoquímica."
    }
  ]
}
```
<!-- /diferencia -->

## Paso a paso: el tamaño del tumor

### Paso 1 · El mínimo: estado y código

<!-- paso 11e 1 -->
```json
{
  "resourceType": "Observation",
  "status": "final",
  "code": {
    "coding": [
      {
        "system": "http://snomed.info/sct",
        "code": "263605001",
        "display": "Length dimension of neoplasm"
      }
    ],
    "text": "Tamaño del tumor"
  }
}
```
<!-- /paso -->

SNOMED `263605001` *Length dimension of neoplasm*.

### Paso 2 · El resultado: 2,5 cm

<!-- paso 11e 2 -->
```json
{
  "category": [
    {
      "coding": [
        {
          "system": "http://terminology.hl7.org/CodeSystem/observation-category",
          "code": "laboratory",
          "display": "Laboratory"
        }
      ]
    }
  ],
  "subject": {
    "reference": "Patient/{{patientId}}",
    "display": "Luis Alberto Paredes Cevallos"
  },
  "effectiveDateTime": "2025-05-08",
  "performer": [
    {
      "reference": "Practitioner/{{practitionerId}}",
      "display": "Dra. Andrea Lucía Salazar Moreno"
    }
  ],
  "valueQuantity": {
    "value": 2.5,
    "unit": "cm",
    "system": "http://unitsofmeasure.org",
    "code": "cm"
  }
}
```
<!-- /paso -->

### Paso 3 · A qué se refiere: el tumor, la mama y la muestra

<!-- paso 11e 3 -->
```json
{
  "focus": [
    {
      "reference": "BodyStructure/{{bodyStructureId}}",
      "display": "Tumor de mama izquierda"
    }
  ],
  "bodySite": {
    "coding": [
      {
        "system": "http://snomed.info/sct",
        "code": "80248007",
        "display": "Left breast structure"
      }
    ],
    "text": "Mama izquierda"
  },
  "specimen": {
    "reference": "Specimen/{{specimenId}}",
    "display": "Biopsia AP-2025-0457"
  },
  "text": {
    "status": "generated",
    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><p>Tamaño del tumor: 2,5 cm. Estado: final.</p></div>"
  }
}
```
<!-- /paso -->

`focus` dice que la medida es **del tumor**, no del paciente en general. Así,
una medida futura del mismo tumor se compara con esta. Solución:
[`11e_observation_tamano_tumor.json`](soluciones/11e_observation_tamano_tumor.json).

### Corregir un resultado: `amended`

El patólogo revisa la pieza y la medida correcta es 3,5 cm. **No se borra ni
se crea otra observación**: se actualiza la misma con `PUT`, con
`status: amended` y una nota que explica la corrección. Lo que cambia:

<!-- diferencia 11f -->
```json
{
  "id": "{{obsTumorId}}",
  "status": "amended",
  "valueQuantity": {
    "value": 3.5,
    "unit": "cm",
    "system": "http://unitsofmeasure.org",
    "code": "cm"
  },
  "note": [
    {
      "text": "Corrección: la medición inicial de 2,5 cm se rectifica a 3,5 cm tras la revisión de la pieza."
    }
  ]
}
```
<!-- /diferencia -->

El historial (`_history`) conserva la versión de 2,5 cm. Cualquiera puede
ver qué se informó primero y cuándo se corrigió: es la **trazabilidad** que
exige un registro clínico.

El **receptor de estrógeno** sigue el mismo camino: se informa positivo
([`11g`](soluciones/11g_observation_receptor_estrogeno.json), LOINC `85337-4`)
y después se amplía con el porcentaje y la puntuación de Allred. Lo que
cambia:

<!-- diferencia 11h -->
```json
{
  "id": "{{obsREId}}",
  "status": "amended",
  "interpretation": [
    {
      "coding": [
        {
          "system": "http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation",
          "code": "POS",
          "display": "Positive"
        }
      ]
    }
  ],
  "note": [
    {
      "text": "Positivo en el 90 % de las células tumorales, intensidad fuerte (Allred 8/8)."
    }
  ]
}
```
<!-- /diferencia -->

## Paso a paso: el informe

### Paso 1 · El mínimo: estado y código

<!-- paso 11i 1 -->
```json
{
  "resourceType": "DiagnosticReport",
  "status": "final",
  "code": {
    "coding": [
      {
        "system": "http://loinc.org",
        "code": "11526-1",
        "display": "Pathology study"
      }
    ],
    "text": "Estudio de patología"
  }
}
```
<!-- /paso -->

LOINC `11526-1` *Pathology study*.

### Paso 2 · De quién, cuándo y quién informa

<!-- paso 11i 2 -->
```json
{
  "category": [
    {
      "coding": [
        {
          "system": "http://terminology.hl7.org/CodeSystem/v2-0074",
          "code": "SP",
          "display": "Surgical Pathology"
        }
      ],
      "text": "Anatomía patológica"
    }
  ],
  "subject": {
    "reference": "Patient/{{patientId}}",
    "display": "Luis Alberto Paredes Cevallos"
  },
  "effectiveDateTime": "2025-05-12",
  "issued": "2025-05-13T12:00:00-05:00",
  "performer": [
    {
      "reference": "Organization/{{hospitalId}}",
      "display": "Hospital General Docente Ejemplo"
    }
  ],
  "resultsInterpreter": [
    {
      "reference": "Practitioner/{{practitionerId}}",
      "display": "Dra. Andrea Lucía Salazar Moreno"
    }
  ]
}
```
<!-- /paso -->

`category` con la tabla `v2-0074`: `SP` es *Surgical Pathology*. `effective`
es cuándo se hizo el estudio; `issued`, cuándo se publicó el informe.

### Paso 3 · La orden, la muestra y los resultados

<!-- paso 11i 3 -->
```json
{
  "specimen": [
    {
      "reference": "Specimen/{{specimenId}}",
      "display": "Biopsia AP-2025-0457"
    }
  ],
  "result": [
    {
      "reference": "Observation/{{obsTumorId}}",
      "display": "Tamaño del tumor 3,5 cm"
    },
    {
      "reference": "Observation/{{obsREId}}",
      "display": "Receptor de estrógeno positivo"
    }
  ],
  "basedOn": [
    {
      "reference": "ServiceRequest/{{biopsyRequestId}}",
      "display": "Orden de biopsia de mama"
    }
  ]
}
```
<!-- /paso -->

`basedOn` cierra el ciclo con la orden de biopsia, como el informe de la
ecografía en el módulo 10.

### Paso 4 · La conclusión

<!-- paso 11i 4 -->
```json
{
  "conclusion": "Carcinoma ductal infiltrante de mama izquierda, 3,5 cm, receptor de estrógeno positivo.",
  "conclusionCode": [
    {
      "coding": [
        {
          "system": "http://snomed.info/sct",
          "code": "254837009",
          "display": "Malignant neoplasm of breast"
        }
      ],
      "text": "Cáncer de mama"
    }
  ],
  "identifier": [
    {
      "system": "https://f-slg.github.io/aprende-fhir/sid/informe",
      "value": "INF-AP-2025-0457"
    }
  ],
  "text": {
    "status": "generated",
    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><p>Informe de anatomía patológica: carcinoma ductal infiltrante de mama izquierda de 3,5 cm,</p><p>receptor de estrógeno positivo (Allred 8).</p></div>"
  }
}
```
<!-- /paso -->

`conclusion` para personas, `conclusionCode` para las máquinas (SNOMED
`254837009`, *Malignant neoplasm of breast*). Solución:
[`11i_diagnosticreport_patologia.json`](soluciones/11i_diagnosticreport_patologia.json).

## Paso a paso: el diagnóstico de cáncer

### Paso 1 · El diagnóstico con dos códigos

<!-- paso 11j 1 -->
```json
{
  "resourceType": "Condition",
  "subject": {
    "reference": "Patient/{{patientId}}",
    "display": "Luis Alberto Paredes Cevallos"
  },
  "code": {
    "coding": [
      {
        "system": "http://hl7.org/fhir/sid/icd-10",
        "code": "C50.9",
        "display": "Breast, unspecified"
      },
      {
        "system": "http://snomed.info/sct",
        "code": "254837009",
        "display": "Malignant neoplasm of breast"
      }
    ],
    "text": "Carcinoma ductal infiltrante de mama izquierda"
  }
}
```
<!-- /paso -->

Un `CodeableConcept` puede tener **varios** `coding` que dicen lo mismo en
distintas terminologías: CIE-10 `C50.9` para la estadística y SNOMED CT
`254837009` para la historia clínica.

### Paso 2 · Estados, categoría y sitio

<!-- paso 11j 2 -->
```json
{
  "clinicalStatus": {
    "coding": [
      {
        "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
        "code": "active",
        "display": "Active"
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
          "code": "problem-list-item",
          "display": "Problem List Item"
        }
      ]
    }
  ],
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

Ahora la categoría es `problem-list-item`: no es el diagnóstico de una
consulta, sino un problema que acompañará a Luis durante años.

### Paso 3 · Fechas, autor y la evidencia: el informe

<!-- paso 11j 3 -->
```json
{
  "onsetDateTime": "2025-05-13",
  "recordedDate": "2025-05-13",
  "recorder": {
    "reference": "Practitioner/{{practitionerId}}",
    "display": "Dra. Andrea Lucía Salazar Moreno"
  },
  "evidence": [
    {
      "detail": [
        {
          "reference": "DiagnosticReport/{{diagnosticReportId}}",
          "display": "Informe de patología AP-2025-0457"
        }
      ]
    }
  ],
  "identifier": [
    {
      "system": "https://f-slg.github.io/aprende-fhir/sid/condicion",
      "value": "COND-2025-0002"
    }
  ],
  "text": {
    "status": "generated",
    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><p>Carcinoma ductal infiltrante de mama izquierda (activo, confirmado).</p><p>Diagnóstico: 13 de mayo de 2025.</p></div>"
  }
}
```
<!-- /paso -->

`evidence.detail` apunta al informe de patología: el diagnóstico tiene
sustento verificable. Solución:
[`11j_condition_cancer_mama.json`](soluciones/11j_condition_cancer_mama.json).

---

## Ejercicios en el servidor

| Paso | Petición | Guarda |
|---|---|---|
| 11a | `POST /BodyStructure` | `bodyStructureId` |
| 11b | `PUT /BodyStructure/{{bodyStructureId}}` | |
| 11c | `POST /Specimen` | `specimenId` |
| 11d | `PUT /Specimen/{{specimenId}}` | |
| 11e | `POST /Observation` (2,5 cm) | `obsTumorId` |
| 11f | Error a propósito (abajo) | |
| 11g | `PUT /Observation/{{obsTumorId}}` (3,5 cm, amended) | |
| 11h | `GET /Observation/{{obsTumorId}}/_history` | |
| 11i | `POST /Observation` (receptor de estrógeno) | `obsREId` |
| 11j | `PUT /Observation/{{obsREId}}` (amended) | |
| 11k | `POST /DiagnosticReport` | `diagnosticReportId` |
| 11l | `POST /Condition` | `conditionCancerId` |
| 11m | `GET /DiagnosticReport?subject=Patient/{{patientId}}&_include=DiagnosticReport:result` | |

### 11f · Error a propósito: actualizar sin `id`

Envía `PUT {{FHIRURL}}/Observation/{{obsTumorId}}` con un recurso que **no
tiene `id`** ([`11e1_actualizar_sin_id.json`](errores/11e1_actualizar_sin_id.json)).
El servidor responde **`400`**:

```
HAPI-0419: Can not update resource, resource body must contain an ID element for update (PUT) operation
```

En una actualización, el `id` del cuerpo debe coincidir con el de la ruta.
Es otro error que el validador no detecta: el recurso es válido, lo que
falla es la operación.

### 11h · El historial

En el historial verás dos versiones: 2,5 cm con `final` y 3,5 cm con
`amended`.

## Autoevaluación

<details><summary>1. ¿Por qué no se borra la observación de 2,5 cm y se crea otra de 3,5 cm?</summary>

Porque se perdería el rastro: no se sabría que hubo una medida anterior ni
cuándo se corrigió. Con `PUT` y `amended`, el historial conserva ambas.
</details>

<details><summary>2. ¿Qué diferencia hay entre <code>bodySite</code> y un BodyStructure?</summary>

`bodySite` dice dónde, con un código: "mama izquierda". BodyStructure
identifica **una** estructura concreta del paciente (este tumor) a la que
varios recursos pueden apuntar a lo largo del tiempo.
</details>

<details><summary>3. ¿Para qué sirven dos códigos en el diagnóstico de cáncer?</summary>

CIE-10 para la estadística de morbilidad y mortalidad; SNOMED CT, más
detallado, para la historia clínica y el apoyo a decisiones.
</details>

## Resumen

- **BodyStructure** identifica una lesión concreta; **Specimen**, la muestra.
- Un resultado se corrige con `PUT` y `status: amended`; el historial
  conserva la versión anterior.
- **DiagnosticReport** agrupa resultados, muestra y conclusión.
- El diagnóstico se enlaza con su sustento mediante `evidence`.

## Ejecutar este módulo

- **Postman:** carpeta *11 · Anatomía patológica*.
- **curl:** `curl/taller.sh 11`
- **R:**

  ```r
  h <- fhir_leer("Observation/{{obsTumorId}}/_history")
  fhir_tabla(h, list(
    version = function(r) r$meta$versionId,
    estado  = function(r) r$status,
    cm      = function(r) r$valueQuantity$value
  ))
  ```
