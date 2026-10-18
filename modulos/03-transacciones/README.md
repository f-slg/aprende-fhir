# Módulo 03 · Transacciones

[← Módulo 02](../02-patient/README.md) · [Inicio](../../README.md) · [Módulo 04 →](../04-profesionales-y-organizaciones/README.md)

## Objetivos

- Enviar varios recursos en una sola petición con un `Bundle` de tipo
  `transaction`.
- Entender que una transacción es **todo o nada**.
- Evitar duplicados con la **creación condicional** (`ifNoneExist`).

## El caso

Luis acude con su familia: su hija María José, su esposa Carmen Elena y su
hijo Daniel Esteban. Hay que registrarlos a los tres a la vez.

## Conceptos clave

Un `Bundle` agrupa recursos. Según su `type` sirve para cosas distintas:

| `type` | Para qué |
|---|---|
| `searchset` | Resultados de una búsqueda (lo devuelve el servidor) |
| `transaction` | Varias operaciones que se aplican juntas: todas o ninguna |
| `batch` | Varias operaciones independientes: cada una puede fallar por separado |
| `document` | Un documento clínico firmado e inmutable (módulo 07) |
| `history` | Versiones de un recurso |

En una transacción, cada `entry` lleva el recurso y un `request` con el método
y la ruta. El `fullUrl` con `urn:uuid:` es un id temporal que sirve para que
las entradas se refieran entre sí antes de existir en el servidor.

`ifNoneExist` convierte el `POST` en una **creación condicional**: si ya
existe un paciente con esa cédula, el servidor no crea otro.

```json
"request": {
  "method": "POST",
  "url": "Patient",
  "ifNoneExist": "identifier=https://f-slg.github.io/aprende-fhir/sid/cedula|9900000025"
}
```

## Ejercicios

### 03a · Registrar a la familia

Arma un `Bundle` de tipo `transaction` con los tres pacientes y envíalo a la
**raíz** del servidor: `POST {{FHIRURL}}` (sin tipo de recurso en la ruta).

Solución: [`03a_bundle_transaction_familia.json`](soluciones/03a_bundle_transaction_familia.json)

La respuesta es un `Bundle` de tipo `transaction-response`: revisa en cada
`entry.response` el `status` y el `location` del recurso creado.

### 03b · Comprobar

`GET {{FHIRURL}}/Patient?family=Paredes`. ¿Cuántos pacientes aparecen? ¿Por
qué no aparece Carmen Elena?

### Reto

Envía **otra vez** la misma transacción. Gracias a `ifNoneExist`, el servidor
responde `200 OK` (ya existía) en lugar de `201 Created`, y no hay duplicados.
Ahora cambia las tres cédulas por otras nuevas y, en uno de los pacientes,
escribe `"gender": "masculino"` (el valor correcto es `male`). El servidor
responde `400` y, como es una transacción, **ninguno** de los tres pacientes
se crea.

## Para pensar

¿Cuándo usarías `batch` en lugar de `transaction`? Piensa en una carga masiva
de vacunas desde varios centros de salud.

## Ejecutar este módulo

- **Postman:** carpeta *03 · Transacciones*.
- **curl:** `curl/taller.sh 03`
- **R:** `fhir("POST", "", "modulos/03-transacciones/soluciones/03a_bundle_transaction_familia.json")`
