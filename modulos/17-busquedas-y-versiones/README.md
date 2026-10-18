# Módulo 17 · Búsquedas avanzadas y versiones

[← Módulo 16](../16-seguimiento/README.md) · [Inicio](../../README.md) · [Módulo 18 →](../18-terminologias-y-perfiles/README.md)

> **Nivel:** avanzado · **Duración:** 90 minutos · **Necesitas:** módulos 01 a 16
> (este módulo busca sobre el expediente completo de Luis)

## Lo que vas a aprender

1. Los **tipos de parámetros** de búsqueda y cómo se escribe cada uno.
2. **Prefijos** para comparar números y fechas (`gt`, `ge`, `lt`...).
3. **Modificadores** (`:exact`, `:not`, `:missing`...).
4. **Búsquedas encadenadas** (`subject.identifier`) e **inversas** (`_has`).
5. A controlar **qué** devuelve el servidor y **cuánto** (`_summary`,
   `_elements`, `_sort`, `_count`, paginación).
6. A trabajar con **versiones**: leer una versión anterior, comparar versiones
   y evitar que dos personas se sobrescriban (`If-Match`).

## La historia

Han pasado diez meses desde la primera consulta. El expediente de Luis tiene
más de 60 recursos. Ahora no se trata de registrar, sino de **encontrar**: la
última frecuencia cardíaca, las consultas de abril, los problemas activos,
los pacientes con cáncer de mama. Y la admisionista necesita agregar el
correo electrónico de Luis sin pisar los cambios que otra persona pueda estar
haciendo al mismo tiempo.

> Todas las búsquedas de este módulo se envían con `Cache-Control: no-cache`,
> para que el servidor no reutilice resultados anteriores (módulo 14).

---

## Ficha: los tipos de parámetros de búsqueda

Cada recurso tiene sus **parámetros de búsqueda**, que están al final de su
página en la especificación (por ejemplo,
<https://hl7.org/fhir/R4/observation.html#search>). Cada parámetro es de un
**tipo**, y el tipo dice cómo se escribe el valor:

| Tipo | Busca en... | Cómo se escribe | Ejemplo |
|---|---|---|---|
| `string` | Textos: nombres, direcciones | El comienzo del texto, sin importar mayúsculas ni tildes | `Patient?family=pare` |
| `token` | Códigos e identificadores | `system\|code`, o solo `code` | `Observation?code=http://loinc.org\|8310-5` |
| `reference` | Referencias a otros recursos | `Tipo/id` | `Observation?subject=Patient/1001` |
| `date` | Fechas y periodos | `AAAA-MM-DD`, con prefijo opcional | `Encounter?date=ge2025-04-01` |
| `quantity` | Cantidades | `[prefijo]valor\|sistema\|unidad` | `Observation?value-quantity=ge38\|http://unitsofmeasure.org\|Cel` |
| `number` | Números sin unidad | `[prefijo]valor` | `RiskAssessment?probability=gt0.8` |
| `uri` | Direcciones canónicas | La URL completa | `Questionnaire?url=https://…` |

**Parámetros generales**, que sirven en cualquier recurso:

| Parámetro | Para qué | Ejemplo |
|---|---|---|
| `_id` | Por id | `Patient?_id=1001` |
| `_lastUpdated` | Por fecha de última modificación | `Patient?_lastUpdated=gt2026-01-01` |
| `_count` | Resultados por página | `_count=5` |
| `_sort` | Orden (con `-`, descendente) | `_sort=-date` |
| `_summary` | Una versión resumida, o solo el total con `count` | `_summary=count` |
| `_elements` | Solo ciertos elementos | `_elements=code,value` |
| `_include`, `_revinclude` | Agregar recursos relacionados (módulos 05 y 10) | `_include=Encounter:diagnosis` |
| `_has` | Búsqueda inversa | `Patient?_has:Condition:subject:code=…` |

Los valores con caracteres especiales se **codifican** en la URL: un espacio
es `%20`, una barra vertical `|` puede ir como `%7C`. Postman lo hace por ti;
en curl y en el navegador, escríbelo tú.

## Ficha: prefijos

Para `date`, `number` y `quantity`, el valor puede llevar un prefijo:

| Prefijo | Significa | Ejemplo |
|---|---|---|
| `eq` | igual (es el predeterminado) | `date=eq2025-04-22` |
| `ne` | distinto | `value-quantity=ne0` |
| `gt` / `lt` | mayor / menor que | `value-quantity=gt100` |
| `ge` / `le` | mayor o igual / menor o igual | `date=ge2025-04-01` |
| `sa` / `eb` | empieza después de / termina antes de | `date=sa2025-06-01` |

Para un **rango**, se repite el parámetro: `date=ge2025-04-01&date=lt2025-05-01`
es "en abril de 2025".

## Ficha: modificadores

Se escriben después del nombre del parámetro, con dos puntos:

| Modificador | Para | Significa | Ejemplo |
|---|---|---|---|
| `:exact` | string | Exactamente ese texto (con mayúsculas y tildes) | `family:exact=Paredes Cevallos` |
| `:contains` | string | Contiene el texto en cualquier parte | `family:contains=redes` |
| `:text` | token | Busca en el texto del código, no en el código | `code:text=presión` |
| `:not` | token | Distinto de ese código | `clinical-status:not=resolved` |
| `:missing` | todos | El elemento falta (`true`) o está (`false`) | `encounter:missing=true` |
| `:[Tipo]` | reference | Limita el tipo de recurso referenciado | `subject:Patient.family=Paredes` |

---

## Ejercicios en el servidor

### 17a · Encadenada: por la cédula, sin conocer el id

```http
GET {{FHIRURL}}/Observation?subject.identifier=https://f-slg.github.io/aprende-fhir/sid/cedula|9900000017&category=vital-signs
```

El punto **encadena**: "las observaciones cuyo `subject` es un paciente con
esta cédula". No necesitas saber el `id` de Luis en el servidor, solo su
cédula: es la forma de buscar cuando los datos vienen de otro sistema.
Devuelve 5 signos vitales (los 4 de la consulta y la superficie corporal).

### 17b · Encadenada con tipo

```http
GET {{FHIRURL}}/Encounter?subject:Patient.family=Paredes&subject:Patient.given=Luis
```

`:Patient` aclara de qué tipo es la referencia encadenada. Devuelve las 3
atenciones de Luis: la consulta de marzo, el vacunatorio y la consulta por el
nódulo.

### 17c · Inversa: `_has`

```http
GET {{FHIRURL}}/Patient?_has:Condition:subject:code=http://snomed.info/sct|254837009
```

Se lee: "pacientes **que tienen** una Condition, cuyo `subject` es el
paciente, con el código de cáncer de mama". Es la búsqueda de un registro de
tumores o de un programa: encontrar personas a partir de sus diagnósticos.

### 17d · Prefijo `gt`

```http
GET {{FHIRURL}}/Observation?subject=Patient/{{patientId}}&code=http://loinc.org|8867-4&value-quantity=gt100
```

Frecuencias cardíacas mayores que 100: encuentra los 102 latidos por minuto
de la consulta de marzo.

### 17e · Un rango de fechas

```http
GET {{FHIRURL}}/Encounter?subject=Patient/{{patientId}}&date=ge2025-04-01&date=lt2025-05-01
```

Las atenciones de abril: el vacunatorio (3 de abril) y la consulta por el
nódulo (22 de abril).

### 17f, 17g y 17h · Modificadores

```http
GET {{FHIRURL}}/Patient?family:exact=Paredes%20Cevallos
GET {{FHIRURL}}/Condition?subject=Patient/{{patientId}}&clinical-status:not=resolved
GET {{FHIRURL}}/Observation?subject=Patient/{{patientId}}&encounter:missing=true
```

- `:exact` encuentra solo a Luis, no a sus hijos Paredes Andrade. Fíjate en
  el `%20`: el espacio va codificado.
- `:not=resolved` deja solo el cáncer de mama: la intoxicación se resolvió.
- `:missing=true` devuelve las 4 observaciones registradas fuera de una
  consulta: el tamaño del tumor, el receptor de estrógeno, la superficie
  corporal y el dolor del cuestionario. Útil para controlar la calidad del
  registro.

### 17i, 17j y 17k · Controlar la respuesta

```http
GET {{FHIRURL}}/Observation?subject=Patient/{{patientId}}&_summary=count
GET {{FHIRURL}}/Observation?subject=Patient/{{patientId}}&category=vital-signs&_elements=code,value
GET {{FHIRURL}}/Observation?subject=Patient/{{patientId}}&code=http://loinc.org|8867-4&_sort=-date&_count=1
```

- `_summary=count` devuelve **solo el total** (12 observaciones), sin los
  recursos: ideal para indicadores.
- `_elements=code,value` devuelve cada observación solo con su código y su
  valor. Para un elemento de elección se usa su nombre base: `value`, no
  `valueQuantity`.
- `_sort=-date&_count=1` es "la más reciente": orden descendente por fecha y
  un solo resultado.

### 17l · Paginación

```http
GET {{FHIRURL}}/Observation?subject=Patient/{{patientId}}&_count=5
```

El servidor devuelve 5 resultados y, en `link`, la relación `next` con la
dirección de la página siguiente. Para recorrer todos los resultados se
sigue `next` hasta que no aparezca. **No construyas tú la dirección de la
página siguiente**: usa la que da el servidor.

## Las versiones

Cada `PUT` crea una **versión** nueva (módulo 02). El servidor lo indica en
`meta.versionId` y en el encabezado HTTP `ETag`, por ejemplo `W/"2"`.

| Operación | Petición | Para qué |
|---|---|---|
| Leer la versión actual | `GET /Patient/{id}` | Lo de siempre |
| Historial | `GET /Patient/{id}/_history` | Todas las versiones (módulo 02) |
| Leer una versión (*vread*) | `GET /Patient/{id}/_history/1` | Cómo estaba en un momento |
| Comparar versiones | `GET /Patient/{id}/$diff` | Qué cambió (operación de HAPI) |
| Actualizar sin pisar a otro | `PUT` con `If-Match: W/"2"` | Control de concurrencia |

### 17m y 17n · Leer y comparar versiones

```http
GET {{FHIRURL}}/Patient/{{patientId}}/_history/1
GET {{FHIRURL}}/Patient/{{patientId}}/$diff
```

La versión 1 es el paciente del módulo 02, sin teléfono ni estado civil.
`$diff` compara la versión actual con la anterior y devuelve un `Parameters`
con cada cambio: su tipo (`insert`, `replace`, `delete`) y su ruta
(`Patient.telecom`, `Patient.maritalStatus`...). `$diff` es una operación de
HAPI: no todos los servidores la tienen.

### 17o · Actualizar con `If-Match`

Imagina que la admisionista abre el registro de Luis (versión 2) para
agregar su correo. Mientras escribe, otra persona actualiza el teléfono. Si la
admisionista guarda sin más, **borra** el cambio de la otra persona, porque
`PUT` reemplaza todo el recurso.

`If-Match` lo evita: dice "actualiza solo si el recurso **sigue** en la
versión que yo leí".

```http
PUT {{FHIRURL}}/Patient/{{patientId}}
If-Match: W/"2"
```

Esto es lo que agrega la actualización
([`17a_patient_agregar_correo.json`](soluciones/17a_patient_agregar_correo.json)):

<!-- diferencia 17a -->
```json
{
  "telecom": [
    {
      "system": "phone",
      "value": "+593 99 000 0000",
      "use": "mobile"
    },
    {
      "system": "email",
      "value": "luis.paredes@correo.invalid",
      "use": "home"
    }
  ]
}
```
<!-- /diferencia -->

El servidor responde `200 OK` y el paciente pasa a la versión 3.

### 17p · Error a propósito: actualizar con una versión vieja

Repite **exactamente** la misma petición, con `If-Match: W/"2"`. Ahora el
recurso ya está en la versión 3, y el servidor la rechaza:

```
409 · HAPI-0989: Trying to update Patient/1001/_history/2 but this is not the current version
```

La especificación de FHIR indica responder `412 Precondition Failed`; HAPI
responde `409 Conflict`. Los dos dicen lo mismo: **alguien cambió el recurso
después de que lo leíste**. Lo correcto es volver a leerlo, aplicar tu cambio
sobre la versión nueva y enviarlo con el `If-Match` actualizado.

## Para pensar

Para un **tablero de vigilancia** de hipertensión necesitas, cada semana, el
número de pacientes con hipertensión que tienen al menos una presión
sistólica mayor o igual a 140 en el último mes. ¿Qué combinación de `_has`,
`_summary=count` y prefijos de fecha usarías? ¿Qué problema tendría contar
directamente las observaciones en lugar de los pacientes?

## Autoevaluación

<details><summary>1. ¿Cómo buscas las vacunas de un paciente si solo conoces su cédula?</summary>

Con una búsqueda encadenada: `Immunization?patient.identifier=<system>|<cédula>`.
</details>

<details><summary>2. ¿Qué diferencia hay entre <code>_include</code> y <code>_has</code>?</summary>

`_include` **agrega** al resultado los recursos relacionados. `_has`
**filtra**: devuelve los recursos que tienen otros recursos que cumplen una
condición, sin agregarlos.
</details>

<details><summary>3. El servidor responde 409 a tu <code>PUT</code> con <code>If-Match</code>. ¿Qué haces?</summary>

Vuelves a leer el recurso (que tiene cambios de otra persona), aplicas tu
cambio sobre esa versión y lo envías con el `If-Match` de la versión nueva.
</details>

## Resumen

- El **tipo** del parámetro dice cómo se escribe el valor: `string`, `token`,
  `reference`, `date`, `quantity`...
- Los **prefijos** comparan (`gt`, `ge`, `lt`, `le`) y los **modificadores**
  cambian el sentido (`:exact`, `:not`, `:missing`).
- Las búsquedas **encadenadas** cruzan referencias; `_has` busca al revés.
- `_summary=count`, `_elements`, `_sort` y `_count` controlan la respuesta;
  para paginar se sigue `next`.
- `If-Match` evita que dos actualizaciones se pisen.

## Ejecutar este módulo

- **Postman:** carpeta *17 · Búsquedas avanzadas y versiones*.
- **curl:** `curl/taller.sh 17` (necesita los módulos anteriores: ejecuta todo)
- **R:**

  ```r
  # La frecuencia cardíaca más reciente, sin conocer el id del paciente
  fc <- fhir("GET", paste0("Observation?subject.identifier=https://f-slg.github.io/aprende-fhir/sid/cedula|9900000017",
                           "&code=http://loinc.org|8867-4&_sort=-date&_count=1"),
             encabezados = list(`Cache-Control` = "no-cache"))
  fc$entry[[1]]$resource$valueQuantity$value
  ```
