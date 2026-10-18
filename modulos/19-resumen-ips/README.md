# Módulo 19 · Resumen del paciente (IPS)

[← Módulo 18](../18-terminologias-y-perfiles/README.md) · [Inicio](../../README.md)

> **Nivel:** avanzado · **Duración:** 90 minutos · **Necesitas:** módulos 01 a 18

## Lo que vas a aprender

1. Qué es el **IPS** (*International Patient Summary*) y para qué sirve.
2. Qué **secciones** tiene y cuáles son obligatorias.
3. A armar el IPS de Luis con lo que registraste en todo el taller.
4. A pedirle al servidor que arme el documento (`$document`) y a revisarlo.
5. A **validar contra una guía de implementación** real.

## La historia

En febrero de 2026, Luis va a viajar a visitar a su hija, que estudia en el
exterior. El Dr. Ruiz le prepara un **resumen de su historia clínica** para
llevar: si necesita atención allá, cualquier médico debe poder ver en
minutos lo esencial, en un formato que su sistema entienda. Ese resumen es
el **IPS**.

---

## Qué es el IPS

El **Resumen Internacional del Paciente** es un documento clínico **mínimo**
y **no específico de una especialidad**, pensado para la atención **no
planificada** y **transfronteriza**: un viajero que llega a urgencias, un
paciente que cambia de país, una consulta en otro sistema de salud. Responde
a "¿qué necesito saber de esta persona para atenderla con seguridad?".

- Es una **guía de implementación de HL7 FHIR** (`hl7.fhir.uv.ips`), con la
  norma ISO 27269 como referencia de contenido.
- Técnicamente es un **Bundle de tipo `document`** (módulo 09) cuya
  Composition sigue el perfil `Composition-uv-ips`, y cuyos recursos siguen
  los perfiles IPS (Patient, AllergyIntolerance, Condition...).
- Usa terminologías internacionales (SNOMED CT, LOINC) para que se entienda
  en cualquier país.

Guía oficial: <https://hl7.org/fhir/uv/ips/>. En este taller usamos la
versión **1.1.0**.

## Ficha: las secciones del IPS

Cada sección es un `Composition.section` con un código LOINC fijo. Estas son
las 14 que define el perfil `Composition-uv-ips` (versión 1.1.0):

| Sección | LOINC | Card. | En el IPS de Luis |
|---|---|---|---|
| **Medicación** | `10160-0` | **1..1** | Losartán (módulo 07) |
| **Alergias e intolerancias** | `48765-2` | **1..1** | Penicilina (módulo 07) |
| **Problemas** | `11450-4` | **1..1** | Cáncer de mama (módulo 11) |
| Procedimientos | `47519-4` | 0..1 | Mastectomía parcial (módulo 13) |
| Vacunas | `11369-6` | 0..1 | Influenza y Td (módulo 08) |
| Dispositivos médicos | `46264-8` | 0..1 | — |
| Resultados | `30954-2` | 0..1 | Informe de patología (módulo 11) |
| Signos vitales | `8716-3` | 0..1 | — |
| Antecedentes de enfermedades pasadas | `11348-0` | 0..1 | Intoxicación alimentaria (módulo 05) |
| Estado funcional | `47420-5` | 0..1 | — |
| Plan de cuidados | `18776-5` | 0..1 | Plan del comité (módulo 12) |
| Historia social | `29762-2` | 0..1 | — |
| Embarazos | `10162-6` | 0..1 | — |
| Directivas anticipadas | `42348-3` | 0..1 | — |

Las tres primeras son **obligatorias**. La guía recomienda además
procedimientos, vacunas, dispositivos y resultados. El resto es opcional.

**Si no hay datos, se dice.** Una sección obligatoria no puede omitirse: si
el paciente no tiene alergias conocidas, la sección lleva un recurso que lo
afirma (*no known allergies*), o un `emptyReason` que explica por qué no hay
información. "No hay alergias" y "no sabemos si hay alergias" son cosas muy
distintas para quien atiende.

Cada sección lleva **narrativa** (`section.text`) además de las referencias:
el médico que no tiene un sistema compatible igual puede leer el resumen.

---

## Paso a paso: la Composition del IPS

Primero se arma la Composition **en el servidor**, apuntando a los recursos
que ya existen allí (como en el módulo 09).

### Paso 1 · El mínimo: estado, tipo, paciente, fecha, autor y título

<!-- paso 19a 1 -->
```json
{
  "resourceType": "Composition",
  "status": "final",
  "type": {
    "coding": [
      {
        "system": "http://loinc.org",
        "code": "60591-5",
        "display": "Patient summary Document"
      }
    ],
    "text": "Resumen del paciente"
  },
  "subject": {
    "reference": "Patient/{{patientId}}",
    "display": "Luis Alberto Paredes Cevallos"
  },
  "date": "2026-02-15T10:00:00-05:00",
  "author": [
    {
      "reference": "PractitionerRole/{{oncologistRoleId}}",
      "display": "Dr. Ruiz · Oncología clínica"
    }
  ],
  "title": "Resumen internacional del paciente"
}
```
<!-- /paso -->

El tipo es LOINC `60591-5`, *Patient summary Document*: es lo que hace que la
Composition sea un IPS. El autor es el rol del oncólogo (módulo 10).

### Paso 2 · Identificador, confidencialidad y custodio

<!-- paso 19a 2 -->
```json
{
  "identifier": {
    "system": "https://f-slg.github.io/aprende-fhir/sid/documento",
    "value": "IPS-2026-0001"
  },
  "confidentiality": "N",
  "custodian": {
    "reference": "Organization/{{hospitalId}}",
    "display": "Hospital General Docente Ejemplo"
  }
}
```
<!-- /paso -->

`confidentiality: N` (*normal*) es el nivel habitual de la información
clínica.

### Paso 3 · Las tres secciones obligatorias: problemas, alergias y medicación

<!-- paso 19a 3 -->
```json
{
  "section": [
    {
      "title": "Problemas activos",
      "code": {
        "coding": [
          {
            "system": "http://loinc.org",
            "code": "11450-4",
            "display": "Problem list - Reported"
          }
        ]
      },
      "text": {
        "status": "generated",
        "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><p>Carcinoma ductal infiltrante de mama izquierda (activo, desde mayo de 2025).</p></div>"
      },
      "entry": [
        {
          "reference": "Condition/{{conditionCancerId}}",
          "display": "Carcinoma ductal infiltrante de mama izquierda"
        }
      ]
    },
    {
      "title": "Alergias e intolerancias",
      "code": {
        "coding": [
          {
            "system": "http://loinc.org",
            "code": "48765-2",
            "display": "Allergies and adverse reactions Document"
          }
        ]
      },
      "text": {
        "status": "generated",
        "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><p>Alergia a la penicilina, criticidad alta: urticaria generalizada.</p></div>"
      },
      "entry": [
        {
          "reference": "AllergyIntolerance/{{allergyId}}",
          "display": "Alergia a la penicilina"
        }
      ]
    },
    {
      "title": "Medicación",
      "code": {
        "coding": [
          {
            "system": "http://loinc.org",
            "code": "10160-0",
            "display": "History of Medication use Narrative"
          }
        ]
      },
      "text": {
        "status": "generated",
        "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><p>Losartán 50 mg por vía oral una vez al día (hipertensión arterial).</p></div>"
      },
      "entry": [
        {
          "reference": "MedicationStatement/{{medStatementId}}",
          "display": "Losartán 50 mg diarios"
        }
      ]
    }
  ]
}
```
<!-- /paso -->

Cada sección tiene título, código LOINC, narrativa y sus `entry`.

### Paso 4 · Las secciones recomendadas y la narrativa

<!-- paso 19a 4 -->
```json
{
  "section": [
    {
      "title": "Problemas activos",
      "code": {
        "coding": [
          {
            "system": "http://loinc.org",
            "code": "11450-4",
            "display": "Problem list - Reported"
          }
        ]
      },
      "text": {
        "status": "generated",
        "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><p>Carcinoma ductal infiltrante de mama izquierda (activo, desde mayo de 2025).</p></div>"
      },
      "entry": [
        {
          "reference": "Condition/{{conditionCancerId}}",
          "display": "Carcinoma ductal infiltrante de mama izquierda"
        }
      ]
    },
    {
      "title": "Alergias e intolerancias",
      "code": {
        "coding": [
          {
            "system": "http://loinc.org",
            "code": "48765-2",
            "display": "Allergies and adverse reactions Document"
          }
        ]
      },
      "text": {
        "status": "generated",
        "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><p>Alergia a la penicilina, criticidad alta: urticaria generalizada.</p></div>"
      },
      "entry": [
        {
          "reference": "AllergyIntolerance/{{allergyId}}",
          "display": "Alergia a la penicilina"
        }
      ]
    },
    {
      "title": "Medicación",
      "code": {
        "coding": [
          {
            "system": "http://loinc.org",
            "code": "10160-0",
            "display": "History of Medication use Narrative"
          }
        ]
      },
      "text": {
        "status": "generated",
        "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><p>Losartán 50 mg por vía oral una vez al día (hipertensión arterial).</p></div>"
      },
      "entry": [
        {
          "reference": "MedicationStatement/{{medStatementId}}",
          "display": "Losartán 50 mg diarios"
        }
      ]
    },
    {
      "title": "Vacunas",
      "code": {
        "coding": [
          {
            "system": "http://loinc.org",
            "code": "11369-6",
            "display": "History of Immunization note"
          }
        ]
      },
      "text": {
        "status": "generated",
        "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><p>Influenza estacional (3 de abril de 2025).</p><p>Td, refuerzo (3 de abril de 2025).</p></div>"
      },
      "entry": [
        {
          "reference": "Immunization/{{fluImmunizationId}}",
          "display": "Influenza, 3 de abril de 2025"
        },
        {
          "reference": "Immunization/{{tdImmunizationId}}",
          "display": "Td, 3 de abril de 2025"
        }
      ]
    },
    {
      "title": "Procedimientos",
      "code": {
        "coding": [
          {
            "system": "http://loinc.org",
            "code": "47519-4",
            "display": "History of Procedures Document"
          }
        ]
      },
      "text": {
        "status": "generated",
        "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><p>Mastectomía parcial de mama izquierda (10 de junio de 2025), exitosa.</p></div>"
      },
      "entry": [
        {
          "reference": "Procedure/{{procedureId}}",
          "display": "Mastectomía parcial"
        }
      ]
    },
    {
      "title": "Resultados",
      "code": {
        "coding": [
          {
            "system": "http://loinc.org",
            "code": "30954-2",
            "display": "Relevant diagnostic tests/laboratory data note"
          }
        ]
      },
      "text": {
        "status": "generated",
        "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><p>Anatomía patológica: carcinoma ductal infiltrante de 3,5 cm, receptor de estrógeno positivo (Allred 8).</p></div>"
      },
      "entry": [
        {
          "reference": "DiagnosticReport/{{diagnosticReportId}}",
          "display": "Informe de patología"
        }
      ]
    },
    {
      "title": "Plan de tratamiento",
      "code": {
        "coding": [
          {
            "system": "http://loinc.org",
            "code": "18776-5",
            "display": "Plan of care note"
          }
        ]
      },
      "text": {
        "status": "generated",
        "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><p>Plan del comité de tumores: cirugía, quimioterapia (4 ciclos) y hormonoterapia;</p><p>tamoxifeno suspendido en febrero de 2026 por intolerancia.</p></div>"
      },
      "entry": [
        {
          "reference": "CarePlan/{{carePlanId}}",
          "display": "Plan de tratamiento del cáncer de mama"
        }
      ]
    },
    {
      "title": "Antecedentes",
      "code": {
        "coding": [
          {
            "system": "http://loinc.org",
            "code": "11348-0",
            "display": "History of Past illness note"
          }
        ]
      },
      "text": {
        "status": "generated",
        "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><p>Intoxicación alimentaria bacteriana (marzo de 2025), resuelta.</p></div>"
      },
      "entry": [
        {
          "reference": "Condition/{{conditionIntoxId}}",
          "display": "Intoxicación alimentaria"
        }
      ]
    }
  ],
  "text": {
    "status": "generated",
    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><p>Resumen internacional del paciente (IPS) de Luis Alberto Paredes Cevallos,</p><p>emitido el 15 de febrero de 2026 por el servicio de Oncología Clínica.</p></div>"
  }
}
```
<!-- /paso -->

Vacunas, procedimientos, resultados, plan de cuidados y antecedentes.
Solución: [`19a_composition_ips.json`](soluciones/19a_composition_ips.json).

---

## Ejercicios en el servidor

### 19a · Guardar la Composition

```http
POST {{FHIRURL}}/Composition        → compositionIpsId
```

### 19b · El servidor arma el documento: `$document`

```http
GET {{FHIRURL}}/Composition/{{compositionIpsId}}/$document
```

La operación `$document` arma un **Bundle de tipo `document`** con la
Composition y todos los recursos a los que apunta, y los que apuntan esos,
hasta completar el documento. Para el IPS de Luis, HAPI devuelve **29
entradas**: además de las secciones trae, por ejemplo, el hospital, los
encuentros y la muestra de la biopsia, porque los recursos de las secciones
los referencian.

Revisa el Bundle que devuelve: **no tiene `identifier` ni `timestamp`**, y la
especificación los exige en todo documento (reglas `bdl-9` y `bdl-10`). Que
el servidor arme un documento no garantiza que esté completo: **valídalo**
antes de enviarlo a otro sistema.

### 19c y 19d · El IPS autocontenido

Para un IPS que viaje a otro país conviene armar el Bundle con cuidado:

- copias de los recursos **dentro** del Bundle, enlazados con `urn:uuid:`;
- **solo** lo que el resumen necesita: se quitan las referencias a
  encuentros, órdenes, muestras o profesionales que no forman parte del
  resumen;
- `identifier` y `timestamp` del documento.

El resultado tiene **14 recursos**: la Composition, el paciente, el oncólogo y
su rol, el hospital, los dos diagnósticos, la alergia, el losartán, las dos
vacunas, la cirugía, el informe de patología y el plan
([`19b_bundle_ips.json`](soluciones/19b_bundle_ips.json)).

```http
POST {{FHIRURL}}/Bundle             → bundleIpsId
GET  {{FHIRURL}}/Bundle/{{bundleIpsId}}
```

### Validar contra la guía IPS

Este es el paso que de verdad importa: comprobar que el IPS cumple la
**guía de implementación**, no solo la especificación base. El validador
oficial descarga la guía del registro de paquetes de HL7:

```bash
java -jar validator_cli.jar -version 4.0.1 \
  -ig hl7.fhir.uv.ips#1.1.0 \
  -profile http://hl7.org/fhir/uv/ips/StructureDefinition/Bundle-uv-ips \
  modulos/19-resumen-ips/soluciones/19b_bundle_ips.json
```

El IPS de Luis pasa **sin errores**. `herramientas/validar.sh` hace esta
validación automáticamente en cada cambio del taller.

Mientras se armaba este módulo, el validador encontró problemas que vale la
pena conocer:

- **Nombres de LOINC actualizados.** LOINC renombró los códigos de algunas
  secciones. Por ejemplo, `11369-6` se llamaba *History of Immunization
  Narrative* y hoy es *History of Immunization note*. El validador consulta el
  nombre vigente.
- **Bloques incompletos.** Al quitar del resumen a la enfermera que vacunó,
  quedaba un `performer` sin `actor`, que es obligatorio. La solución fue
  quitar el bloque completo, no solo la referencia.

### 19e y 19f · Error a propósito: un IPS sin alergias

[`19e1_ips_sin_alergias.json`](errores/19e1_ips_sin_alergias.json) es el
mismo IPS sin la sección de alergias. **El servidor lo acepta**: para él es un
Bundle cualquiera. La especificación base también lo acepta. Solo la guía
IPS lo detecta, y su mensaje hay que aprender a leerlo. Al validar el Bundle:

```
Bundle | Slice 'Bundle.entry:composition': a matching slice is required, but not found (from …/Bundle-uv-ips|1.1.0)
```

Dice que el Bundle **no tiene una Composition que cumpla el perfil IPS**, pero
no dice por qué. Para saberlo, se valida la Composition sola contra
`Composition-uv-ips`, y el primer error es el que buscamos:

```
Composition | Slice 'Composition.section:sectionAllergies': a matching slice is required, but not found
```

(Validada fuera del Bundle, la Composition muestra además errores en las
`entry` de otras secciones: no son reales, aparecen porque sus referencias
`urn:uuid:` solo se resuelven dentro del Bundle.)

En un IPS, la ausencia de la sección de alergias podría hacer creer al
médico que el paciente no tiene alergias. Por eso la guía la exige. Bórralo
con `DELETE {{FHIRURL}}/Bundle/{{errorIpsId}}`.

### 19g · El expediente completo

```http
GET {{FHIRURL}}/Patient/{{patientId}}/$everything
```

Después de los 19 módulos, el expediente de Luis tiene **29 tipos de
recursos**: de su primera consulta por una intoxicación hasta el resumen que
lleva de viaje. Compáralo con el IPS: el expediente tiene **todo**; el IPS,
**lo esencial**.

## Para pensar

Luis llega a urgencias en otro país con un código QR que lleva a su IPS.
¿Qué tres datos del resumen mirarías primero? ¿Qué pasaría si la sección de
medicación incluyera el tamoxifeno suspendido sin aclarar su estado? Piensa
en por qué cada recurso tiene `status`.

## Autoevaluación

<details><summary>1. ¿Cuáles son las tres secciones obligatorias del IPS?</summary>

Medicación (`10160-0`), alergias e intolerancias (`48765-2`) y problemas
(`11450-4`).
</details>

<details><summary>2. Un paciente no tiene alergias conocidas. ¿Se omite la sección?</summary>

No. Se incluye con un recurso que afirma que no hay alergias conocidas, o con
un `emptyReason`. Omitirla no permite distinguir "no tiene" de "no sabemos".
</details>

<details><summary>3. El documento que devolvió <code>$document</code>, ¿se puede enviar tal cual?</summary>

No sin revisarlo: le faltan el `identifier` y el `timestamp` que exige todo
documento, y trae recursos que el resumen no necesita. Hay que completarlo y
validarlo.
</details>

<details><summary>4. ¿Por qué el error del IPS sin alergias no lo detecta la especificación base?</summary>

Porque para la base es un documento válido: es la **guía IPS** la que exige
esa sección. Por eso se valida contra el perfil de la guía, no solo contra
FHIR.
</details>

## Resumen

- El **IPS** es un resumen mínimo para atención no planificada y entre
  países: un Bundle `document` que sigue la guía `hl7.fhir.uv.ips`.
- Medicación, alergias y problemas son obligatorias; si no hay datos, se
  declara.
- `$document` arma el documento en el servidor, pero hay que completarlo y
  validarlo.
- Validar contra la **guía de implementación** detecta lo que la base no ve.

## Cierre del taller

Recorriste **33 tipos de recursos** siguiendo a una persona durante casi un
año: la registraste, la atendiste, le pediste estudios, la operaste, la
trataste, la seguiste y, al final, resumiste su historia para que viaje con
ella. En el camino aprendiste a leer la especificación, a codificar con
terminologías internacionales, a buscar, a corregir sin perder la historia,
a escribir un perfil y a validar contra una guía real.

Ideas para seguir:

- Implementa uno de estos flujos en tu propio sistema o en R (el prototipo
  [Agenda FHIR](https://github.com/f-slg/agenda-fhir-r) es un ejemplo).
- Lee la guía IPS completa y las guías de otros países en
  <https://registry.fhir.org/>.
- Participa en la comunidad: <https://chat.fhir.org> y los grupos de
  trabajo de HL7.

## Ejecutar este módulo

- **Postman:** carpeta *19 · Resumen del paciente (IPS)*.
- **curl:** `curl/taller.sh` (todo el taller)
- **R:**

  ```r
  doc <- fhir_leer("Composition/{{compositionIpsId}}/$document")
  c(identifier = is.null(doc$identifier), timestamp = is.null(doc$timestamp))  # ¿faltan?
  ips <- jsonlite::fromJSON("modulos/19-resumen-ips/soluciones/19b_bundle_ips.json", simplifyVector = FALSE)
  vapply(ips$entry[[1]]$resource$section, function(s) s$title, "")
  ```
