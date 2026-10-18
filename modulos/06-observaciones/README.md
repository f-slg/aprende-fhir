# Módulo 06 · Observaciones: signos vitales y tipos de valor

[← Módulo 05](../05-diagnostico-y-encuentro/README.md) · [Inicio](../../README.md) · [Módulo 07 →](../07-documentos-clinicos/README.md)

## Objetivos

- Registrar signos vitales según el **perfil de signos vitales** de FHIR R4.
- Usar los distintos tipos de valor de `Observation` (`value[x]`).
- Modelar mediciones con varias partes usando `component`.

## El caso

En la consulta del 20 de marzo, a las 07:30, se registra: presión arterial
128/84 mmHg, temperatura 38,4 °C, frecuencia respiratoria 20/min y frecuencia
cardíaca 102/min. Además: fiebre presente, el motivo de consulta, sangre oculta
en heces positiva y una reacción de Widal con título 1:160.

## Conceptos clave

- **`Observation`** es el recurso más usado de FHIR: signos vitales,
  resultados de laboratorio, escalas, hallazgos del examen físico...
- **Perfil de signos vitales**: FHIR R4 exige que cada signo vital tenga
  `category = vital-signs`, un código **LOINC** concreto y un valor en
  unidades **UCUM**. Por ejemplo: presión arterial `85354-9`, temperatura
  `8310-5`, frecuencia respiratoria `9279-1`, frecuencia cardíaca `8867-4`.
- **`component`**: la presión arterial no es un valor sino dos (sistólica
  `8480-6` y diastólica `8462-4`). No se usa `valueRatio` ni un texto
  "128/84": son dos componentes con su propio código y valor.
- **`value[x]`**: el valor puede ser de distintos tipos. El nombre del campo
  cambia según el tipo.

| Ejercicio | Tipo | Campo |
|---|---|---|
| Temperatura, frecuencias | Cantidad con unidad | `valueQuantity` |
| Fiebre | Sí / no | `valueBoolean` |
| Motivo de consulta | Texto libre | `valueString` |
| Sangre oculta | Concepto codificado | `valueCodeableConcept` |
| Título de Widal | Proporción | `valueRatio` |

- **UCUM**: en `valueQuantity`, `unit` es lo que ve la persona (`°C`) y `code`
  lo que entiende la máquina (`Cel`). Los códigos UCUM distinguen mayúsculas.

## Ejercicios

### 06a a 06d · Signos vitales

Registra los cuatro signos vitales, enlazados al paciente y al **encuentro**
del módulo 05.

Soluciones: [`06a` presión arterial](soluciones/06a_observation_presion_arterial.json) ·
[`06b` temperatura](soluciones/06b_observation_temperatura.json) ·
[`06c` frecuencia respiratoria](soluciones/06c_observation_frecuencia_respiratoria.json) ·
[`06d` frecuencia cardíaca](soluciones/06d_observation_frecuencia_cardiaca.json)

### 06e a 06h · Otros tipos de valor

Soluciones: [`06e` fiebre](soluciones/06e_observation_fiebre_boolean.json) ·
[`06f` motivo de consulta](soluciones/06f_observation_motivo_string.json) ·
[`06g` sangre oculta](soluciones/06g_observation_sangre_oculta_codeable.json) ·
[`06h` título de Widal](soluciones/06h_observation_titulo_ratio.json)

### 06i · Buscar los signos vitales

```http
GET {{FHIRURL}}/Observation?subject=Patient/{{patientId}}&category=vital-signs
```

### Reto: codificar el título de Widal

La observación `06h` solo tiene `code.text`. Busca en
[loinc.org](https://loinc.org/search/) el código LOINC del título de
anticuerpos contra el antígeno O de *Salmonella typhi* en suero, agrégalo como
`coding` y valida el recurso (ver *Validar tus recursos* en el inicio).

## Para pensar

Para la fiebre usamos SNOMED CT (`386661006`, *Fever*) con `valueBoolean`. ¿No
sería suficiente con la temperatura? ¿Cuándo tiene sentido registrar el
hallazgo además de la medición?

## Ejecutar este módulo

- **Postman:** carpeta *06 · Observaciones*.
- **curl:** `curl/taller.sh 06`
- **R:**

  ```r
  signos <- fhir_buscar("Observation?subject=Patient/{{patientId}}&category=vital-signs")
  fhir_tabla(signos, list(
    signo = function(r) r$code$text,
    valor = function(r) r$valueQuantity$value,
    unidad = function(r) r$valueQuantity$unit
  ))
  ```
