# Módulo 10 · Medicamentos y cierre

[← Módulo 09](../09-procedimientos/README.md) · [Inicio](../../README.md)

## Objetivos

- Distinguir la **prescripción** (`MedicationRequest`) de la
  **administración** (`MedicationAdministration`).
- Calcular y justificar una dosis con una observación.
- Gestionar el ciclo de vida de una receta: activa → suspendida.
- Recuperar el expediente completo con `$everything`.

## El caso

**Quimioterapia.** El 1 de julio de 2025 se calcula la superficie corporal de
Luis: 1,77 m². La dosis de doxorrubicina es 60 mg/m² × 1,77 m² = **106,2 mg**
por vía intravenosa, cada 21 días, 4 ciclos. El primer ciclo se administra el
2 de julio. Dos horas después Luis presenta náuseas leves.

**Hormonoterapia.** Como el tumor es receptor de estrógeno positivo, el 15 de
octubre se prescribe **tamoxifeno** 20 mg diarios por vía oral durante 5 años.
Luis toma la primera dosis en casa al día siguiente. En febrero de 2026 se
suspende por intolerancia (sofocos y dolor articular).

## Conceptos clave

- **`MedicationRequest`**: la orden. Tiene `status` (`active`, `stopped`,
  `completed`...) e `intent` (`order`). La dosis se describe en
  `dosageInstruction`, con texto para personas y datos estructurados
  (`timing`, `route`, `doseAndRate`).
- **`MedicationAdministration`**: lo que realmente se administró, cuándo y
  quién. Se enlaza con la orden mediante `request`.
- **`category`** de la administración: `outpatient` (en el hospital, sin
  internación) o `community` (en casa, la hace el propio paciente: `performer`
  = `Patient`).
- **`supportingInformation`**: la superficie corporal que justifica la dosis.
- **Suspender** no es borrar: es `PUT` con `status = stopped` y el motivo en
  `statusReason`.

## Ejercicios

| Paso | Qué hacer | Solución |
|---|---|---|
| 10a | Superficie corporal 1,77 m² (LOINC `8277-6`) | [`10a`](soluciones/10a_observation_superficie_corporal.json) |
| 10b | Prescribir doxorrubicina 106,2 mg IV cada 21 días, 4 ciclos | [`10b`](soluciones/10b_medicationrequest_doxorrubicina.json) |
| 10c | Administrar el primer ciclo, enlazado con la orden | [`10c`](soluciones/10c_medicationadministration_doxorrubicina.json) |
| 10d | Agregar la nota del evento posterior (náuseas) | [`10d`](soluciones/10d_medicationadministration_actualizar.json) |
| 10e | Prescribir tamoxifeno 20 mg diarios por 5 años | [`10e`](soluciones/10e_medicationrequest_tamoxifeno.json) |
| 10f | Primera dosis autoadministrada en casa | [`10f`](soluciones/10f_medicationadministration_tamoxifeno.json) |
| 10g | Suspender el tamoxifeno por intolerancia | [`10g`](soluciones/10g_medicationrequest_suspender.json) |

### 10h · El expediente completo

```http
GET {{FHIRURL}}/Patient/{{patientId}}/$everything
```

`$everything` es una **operación** (empiezan con `$`): devuelve el paciente y
todo lo que se relaciona con él. Cuenta cuántos recursos de cada tipo creaste
durante el taller.

## Cierre: lo que aprendiste

Recorriste un caso completo, de la consulta por una intoxicación hasta el
tratamiento de un cáncer, con **15 tipos de recursos** enlazados: Patient,
Practitioner, Organization, Condition, Encounter, Observation, Composition,
Bundle, BodyStructure, Specimen, DiagnosticReport, Procedure,
MedicationRequest y MedicationAdministration, además de CapabilityStatement.

Siguientes pasos sugeridos:

- Explora `PractitionerRole`, `Location`, `Immunization` y `AllergyIntolerance`.
- Lee sobre **perfiles** y **guías de implementación**: así cada país o
  programa define cómo usar FHIR (por ejemplo, qué identificador es la cédula).
- Prueba **Agenda FHIR**, un prototipo en R y Shiny con Schedule, Slot y
  Appointment: <https://github.com/f-slg/agenda-fhir-r>.

## Ejecutar este módulo

- **Postman:** carpeta *10 · Medicamentos*.
- **curl:** `curl/taller.sh` (todo el taller)
- **R:**

  ```r
  todo <- fhir_leer("Patient/{{patientId}}/$everything?_count=100")
  table(vapply(todo$entry, function(e) e$resource$resourceType, ""))
  ```
