# Módulo 02 · Patient: crear, leer, buscar y actualizar

[← Módulo 01](../01-fundamentos/README.md) · [Inicio](../../README.md) · [Módulo 03 →](../03-transacciones/README.md)

## Objetivos

- Crear un recurso `Patient` completo y obtener el `id` que asigna el servidor.
- Leerlo, buscarlo por identificador y por nombre.
- Actualizarlo y ver su **historial de versiones**.

## El caso

**Luis Alberto Paredes Cevallos** nació el 12 de marzo de 1979 en Riobamba y
vive en Quito. Su cédula (ficticia) es `9900000017` y su historia clínica en el
hospital es `HC-000123`. *Todos los datos del taller son inventados; las
cédulas empiezan con `99`, un código de provincia que no existe.*

## Conceptos clave

- **`identifier`**: un paciente puede tener varios identificadores. Cada uno
  tiene un `system` (quién lo emite, como una URL) y un `value`. La pareja
  *system + value* debe ser única. En este taller los `system` son
  direcciones didácticas (`https://f-slg.github.io/aprende-fhir/sid/...`); en
  producción se usan las que defina la guía de implementación nacional.
- **`type` del identificador**: `NI` (identificador nacional) para la cédula,
  `MR` (historia clínica). Al validar verás un aviso porque `NI` no está en la
  lista sugerida por FHIR R4. Esa lista es *extensible*: se puede usar otro
  código cuando ninguno de la lista sirve. Es una buena lección sobre los
  tipos de *binding*.
- **Extensiones**: los dos apellidos se registran con las extensiones estándar
  `humanname-fathers-family` y `humanname-mothers-family`, y el lugar de
  nacimiento con `patient-birthPlace`.
- **`text`**: un resumen en HTML para personas. No reemplaza los datos
  estructurados, pero los sistemas lo muestran cuando no entienden el resto.

## Ejercicios

### 02a · Crear el paciente

Construye un `Patient` con: los dos identificadores, el nombre oficial (con
apellido paterno y materno) y el de uso habitual (*Luis Paredes*), sexo,
fecha de nacimiento, dirección en Quito, idioma español y lugar de
nacimiento. Envíalo con `POST {{FHIRURL}}/Patient` y anota el `id` que
devuelve el servidor.

<details><summary>Pista</summary>

El apellido compuesto va en `family` ("Paredes Cevallos") y cada apellido por
separado en extensiones dentro de `_family`. Mira la definición de
[HumanName](https://hl7.org/fhir/R4/datatypes.html#HumanName).
</details>

Solución: [`02a_patient_crear.json`](soluciones/02a_patient_crear.json)

### 02b · Leerlo

`GET {{FHIRURL}}/Patient/{{patientId}}`. Compara lo que enviaste con lo que
devuelve: ¿qué agregó el servidor en `meta`?

### 02c y 02d · Buscarlo

```http
GET {{FHIRURL}}/Patient?identifier=https://f-slg.github.io/aprende-fhir/sid/cedula|9900000017
GET {{FHIRURL}}/Patient?family=Paredes&given=Luis
```

El primer parámetro usa el formato `system|value`. ¿Cuál de las dos
búsquedas es más segura para encontrar a *esta* persona y no a otra?

### 02e · Actualizarlo

Luis da su teléfono (`+593 99 000 0000`) y su estado civil (casado). Con `PUT`
se envía **el recurso completo**, con su `id`, no solo los campos nuevos.

Solución: [`02e_patient_actualizar.json`](soluciones/02e_patient_actualizar.json)

### 02f · Historial

`GET {{FHIRURL}}/Patient/{{patientId}}/_history` devuelve las dos versiones.
Observa `meta.versionId` y `meta.lastUpdated` en cada una.

## Para pensar

Si en la actualización olvidas enviar la dirección, ¿qué pasa con ella? ¿Por
qué `PUT` reemplaza el recurso entero en lugar de modificar campos?

## Ejecutar este módulo

- **Postman:** carpeta *02 · Patient*.
- **curl:** `curl/taller.sh 02`
- **R:**

  ```r
  source("r/fhir.R")
  p <- fhir_crear("Patient", "modulos/02-patient/soluciones/02a_patient_crear.json",
                  guarda = "patientId")
  p$id
  fhir_leer("Patient/{{patientId}}/_history")$total
  ```
