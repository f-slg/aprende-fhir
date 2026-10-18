# Módulo 09 · Documentos clínicos

[← Módulo 08](../08-vacunacion/README.md) · [Inicio](../../README.md) · [Módulo 11 →](../11-anatomia-patologica/README.md)

> **Nivel:** intermedio · **Duración:** 60 minutos · **Necesitas:** módulo 06

## Lo que vas a aprender

1. La diferencia entre **recursos sueltos** y un **documento clínico**.
2. Qué es **Composition** y cómo organiza un documento en secciones.
3. A armar un **Bundle de tipo `document`**, autocontenido e inmutable.

## La historia

Luis va a acudir a un control en otro centro de salud, que no tiene acceso
al servidor del hospital. La Dra. Salazar prepara una **nota de signos
vitales** de la consulta del 20 de marzo: un documento que Luis puede llevar
y que debe leerse completo en cualquier sistema, sin consultar nada más.

---

## Recursos sueltos frente a documentos

Hasta ahora cada recurso vive por separado en el servidor: se puede leer,
buscar y **cambiar**. Un documento es otra cosa:

| | Recursos en el servidor | Documento |
|---|---|---|
| ¿Cambia? | Sí, con `PUT` (nuevas versiones) | **No**: se emite una vez |
| ¿Quién responde? | Cada recurso por separado | Un **autor** que firma el conjunto |
| ¿Se lee fuera del servidor? | Hay que seguir las referencias | Sí: lleva **todo** dentro |
| Ejemplos | La lista de problemas de hoy | Epicrisis, informe, certificado, resumen del paciente |

## Ficha del recurso: Composition

**¿Qué es?** El **índice** de un documento clínico: de qué tipo es, quién lo
escribió, cuándo, sobre quién, y sus **secciones**, cada una con su texto y
las referencias a los recursos que la sustentan.

**¿Para qué se usa?** Para construir documentos: epicrisis, notas de
evolución, informes de alta, resúmenes como el **IPS** (módulo 19).

**¿Cuándo usar otro recurso?** Para un documento que ya existe como archivo
(un PDF escaneado, una imagen): **DocumentReference**.

**Elementos principales** (<https://hl7.org/fhir/R4/composition.html>):

<!-- ficha Composition -->
| Elemento | Card. | Tipo | Para qué sirve |
|---|---|---|---|
| `identifier` | 0..1 | Identifier | Identificador del documento. |
| `status` ⚑ | **1..1** | code | `preliminary`, `final`, `amended` o `entered-in-error`. |
| `type` | **1..1** | CodeableConcept | Qué documento es: un código LOINC de documento. |
| `category` | 0..* | CodeableConcept | Clase de documento. |
| `subject` | 0..1 | Reference(Resource) | Sobre quién trata. |
| `encounter` | 0..1 | Reference(Encounter) | De qué atención. |
| `date` | **1..1** | dateTime | Cuándo se escribió. |
| `author` | **1..*** | Reference(Practitioner \| PractitionerRole \| Device \| Patient \| …) | Quién lo escribió. |
| `title` | **1..1** | string | Título. |
| `confidentiality` | 0..1 | code | Nivel de confidencialidad. |
| `attester` | 0..* | BackboneElement | Quién lo certifica o firma. |
| `custodian` | 0..1 | Reference(Organization) | La organización que lo custodia. |
| `relatesTo` | 0..* | BackboneElement | Otros documentos a los que reemplaza o complementa. |
| `section` | 0..* | BackboneElement | Las secciones. |
| `section.title` | 0..1 | string | Título de la sección. |
| `section.code` | 0..1 | CodeableConcept | Qué sección es. |
| `section.text` | 0..1 | Narrative | El texto de la sección para personas. |
| `section.entry` | 0..* | Reference(Resource) | Los recursos que contiene la sección. |
<!-- /ficha -->

---

## Paso a paso: la composición

### Paso 1 · El mínimo: estado, tipo, fecha, autor y título

<!-- paso 09a 1 -->
```json
{
  "resourceType": "Composition",
  "status": "final",
  "type": {
    "coding": [
      {
        "system": "http://loinc.org",
        "code": "8716-3",
        "display": "Vital signs note"
      }
    ],
    "text": "Nota de signos vitales"
  },
  "date": "2025-03-20T08:00:00-05:00",
  "author": [
    {
      "reference": "Practitioner/{{practitionerId}}",
      "display": "Dra. Andrea Lucía Salazar Moreno"
    }
  ],
  "title": "Signos vitales - consulta del 20 de marzo de 2025"
}
```
<!-- /paso -->

Cinco elementos obligatorios. El tipo de documento es LOINC `8716-3`,
*Vital signs note*.

### Paso 2 · De quién y de qué consulta

<!-- paso 09a 2 -->
```json
{
  "subject": {
    "reference": "Patient/{{patientId}}",
    "display": "Luis Alberto Paredes Cevallos"
  },
  "encounter": {
    "reference": "Encounter/{{encounterId}}",
    "display": "Consulta por dolor abdominal"
  },
  "custodian": {
    "reference": "Organization/{{hospitalId}}",
    "display": "Hospital General Docente Ejemplo"
  }
}
```
<!-- /paso -->

### Paso 3 · La sección con los signos vitales

<!-- paso 09a 3 -->
```json
{
  "section": [
    {
      "title": "Signos vitales",
      "code": {
        "coding": [
          {
            "system": "http://loinc.org",
            "code": "8716-3",
            "display": "Vital signs note"
          }
        ],
        "text": "Nota de signos vitales"
      },
      "text": {
        "status": "generated",
        "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><p>Presión arterial 128/84 mmHg; Temperatura 38,4 °C; Frecuencia respiratoria 20/min; Frecuencia cardíaca 102/min.</p></div>"
      },
      "entry": [
        {
          "reference": "Observation/{{obsPAId}}",
          "display": "Presión arterial 128/84 mmHg"
        },
        {
          "reference": "Observation/{{obsTempId}}",
          "display": "Temperatura 38,4 °C"
        },
        {
          "reference": "Observation/{{obsFRId}}",
          "display": "Frecuencia respiratoria 20/min"
        },
        {
          "reference": "Observation/{{obsFCId}}",
          "display": "Frecuencia cardíaca 102/min"
        }
      ]
    }
  ]
}
```
<!-- /paso -->

`section.text` es lo que leerá una persona; `section.entry` apunta a las
cuatro observaciones del módulo 06. Las dos cosas deben decir lo mismo.

### Paso 4 · Identificador y narrativa

<!-- paso 09a 4 -->
```json
{
  "identifier": {
    "system": "https://f-slg.github.io/aprende-fhir/sid/documento",
    "value": "DOC-2025-0001"
  },
  "text": {
    "status": "generated",
    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><p>Nota de signos vitales del 20 de marzo de 2025.</p><p>Presión arterial 128/84 mmHg; Temperatura 38,4 °C; Frecuencia respiratoria 20/min; Frecuencia cardíaca 102/min.</p></div>"
  }
}
```
<!-- /paso -->

Solución: [`09a_composition_signos_vitales.json`](soluciones/09a_composition_signos_vitales.json).

## El documento autocontenido: Bundle `document`

Una Composition guardada en el servidor sigue apuntando a recursos que
pueden cambiar. Para que el documento sea **autocontenido e inmutable** se
arma un **Bundle de tipo `document`**:

1. El **primer** `entry` es la Composition.
2. Después van **todos** los recursos a los que apunta: el paciente, la
   autora, el hospital custodio y las cuatro observaciones.
3. Las referencias usan `urn:uuid:` **dentro del Bundle**, no `id` del
   servidor: `"subject": {"reference": "urn:uuid:…"}`.
4. El Bundle lleva `identifier` y `timestamp`, obligatorios en un documento.

```json
{
  "resourceType": "Bundle",
  "identifier": { "system": "https://f-slg.github.io/aprende-fhir/sid/documento", "value": "DOC-2025-0002" },
  "type": "document",
  "timestamp": "2025-03-20T08:05:00-05:00",
  "entry": [
    { "fullUrl": "urn:uuid:…", "resource": { "resourceType": "Composition", … } },
    { "fullUrl": "urn:uuid:…", "resource": { "resourceType": "Patient", … } },
    …
  ]
}
```

Solución completa: [`09b_bundle_document_signos_vitales.json`](soluciones/09b_bundle_document_signos_vitales.json).
Ábrela y sigue una referencia: el `subject` de la Composition apunta a un
`urn:uuid:` que es el `fullUrl` del Patient del mismo Bundle.

---

## Ejercicios en el servidor

### 09a · Guardar la composición

```http
POST {{FHIRURL}}/Composition        → compositionId
```

### 09b · Guardar el documento

```http
POST {{FHIRURL}}/Bundle             → bundleDocId
```

Fíjate en la ruta: `/Bundle`, no la raíz. A la raíz se envían las
transacciones (módulo 03), que el servidor **separa** en recursos. En
`/Bundle` el documento se guarda **entero**, como un solo recurso.

### 09c · Leerlo

```http
GET {{FHIRURL}}/Bundle/{{bundleDocId}}
```

Compáralo con la búsqueda del módulo 06: ¿qué diferencia hay entre el
`searchset` de entonces y este `document`?

## Autoevaluación

<details><summary>1. Mañana se corrige la presión arterial de Luis con <code>PUT</code>. ¿Cambia el documento?</summary>

No. El documento lleva su propia copia de las observaciones. Así debe ser: un
documento firmado no cambia; si hay un error, se emite uno nuevo que
reemplaza al anterior (`relatesTo`).
</details>

<details><summary>2. ¿Qué entrada va primero en un Bundle document?</summary>

La Composition. Después, todos los recursos a los que se refiere.
</details>

<details><summary>3. ¿Por qué se usan <code>urn:uuid:</code> en lugar de <code>Patient/1006</code>?</summary>

Porque el documento debe poder leerse fuera del servidor. `Patient/1006`
solo tiene sentido en ese servidor; el `urn:uuid:` apunta a una entrada del
propio Bundle.
</details>

## Resumen

- Un **documento** es un conjunto inmutable firmado por un autor.
- **Composition** es su índice: tipo, autor, fecha y secciones.
- El **Bundle `document`** lleva la Composition primero y todo lo demás
  dentro, enlazado con `urn:uuid:`.
- Las transacciones van a la raíz; los documentos, a `/Bundle`.

## Ejecutar este módulo

- **Postman:** carpeta *09 · Documentos clínicos*.
- **curl:** `curl/taller.sh 09`
- **R:**

  ```r
  doc <- fhir_crear("Bundle", "modulos/09-documentos-clinicos/soluciones/09b_bundle_document_signos_vitales.json",
                    guarda = "bundleDocId")
  vapply(doc$entry, function(e) e$resource$resourceType, "")
  ```
