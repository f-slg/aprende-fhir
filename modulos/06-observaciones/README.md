# Módulo 06 · Observaciones: signos vitales y tipos de valor

[← Módulo 05](../05-diagnostico-y-encuentro/README.md) · [Inicio](../../README.md) · [Módulo 07 →](../07-antecedentes/README.md)

> **Nivel:** básico · **Duración:** 75 minutos · **Necesitas:** módulo 05

## Lo que vas a aprender

1. Qué es **Observation**, el recurso más usado de FHIR.
2. A registrar signos vitales según el **perfil de signos vitales** de FHIR R4.
3. Los distintos **tipos de valor** (`value[x]`).
4. A modelar mediciones con varias partes usando `component`.
5. A expresar unidades con **UCUM** y códigos con **LOINC**.

## La historia

En la consulta del 20 de marzo, a las 07:30, la Dra. Salazar registra:

| Medición | Resultado |
|---|---|
| Presión arterial | 128/84 mmHg |
| Temperatura | 38,4 °C |
| Frecuencia respiratoria | 20 por minuto |
| Frecuencia cardíaca | 102 por minuto |
| Fiebre | presente |
| Motivo de consulta | "Dolor abdominal tipo cólico desde hace 3 días, con náuseas y diarrea" |
| Sangre oculta en heces | positiva |
| Reacción de Widal, antígeno O | título 1:160 |

Cada una es una **Observation**.

---

## Ficha del recurso: Observation

**¿Qué es?** Una **medición o afirmación simple** sobre un paciente: un
signo vital, un resultado de laboratorio, un hallazgo del examen físico, el
puntaje de una escala, un dato social (tabaquismo, ocupación).

**¿Para qué se usa?** Para casi todo lo que se **mide o se observa**. Es el
recurso más usado de FHIR: un paciente hospitalizado puede acumular miles.

**¿Cuándo usar otro recurso?**

- Un diagnóstico o problema de salud: **Condition**.
- Un informe que agrupa resultados (un hemograma completo, un informe de
  patología): **DiagnosticReport**, que apunta a las Observation (módulo 11).
- Una alergia: **AllergyIntolerance**.
- Las respuestas de un formulario completo: **QuestionnaireResponse**.

**Elementos principales** (<https://hl7.org/fhir/R4/observation.html>):

<!-- ficha Observation -->
| Elemento | Card. | Tipo | Para qué sirve |
|---|---|---|---|
| `status` ⚑ | **1..1** | code | `registered`, `preliminary`, `final`, `amended`, `cancelled`, `entered-in-error`. |
| `category` | 0..* | CodeableConcept | Clase: `vital-signs`, `laboratory`, `exam`, `survey`, `social-history`, `imaging`... |
| `code` | **1..1** | CodeableConcept | **Qué** se observó: casi siempre un código LOINC. |
| `subject` | 0..1 | Reference(Patient \| Group \| Device \| Location) | De quién. |
| `focus` | 0..* | Reference(Resource) | Sobre qué, si no es el propio paciente (un tumor, un feto). |
| `encounter` | 0..1 | Reference(Encounter) | En qué atención. |
| `effective[x]` | 0..1 | dateTime \| Period \| Timing \| instant | Cuándo se observó. |
| `issued` | 0..1 | instant | Cuándo se publicó el resultado. |
| `performer` | 0..* | Reference(Practitioner \| PractitionerRole \| Organization \| CareTeam \| …) | Quién lo midió o informó. |
| `value[x]` | 0..1 | Quantity \| CodeableConcept \| string \| boolean \| … | **El resultado**. Su tipo cambia según la observación (ver abajo). |
| `dataAbsentReason` | 0..1 | CodeableConcept | Por qué no hay resultado (muestra hemolizada, paciente se negó). |
| `interpretation` | 0..* | CodeableConcept | Alto, bajo, normal, positivo... |
| `note` | 0..* | Annotation | Comentarios. |
| `bodySite` | 0..1 | CodeableConcept | Parte del cuerpo. |
| `method` | 0..1 | CodeableConcept | Cómo se midió. |
| `specimen` | 0..1 | Reference(Specimen) | La muestra analizada. |
| `referenceRange` | 0..* | BackboneElement | Valores de referencia. |
| `hasMember` | 0..* | Reference(Observation \| QuestionnaireResponse \| MolecularSequence) | Observaciones que agrupa (un panel). |
| `component` | 0..* | BackboneElement | Partes de una observación con varios valores (sistólica y diastólica). |
<!-- /ficha -->

**Los tipos de `value[x]`:**

| Si el resultado es... | Se usa | Ejemplo del caso |
|---|---|---|
| una cantidad con unidad | `valueQuantity` | Temperatura 38,4 °C |
| sí o no | `valueBoolean` | Fiebre: presente |
| un texto libre | `valueString` | Motivo de consulta |
| un concepto codificado | `valueCodeableConcept` | Sangre oculta: positivo |
| una proporción | `valueRatio` | Título 1:160 |
| un número entero | `valueInteger` | Número de deposiciones |
| una fecha, una hora, un periodo | `valueDateTime`, `valueTime`, `valuePeriod` | Fecha de la última menstruación |

**El perfil de signos vitales.** FHIR R4 define que todo signo vital debe
tener `status`, `category = vital-signs`, `code` LOINC, `subject`,
`effective[x]` y un valor en unidades UCUM. El validador aplica este perfil
**automáticamente** cuando reconoce el código LOINC de un signo vital, aunque
el recurso no lo declare.

| Signo vital | LOINC | Unidad UCUM |
|---|---|---|
| Presión arterial (panel) | `85354-9` | componentes en `mm[Hg]` |
| Presión sistólica / diastólica | `8480-6` / `8462-4` | `mm[Hg]` |
| Temperatura corporal | `8310-5` | `Cel` |
| Frecuencia respiratoria | `9279-1` | `/min` |
| Frecuencia cardíaca | `8867-4` | `/min` |
| Saturación de oxígeno | `2708-6` | `%` |
| Peso / talla | `29463-7` / `8302-2` | `kg` / `cm` |
| Índice de masa corporal | `39156-5` | `kg/m2` |

**UCUM** (*Unified Code for Units of Measure*) es el estándar de unidades. En
`valueQuantity`, `unit` es lo que lee la persona (`°C`) y `code` lo que
entiende la máquina (`Cel`). Los códigos UCUM distinguen mayúsculas.

---

## Paso a paso: la presión arterial

La presión arterial no es un valor sino **dos**: sistólica y diastólica. No
se registra como texto (`"128/84"`) ni como proporción: es una observación
con dos **componentes**, cada uno con su propio código y valor.

### Paso 1 · Lo que exige el perfil de signos vitales

<!-- paso 06a 1 -->
```json
{
  "resourceType": "Observation",
  "status": "final",
  "category": [
    {
      "coding": [
        {
          "system": "http://terminology.hl7.org/CodeSystem/observation-category",
          "code": "vital-signs",
          "display": "Vital Signs"
        }
      ]
    }
  ],
  "code": {
    "coding": [
      {
        "system": "http://loinc.org",
        "code": "85354-9",
        "display": "Blood pressure panel with all children optional"
      }
    ],
    "text": "Presión arterial"
  },
  "subject": {
    "reference": "Patient/{{patientId}}",
    "display": "Luis Alberto Paredes Cevallos"
  },
  "effectiveDateTime": "2025-03-20T07:30:00-05:00",
  "component": [
    {
      "code": {
        "coding": [
          {
            "system": "http://loinc.org",
            "code": "8480-6",
            "display": "Systolic blood pressure"
          }
        ],
        "text": "Presión sistólica"
      },
      "valueQuantity": {
        "value": 128,
        "unit": "mmHg",
        "system": "http://unitsofmeasure.org",
        "code": "mm[Hg]"
      }
    },
    {
      "code": {
        "coding": [
          {
            "system": "http://loinc.org",
            "code": "8462-4",
            "display": "Diastolic blood pressure"
          }
        ],
        "text": "Presión diastólica"
      },
      "valueQuantity": {
        "value": 84,
        "unit": "mmHg",
        "system": "http://unitsofmeasure.org",
        "code": "mm[Hg]"
      }
    }
  ]
}
```
<!-- /paso -->

Como `85354-9` es un signo vital, el validador exige desde el primer paso
todo lo del perfil: estado, categoría, código, paciente, fecha y los dos
componentes. Si quitas uno, verás el error. Por ejemplo, sin `component`:

```
Observation.component: minimum required = 2, but only found 0 (from http://hl7.org/fhir/StructureDefinition/bp|4.0.1)
```

La observación principal **no tiene `value[x]`**: los valores están en los
componentes.

### Paso 2 · En qué consulta, quién midió y la narrativa

<!-- paso 06a 2 -->
```json
{
  "encounter": {
    "reference": "Encounter/{{encounterId}}",
    "display": "Consulta por dolor abdominal"
  },
  "performer": [
    {
      "reference": "Practitioner/{{practitionerId}}",
      "display": "Dra. Andrea Lucía Salazar Moreno"
    }
  ],
  "text": {
    "status": "generated",
    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><p>Presión arterial: 128/84 mmHg.</p></div>"
  }
}
```
<!-- /paso -->

`encounter` enlaza con la consulta del módulo 05 y `performer`, con la
médica. Solución:
[`06a_observation_presion_arterial.json`](soluciones/06a_observation_presion_arterial.json).

## Los demás signos vitales: cambia el código y el valor

La temperatura, la frecuencia respiratoria y la cardíaca son iguales a la
presión arterial, pero con un solo valor en `valueQuantity` en lugar de
componentes. Esto es lo que cambia en la temperatura:

<!-- diferencia 06b -->
```json
{
  "code": {
    "coding": [
      {
        "system": "http://loinc.org",
        "code": "8310-5",
        "display": "Body temperature"
      }
    ],
    "text": "Temperatura corporal"
  },
  "valueQuantity": {
    "value": 38.4,
    "unit": "°C",
    "system": "http://unitsofmeasure.org",
    "code": "Cel"
  }
}
```
<!-- /diferencia -->

Soluciones: [`06b` temperatura](soluciones/06b_observation_temperatura.json) ·
[`06c` frecuencia respiratoria](soluciones/06c_observation_frecuencia_respiratoria.json) ·
[`06d` frecuencia cardíaca](soluciones/06d_observation_frecuencia_cardiaca.json).

## Otros tipos de valor

| Ejercicio | Código | Valor | Solución |
|---|---|---|---|
| 06e · Fiebre | SNOMED `386661006` *Fever* | `"valueBoolean": true` | [`06e`](soluciones/06e_observation_fiebre_boolean.json) |
| 06f · Motivo de consulta | LOINC `10154-3` | `"valueString": "Dolor abdominal…"` | [`06f`](soluciones/06f_observation_motivo_string.json) |
| 06g · Sangre oculta en heces | LOINC `2335-8` | `valueCodeableConcept` SNOMED `10828004` *Positive* | [`06g`](soluciones/06g_observation_sangre_oculta_codeable.json) |
| 06h · Título de Widal | solo `code.text` | `valueRatio` 1 / 160 | [`06h`](soluciones/06h_observation_titulo_ratio.json) |

Fíjate en la **categoría** de cada una: la fiebre es un hallazgo del examen
(`exam`), el motivo de consulta lo cuenta el paciente (`survey`) y la sangre
oculta y el Widal son de laboratorio (`laboratory`).

---

## Ejercicios en el servidor

### 06a a 06h · Registrar las observaciones

```http
POST {{FHIRURL}}/Observation
```

Guarda los `id` de los cuatro signos vitales (`obsPAId`, `obsTempId`,
`obsFRId`, `obsFCId`): los usarás en el módulo 09.

### 06i · Buscar los signos vitales

```http
GET {{FHIRURL}}/Observation?subject=Patient/{{patientId}}&category=vital-signs
```

Devuelve los cuatro signos vitales y no las demás observaciones. Prueba
también `&code=http://loinc.org|8310-5` para traer solo la temperatura.

### 06j · Error a propósito: el decimal con coma

Envía ([`06e1_decimal_con_coma.json`](errores/06e1_decimal_con_coma.json))
una temperatura con `"value": "38,4"`. El servidor responde **`400`**:

```
HAPI-1821: [element="value"] Invalid attribute value "38,4": Character , is neither a decimal digit number, decimal point, nor "e" notation exponential mark.
```

En JSON los números van **sin comillas** y con **punto**: `38.4`.

### 06k y 06l · Error a propósito: la observación sin código

Envía ([`06e2_observacion_sin_codigo.json`](errores/06e2_observacion_sin_codigo.json))
una observación con estado, paciente y valor, pero **sin `code`**. **El
servidor responde `201 Created`**: la guarda.

¿Qué es 38,4 °C? ¿La temperatura? ¿La de la habitación? Sin `code` el dato no
sirve. `code` es **obligatorio** (`1..1`) y el validador lo detecta:

```
Observation.code: minimum required = 1, but only found 0
```

El servidor no comprobó la cardinalidad: es un **error de contenido** (módulo
01). Bórrala con `DELETE {{FHIRURL}}/Observation/{{errorObsId}}` para que no
quede en el expediente de Luis.

### Reto · Codificar el título de Widal

La observación `06h` solo tiene `code.text`. Busca en
<https://loinc.org/search/> el código LOINC del título de anticuerpos contra
el antígeno O de *Salmonella typhi* en suero, agrégalo como `coding` y valida
el recurso.

## Autoevaluación

<details><summary>1. ¿Por qué la presión arterial no usa <code>valueRatio</code> ni <code>valueString</code>?</summary>

Porque son dos mediciones distintas, cada una con su propio código LOINC.
Con componentes, un sistema puede graficar la sistólica o alertar si la
diastólica supera un umbral. Con un texto `"128/84"`, no.
</details>

<details><summary>2. ¿Qué diferencia hay entre <code>unit</code> y <code>code</code> en un <code>valueQuantity</code>?</summary>

`unit` es lo que lee la persona (`°C`, `latidos/min`). `code` es la unidad
UCUM que entiende la máquina (`Cel`, `/min`). Para comparar o convertir se usa
`code`.
</details>

<details><summary>3. El servidor aceptó una observación sin <code>code</code>. ¿Por qué?</summary>

Porque muchos servidores no validan la cardinalidad al guardar. Que el
servidor acepte un recurso no garantiza que sea válido: hay que validarlo.
</details>

## Resumen

- **Observation** registra mediciones y hallazgos; su `code` dice qué es y
  su `value[x]`, el resultado.
- Los signos vitales siguen un **perfil** que exige categoría, código LOINC,
  paciente, fecha y unidades UCUM.
- Las mediciones de varias partes usan `component`.
- Los números van con punto y sin comillas.

## Ejecutar este módulo

- **Postman:** carpeta *06 · Observaciones*.
- **curl:** `curl/taller.sh 06`
- **R:**

  ```r
  signos <- fhir_buscar("Observation?subject=Patient/{{patientId}}&category=vital-signs")
  fhir_tabla(signos, list(
    signo  = function(r) r$code$text,
    valor  = function(r) r$valueQuantity$value %||% paste(
      vapply(r$component, function(c) format(c$valueQuantity$value), ""), collapse = "/"),
    unidad = function(r) r$valueQuantity$unit %||% "mmHg"
  ))
  ```
