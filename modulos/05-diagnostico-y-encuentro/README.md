# Módulo 05 · Diagnóstico y encuentro

[← Módulo 04](../04-profesionales-y-organizaciones/README.md) · [Inicio](../../README.md) · [Módulo 06 →](../06-observaciones/README.md)

## Objetivos

- Registrar un diagnóstico con `Condition` y usar terminologías (CIE-10 y
  SNOMED CT).
- Registrar una atención con `Encounter`.
- Traer recursos relacionados en una sola búsqueda con `_include`.

## El caso

El 17 de marzo de 2025 Luis empieza con dolor abdominal, náuseas, vómito y
diarrea. El 20 de marzo consulta en el hospital: la Dra. Salazar diagnostica
una **intoxicación alimentaria bacteriana**, de severidad moderada, que se
resuelve el 24 de marzo.

## Conceptos clave

- **`CodeableConcept`**: un concepto con uno o varios `coding` (sistema +
  código + nombre) y un `text` libre. Es el tipo más usado en FHIR para todo
  lo que se codifica.
- **Terminologías**: el diagnóstico usa **CIE-10** (`A05.9`), la severidad y
  los síntomas usan **SNOMED CT**. El `display` debe ser el nombre oficial del
  código: el validador lo verifica.
- **`Condition`** tiene dos estados distintos: `clinicalStatus` (activa,
  resuelta...) y `verificationStatus` (confirmada, provisional...).
- **`Encounter`** es la atención: su `class` (`AMB` ambulatoria), el periodo,
  quién atendió (`participant`) y qué se diagnosticó (`diagnosis`).

## Ejercicios

### 05a · El diagnóstico

Registra la condición con su código CIE-10, la severidad, el inicio y la
resolución, y los cuatro síntomas como `evidence`.

Solución: [`05a_condition_intoxicacion.json`](soluciones/05a_condition_intoxicacion.json)

<details><summary>Pista</summary>

Busca los códigos en el [buscador de SNOMED CT](https://browser.ihtsdotools.org/)
y en la [CIE-10 de la OMS](https://icd.who.int/browse10/2019/en). El sistema de
CIE-10 en FHIR es `http://hl7.org/fhir/sid/icd-10`.
</details>

### 05b · El encuentro

La consulta fue el 20 de marzo de 2025, de 07:15 a 08:15 (hora de Ecuador,
`-05:00`). Enlázala con el paciente, la médica, el hospital
(`serviceProvider`) y el diagnóstico.

Solución: [`05b_encounter_crear.json`](soluciones/05b_encounter_crear.json)

### 05c · Todo junto

```http
GET {{FHIRURL}}/Encounter?subject=Patient/{{patientId}}&_include=Encounter:diagnosis
```

`_include` agrega al resultado las condiciones a las que apunta cada
encuentro. Fíjate en `entry.search.mode`: `match` o `include`.

## Para pensar

¿El diagnóstico debería apuntar al encuentro, o el encuentro al diagnóstico?
En FHIR R4 existen las dos referencias (`Condition.encounter` y
`Encounter.diagnosis`). ¿Qué ventajas tiene cada una?

## Ejecutar este módulo

- **Postman:** carpeta *05 · Diagnóstico y encuentro*.
- **curl:** `curl/taller.sh 05`
- **R:** `fhir_crear("Encounter", "modulos/05-diagnostico-y-encuentro/soluciones/05b_encounter_crear.json", guarda = "encounterId")`
