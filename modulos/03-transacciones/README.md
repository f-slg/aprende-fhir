# Módulo 03 · Transacciones: varios recursos a la vez

[← Módulo 02](../02-patient/README.md) · [Inicio](../../README.md) · [Módulo 04 →](../04-profesionales-y-organizaciones/README.md)

> **Nivel:** básico · **Duración:** 40 minutos · **Necesitas:** módulo 02

## Lo que vas a aprender

1. Qué es un **Bundle** y sus distintos tipos.
2. A enviar varios recursos en una sola petición con una **transacción**.
3. Por qué una transacción es **todo o nada**.
4. A evitar duplicados con la **creación condicional**.

## La historia

Luis llega acompañado de su familia: su esposa **Carmen Elena Andrade Vega**,
su hija **María José Paredes Andrade** (18 años) y su hijo **Daniel Esteban
Paredes Andrade** (15 años). La admisionista quiere registrar a los tres de
una vez, y sin crear duplicados si alguno ya estaba registrado.

---

## Ficha del recurso: Bundle

**¿Qué es?** Un **contenedor** de recursos. No representa nada clínico por sí
mismo: agrupa otros recursos para enviarlos, devolverlos o guardarlos juntos.

**¿Para qué se usa?** Depende de su `type`:

| `type` | Para qué | Quién lo crea |
|---|---|---|
| `searchset` | Resultados de una búsqueda | El servidor |
| `history` | Las versiones de uno o varios recursos | El servidor |
| `transaction` | Varias operaciones que se aplican **juntas: todas o ninguna** | Tú |
| `batch` | Varias operaciones **independientes**: cada una puede fallar por separado | Tú |
| `transaction-response`, `batch-response` | La respuesta a una transacción o un lote | El servidor |
| `document` | Un documento clínico firmado e inmutable (módulo 09) | Tú |
| `collection` | Un conjunto cualquiera de recursos | Tú |

**¿Cuándo usar otro recurso?** Si solo quieres agrupar recursos por tema
dentro del servidor (por ejemplo, "los pacientes de un programa"), usa
**Group** o **List**. Un Bundle es para **transportar** recursos.

**Elementos principales** (<https://hl7.org/fhir/R4/bundle.html>):

<!-- ficha Bundle -->
| Elemento | Card. | Tipo | Para qué sirve |
|---|---|---|---|
| `type` | **1..1** | code | Qué clase de Bundle es (tabla de arriba). |
| `timestamp` | 0..1 | instant | Cuándo se armó el Bundle. Obligatorio en los documentos. |
| `total` | 0..1 | unsignedInt | En una búsqueda, cuántos resultados hay en total. |
| `link` | 0..* | BackboneElement | Enlaces de paginación: `self`, `next`, `previous`. |
| `entry` | 0..* | BackboneElement | Cada uno de los recursos que contiene. |
| `entry.fullUrl` | 0..1 | uri | La dirección del recurso, o un `urn:uuid:` temporal. |
| `entry.resource` | 0..1 | Resource | El recurso en sí. |
| `entry.request` | 0..1 | BackboneElement | En una transacción: qué operación hacer con este recurso. |
| `entry.request.method` | **1..1** | code | `POST`, `PUT`, `DELETE`... |
| `entry.request.url` | **1..1** | uri | Dónde: `Patient`, `Patient/1000`... |
| `entry.request.ifNoneExist` | 0..1 | string | Creación condicional: no crear si ya existe un recurso que cumple esta búsqueda. |
| `entry.response` | 0..1 | BackboneElement | En la respuesta: el resultado de cada operación. |
<!-- /ficha -->

---

## Paso a paso: armar la transacción

### Paso 1 · El contenedor

```json
{
  "resourceType": "Bundle",
  "type": "transaction",
  "entry": [ ]
}
```

### Paso 2 · Una entrada por cada paciente

Cada `entry` lleva tres cosas: el recurso, su `fullUrl` y la operación.

```json
{
  "fullUrl": "urn:uuid:…",
  "resource": { "resourceType": "Patient", "identifier": [ … ], "name": [ … ], "gender": "female", "birthDate": "2006-07-21" },
  "request": { "method": "POST", "url": "Patient" }
}
```

El `fullUrl` con `urn:uuid:` es un **identificador temporal**. Sirve para que
un recurso de la transacción apunte a otro que todavía no existe en el
servidor: el servidor reemplaza cada `urn:uuid:` por el `id` definitivo al
guardar. Aquí los pacientes no se apuntan entre sí, pero en el módulo 09 lo
aprovecharás.

### Paso 3 · Evitar duplicados

```json
"request": {
  "method": "POST",
  "url": "Patient",
  "ifNoneExist": "identifier=https://f-slg.github.io/aprende-fhir/sid/cedula|9900000025"
}
```

`ifNoneExist` convierte el `POST` en una **creación condicional**: el
servidor busca primero un paciente con esa cédula y solo lo crea si no
existe. Así puedes enviar la misma transacción dos veces sin duplicar a
nadie.

Solución completa: [`03a_bundle_transaction_familia.json`](soluciones/03a_bundle_transaction_familia.json).

---

## Ejercicios en el servidor

### 03a · Registrar a la familia

Una transacción se envía a la **raíz** del servidor, sin tipo de recurso en
la ruta:

```http
POST {{FHIRURL}}
Content-Type: application/fhir+json
```

Respuesta: **`200 OK`** con un Bundle de tipo `transaction-response`. En cada
`entry.response` verás:

- `status`: `201 Created` si lo creó, o `200 OK` si ya existía;
- `location`: la dirección del recurso, por ejemplo `Patient/1001/_history/1`.

### 03b · Comprobar

```http
GET {{FHIRURL}}/Patient?family=Paredes
```

Aparecen Luis, María José y Daniel. ¿Por qué no aparece Carmen Elena?
*(Pista: mira su apellido.)*

### Reto 1 · La creación condicional

Envía **otra vez** la misma transacción. En `entry.response.status` ahora
verás `200 OK` en lugar de `201 Created`: los pacientes ya existían y no se
duplicaron.

### Reto 2 · Todo o nada

Copia la transacción y cambia las tres cédulas por otras nuevas (por ejemplo,
que empiecen con `98`). En uno de los pacientes escribe
`"gender": "masculino"`. El servidor responde **`400`**:

```
HAPI-1821: [element="gender"] Invalid attribute value "masculino": Unknown AdministrativeGender code 'masculino'
```

Busca ahora a los pacientes con las cédulas nuevas: **no existe ninguno**.
Aunque solo una entrada estaba mal, la transacción se rechazó completa. Eso
garantiza que nunca quede la familia registrada a medias.

## Autoevaluación

<details><summary>1. ¿A qué dirección se envía una transacción?</summary>

A la raíz del servidor: `POST {{FHIRURL}}`, no a `/Patient` ni a `/Bundle`.
</details>

<details><summary>2. ¿Cuándo usarías <code>batch</code> en lugar de <code>transaction</code>?</summary>

Cuando las operaciones son independientes y prefieres que se guarden las
correctas aunque alguna falle. Por ejemplo, una carga masiva de vacunas de
muchos centros de salud: no conviene rechazar todo por un registro con error.
</details>

<details><summary>3. ¿Para qué sirve <code>ifNoneExist</code>?</summary>

Para no crear un recurso si ya existe uno que cumple la búsqueda indicada
(aquí, la misma cédula). Evita duplicados cuando se reenvía información.
</details>

## Resumen

- Un **Bundle** agrupa recursos; su `type` dice para qué.
- Una **transacción** se envía a la raíz y es **todo o nada**.
- `urn:uuid:` es un identificador temporal para enlazar recursos que aún no
  existen.
- `ifNoneExist` evita duplicados.

## Ejecutar este módulo

- **Postman:** carpeta *03 · Transacciones*.
- **curl:** `curl/taller.sh 03`
- **R:**

  ```r
  r <- fhir("POST", "", "modulos/03-transacciones/soluciones/03a_bundle_transaction_familia.json")
  vapply(r$entry, function(e) e$response$status, "")
  ```
