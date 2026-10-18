# Módulo 18 · Terminologías y perfiles

[← Módulo 17](../17-busquedas-y-versiones/README.md) · [Inicio](../../README.md) · [Módulo 19 →](../19-resumen-ips/README.md)

> **Nivel:** avanzado · **Duración:** 90 minutos · **Necesitas:** módulos 01 a 16

## Lo que vas a aprender

1. Qué son **CodeSystem** y **ValueSet**, y en qué se diferencian.
2. A usar un **servidor de terminología**: `$lookup`, `$validate-code`,
   `$expand` y `$subsumes`.
3. A crear un **sistema de códigos propio**.
4. Qué es un **perfil** y a escribir uno con **StructureDefinition**.
5. A pedirle al servidor que **valide** con `$validate`, con o sin perfil.
6. Qué es una **guía de implementación**.

## La historia

El hospital quiere que todos sus sistemas registren la funcionalidad ECOG
con los mismos códigos, y que ningún paciente se registre sin cédula,
nombre, sexo y fecha de nacimiento. Son dos necesidades distintas:

- **qué códigos usar**: un problema de **terminología**;
- **qué datos son obligatorios**: un problema de **perfiles**.

En este módulo aprendes las dos cosas. Además, vuelves a los errores de los
módulos anteriores y ves que el servidor también podía detectarlos, si se lo
pides.

---

## Parte 1 · Terminologías

### CodeSystem frente a ValueSet

| | CodeSystem | ValueSet |
|---|---|---|
| ¿Qué es? | Un **sistema de códigos**: define códigos y su significado | Un **conjunto de valores**: elige códigos de uno o más sistemas para un uso |
| Ejemplos | LOINC, SNOMED CT, CIE-10, CVX, `administrative-gender` | "códigos de sexo administrativo", "signos vitales", "criticidad de alergias" |
| ¿Quién lo define? | Su organización (Regenstrief, SNOMED International, OMS) o tú | Quien necesita restringir un elemento |
| Analogía | El diccionario completo | La lista de palabras permitidas para un formulario |

Un elemento **codificado** de un recurso se **vincula** (*binding*) a un
ValueSet, con una fuerza: `required` (solo esos códigos, como `gender`),
`extensible` (esos, salvo que ninguno sirva, como el tipo de identificador
del módulo 02), `preferred` o `example`.

### Ficha del recurso: CodeSystem

<!-- ficha CodeSystem -->
| Elemento | Card. | Tipo | Para qué sirve |
|---|---|---|---|
| `url` | 0..1 | uri | La dirección canónica que identifica el sistema (el `system` de los `Coding`). |
| `version` | 0..1 | string | Versión. |
| `name` | 0..1 | string | Nombre para máquinas. |
| `title` | 0..1 | string | Título para personas. |
| `status` ⚑ | **1..1** | code | `draft`, `active`, `retired` o `unknown`. |
| `date` | 0..1 | dateTime | Fecha de la versión. |
| `publisher` | 0..1 | string | Quién lo publica. |
| `description` | 0..1 | markdown | Para qué sirve. |
| `caseSensitive` | 0..1 | boolean | Si los códigos distinguen mayúsculas. |
| `hierarchyMeaning` | 0..1 | code | Qué significa la jerarquía (`is-a`, `part-of`...). |
| `content` | **1..1** | code | `complete` si trae todos los códigos; `not-present` si solo los describe. |
| `count` | 0..1 | unsignedInt | Cuántos códigos tiene. |
| `concept` | 0..* | BackboneElement | Los códigos. |
| `concept.code` | **1..1** | code | El código. |
| `concept.display` | 0..1 | string | Su nombre. |
| `concept.definition` | 0..1 | string | Su definición. |
| `concept.concept` | 0..* |  | Códigos hijos (jerarquía). |
<!-- /ficha -->

### Ficha del recurso: ValueSet

<!-- ficha ValueSet -->
| Elemento | Card. | Tipo | Para qué sirve |
|---|---|---|---|
| `url` | 0..1 | uri | La dirección canónica del conjunto. |
| `version` | 0..1 | string | Versión. |
| `name` | 0..1 | string | Nombre para máquinas. |
| `title` | 0..1 | string | Título para personas. |
| `status` ⚑ | **1..1** | code | `draft`, `active`, `retired` o `unknown`. |
| `date` | 0..1 | dateTime | Fecha. |
| `publisher` | 0..1 | string | Quién lo publica. |
| `description` | 0..1 | markdown | Para qué sirve. |
| `compose` | 0..1 | BackboneElement | **Cómo se arma**: qué incluir y qué excluir. |
| `compose.include` | **1..*** | BackboneElement | De qué sistemas y con qué criterio. |
| `compose.include.system` | 0..1 | uri | El CodeSystem. |
| `compose.include.concept` | 0..* | BackboneElement | Códigos concretos. |
| `compose.include.filter` | 0..* | BackboneElement | Criterios (por ejemplo, "todo lo que es un tipo de neoplasia"). |
| `compose.exclude` | 0..* |  | Lo que se excluye. |
| `expansion` | 0..1 | BackboneElement | La lista final de códigos, ya calculada. |
<!-- /ficha -->

### Las operaciones de terminología

| Operación | Pregunta | Ejemplo |
|---|---|---|
| `CodeSystem/$lookup` | ¿Qué significa este código? | LOINC `8310-5` → *Body temperature* |
| `ValueSet/$validate-code` | ¿Este código está en este conjunto? | `masculino` en `administrative-gender` → no |
| `ValueSet/$expand` | ¿Qué códigos tiene este conjunto? | criticidad de alergias → `low`, `high`, `unable-to-assess` |
| `CodeSystem/$subsumes` | ¿Este concepto incluye a este otro? | *Malignant neoplastic disease* incluye a *Malignant neoplasm of breast* |
| `ConceptMap/$translate` | ¿Cómo se dice este código en otro sistema? | De un catálogo local a SNOMED CT |

LOINC y SNOMED CT tienen cientos de miles de códigos, y un servidor clínico
común no los trae cargados. Para consultarlos se usa un **servidor de
terminología**. En el taller usamos el de HL7, `https://tx.fhir.org/r4`
(variable `TXURL`). Es el mismo que usa el validador oficial para revisar los
códigos y sus nombres.

> `tx.fhir.org` es un servicio público y a veces no responde. Si un paso de
> terminología falla, Postman, curl y R muestran un aviso y siguen con el
> resto del taller.

---

## Paso a paso: el sistema de códigos ECOG

### Paso 1 · El mínimo: url, nombre, estado y contenido

<!-- paso 18b 1 -->
```json
{
  "resourceType": "CodeSystem",
  "url": "https://f-slg.github.io/aprende-fhir/CodeSystem/ecog",
  "name": "EscalaECOG",
  "status": "active",
  "content": "complete"
}
```
<!-- /paso -->

La `url` es lo que irá en `Coding.system` cuando se use un código ECOG. Como
todas las direcciones del taller, es didáctica.

### Paso 2 · Los metadatos

<!-- paso 18b 2 -->
```json
{
  "version": "1.0.0",
  "title": "Escala de funcionalidad ECOG (versión didáctica)",
  "date": "2026-10-18",
  "publisher": "Aprende FHIR desde cero (ejemplo didáctico)",
  "description": "Códigos de la escala de funcionalidad ECOG, con descripciones en español.",
  "caseSensitive": true
}
```
<!-- /paso -->

### Paso 3 · Los códigos

<!-- paso 18b 3 -->
```json
{
  "count": 5,
  "concept": [
    {
      "code": "0",
      "display": "Actividad normal sin limitaciones"
    },
    {
      "code": "1",
      "display": "Síntomas, pero ambulatorio y capaz de trabajos ligeros"
    },
    {
      "code": "2",
      "display": "Ambulatorio y capaz de cuidarse, pero no de trabajar"
    },
    {
      "code": "3",
      "display": "En cama o sentado más de la mitad del día"
    },
    {
      "code": "4",
      "display": "Completamente incapacitado, en cama"
    }
  ],
  "text": {
    "status": "generated",
    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><p>Escala de funcionalidad ECOG (versión didáctica): 0 a 4.</p></div>"
  }
}
```
<!-- /paso -->

`content: complete` y `count: 5`: el sistema trae sus 5 códigos. Solución:
[`18b_codesystem_ecog.json`](soluciones/18b_codesystem_ecog.json).

## Paso a paso: el conjunto de valores ECOG

### Paso 1 · El mínimo: url, nombre y estado

<!-- paso 18c 1 -->
```json
{
  "resourceType": "ValueSet",
  "url": "https://f-slg.github.io/aprende-fhir/ValueSet/ecog",
  "name": "ValoresECOG",
  "status": "active"
}
```
<!-- /paso -->

### Paso 2 · Qué códigos incluye

<!-- paso 18c 2 -->
```json
{
  "compose": {
    "include": [
      {
        "system": "https://f-slg.github.io/aprende-fhir/CodeSystem/ecog"
      }
    ]
  }
}
```
<!-- /paso -->

`compose.include` con solo el `system` incluye **todos** los códigos del
sistema. Para elegir algunos, se agregan en `concept`; para elegir por
criterio, se usa `filter`.

### Paso 3 · Los metadatos

<!-- paso 18c 3 -->
```json
{
  "version": "1.0.0",
  "title": "Valores de la escala ECOG",
  "date": "2026-10-18",
  "publisher": "Aprende FHIR desde cero (ejemplo didáctico)",
  "description": "Conjunto de valores con todos los códigos de la escala ECOG del taller.",
  "text": {
    "status": "generated",
    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><p>Valores de la escala ECOG: todos los códigos del CodeSystem EscalaECOG.</p></div>"
  }
}
```
<!-- /paso -->

Solución: [`18c_valueset_ecog.json`](soluciones/18c_valueset_ecog.json).

---

## Parte 2 · Perfiles

Un **perfil** adapta un recurso a un uso concreto: dice qué elementos son
obligatorios, qué códigos se usan, qué extensiones se agregan. **No crea un
recurso nuevo**: un paciente que cumple el perfil sigue siendo un Patient.

| La especificación base dice... | Un perfil puede decir... |
|---|---|
| `birthDate` es `0..1` (opcional) | `birthDate` es `1..1` (obligatoria) |
| `identifier` puede ser cualquiera | debe haber una cédula, con este `system` |
| `gender` usa `administrative-gender` | (se mantiene: un perfil solo **restringe**, nunca amplía) |
| no hay etnia | se agrega una extensión de autoidentificación étnica |

Un conjunto de perfiles, terminologías, ejemplos y reglas para un país o un
proyecto es una **guía de implementación** (*Implementation Guide*, IG). Por
ejemplo: el **IPS** (resumen internacional del paciente, módulo 19), *US
Core* en Estados Unidos o las guías nacionales que publican otros países.
Puedes explorarlas en <https://registry.fhir.org/>.

### Ficha del recurso: StructureDefinition

**¿Qué es?** La **definición de una estructura**: de un recurso, de un tipo
de dato, de una extensión o, como aquí, de un **perfil**. La propia
especificación de FHIR está escrita con StructureDefinition.

<!-- ficha StructureDefinition -->
| Elemento | Card. | Tipo | Para qué sirve |
|---|---|---|---|
| `url` | **1..1** | uri | La dirección canónica del perfil (la que va en `meta.profile`). |
| `version` | 0..1 | string | Versión. |
| `name` | **1..1** | string | Nombre para máquinas. |
| `title` | 0..1 | string | Título para personas. |
| `status` ⚑ | **1..1** | code | `draft`, `active`, `retired` o `unknown`. |
| `date` | 0..1 | dateTime | Fecha. |
| `publisher` | 0..1 | string | Quién lo publica. |
| `description` | 0..1 | markdown | Para qué sirve. |
| `fhirVersion` | 0..1 | code | Para qué versión de FHIR. |
| `kind` | **1..1** | code | `resource`, `complex-type`, `primitive-type` o `logical`. |
| `abstract` | **1..1** | boolean | Si es abstracto. |
| `type` | **1..1** | uri | Sobre qué recurso o tipo es. |
| `baseDefinition` | 0..1 | canonical | De qué definición parte. |
| `derivation` | 0..1 | code | `constraint` (un perfil que restringe) o `specialization` (un recurso nuevo). |
| `snapshot` | 0..1 | BackboneElement | La definición completa, elemento por elemento. |
| `differential` | 0..1 | BackboneElement | **Solo lo que cambia** respecto de la base. |
<!-- /ficha -->

Se escribe el `differential`, que es corto, y las herramientas calculan el
`snapshot`.

## Paso a paso: el perfil PacienteTaller

### Paso 1 · El mínimo: qué es, sobre qué recurso y de qué deriva

<!-- paso 18a 1 -->
```json
{
  "resourceType": "StructureDefinition",
  "url": "https://f-slg.github.io/aprende-fhir/StructureDefinition/paciente-taller",
  "name": "PacienteTaller",
  "status": "draft",
  "fhirVersion": "4.0.1",
  "kind": "resource",
  "abstract": false,
  "type": "Patient",
  "baseDefinition": "http://hl7.org/fhir/StructureDefinition/Patient",
  "derivation": "constraint",
  "differential": {
    "element": [
      {
        "id": "Patient",
        "path": "Patient",
        "short": "Paciente del taller"
      }
    ]
  }
}
```
<!-- /paso -->

`type: Patient`, `baseDefinition`: el Patient de la especificación, y
`derivation: constraint`: es un perfil que restringe. El `differential`
empieza con el elemento raíz.

### Paso 2 · La primera restricción: al menos un identificador

<!-- paso 18a 2 -->
```json
{
  "differential": {
    "element": [
      {
        "id": "Patient",
        "path": "Patient",
        "short": "Paciente del taller"
      },
      {
        "id": "Patient.identifier",
        "path": "Patient.identifier",
        "short": "Al menos un identificador (la cédula)",
        "min": 1
      }
    ]
  }
}
```
<!-- /paso -->

Cada elemento del `differential` tiene `id` y `path` (`Patient.identifier`) y
solo lo que cambia: `min: 1`.

### Paso 3 · Las demás restricciones y los metadatos

<!-- paso 18a 3 -->
```json
{
  "differential": {
    "element": [
      {
        "id": "Patient",
        "path": "Patient",
        "short": "Paciente del taller"
      },
      {
        "id": "Patient.identifier",
        "path": "Patient.identifier",
        "short": "Al menos un identificador (la cédula)",
        "min": 1
      },
      {
        "id": "Patient.name",
        "path": "Patient.name",
        "short": "Al menos un nombre",
        "min": 1
      },
      {
        "id": "Patient.gender",
        "path": "Patient.gender",
        "short": "Sexo administrativo obligatorio",
        "min": 1
      },
      {
        "id": "Patient.birthDate",
        "path": "Patient.birthDate",
        "short": "Fecha de nacimiento obligatoria",
        "min": 1
      }
    ]
  },
  "version": "1.0.0",
  "title": "Paciente del taller",
  "date": "2026-10-18",
  "publisher": "Aprende FHIR desde cero (ejemplo didáctico)",
  "description": "Perfil didáctico de Patient: exige identificador, nombre, sexo y fecha de nacimiento.",
  "text": {
    "status": "generated",
    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><p>Perfil didáctico PacienteTaller: un Patient que debe tener al menos un identificador,</p><p>un nombre, el sexo y la fecha de nacimiento.</p></div>"
  }
}
```
<!-- /paso -->

Cuatro elementos obligatorios: identificador, nombre, sexo y fecha de
nacimiento. Solución:
[`18a_structuredefinition_paciente_taller.json`](soluciones/18a_structuredefinition_paciente_taller.json).

Un recurso puede **declarar** que cumple un perfil con
`"meta": {"profile": ["https://f-slg.github.io/aprende-fhir/StructureDefinition/paciente-taller"]}`.
Declararlo no lo hace cumplir: hay que validarlo.

---

## Ejercicios en el servidor

### 18a · Guardar el perfil

```http
POST {{FHIRURL}}/StructureDefinition
If-None-Exist: url=https://f-slg.github.io/aprende-fhir/StructureDefinition/paciente-taller
```

StructureDefinition, CodeSystem, ValueSet y Questionnaire son **recursos
canónicos**: se identifican por su `url` y su `version`, y debe haber uno solo
por cada pareja. Por eso se crean con **creación condicional** (módulo 16): si
ya existe, el servidor devuelve el que tiene. HAPI es estricto con los
sistemas de códigos: si intentas crear un segundo CodeSystem con la misma
`url` y `version`, responde `422`:

```
HAPI-0848: Can not create multiple CodeSystem resources with CodeSystem.url "https://f-slg.github.io/aprende-fhir/CodeSystem/ecog" and CodeSystem.version "1.0.0"
```

### 18b · Validar a Luis contra el perfil

```http
POST {{FHIRURL}}/Patient/$validate?profile=https://f-slg.github.io/aprende-fhir/StructureDefinition/paciente-taller
Content-Type: application/fhir+json

(el paciente del módulo 02)
```

`$validate` **no guarda** el recurso: solo lo revisa y devuelve un
`OperationOutcome`. Luis cumple el perfil: sin errores, solo el aviso
conocido del tipo de identificador `NI` (módulo 02).

### 18c · Error a propósito: un paciente sin fecha de nacimiento

Valida contra el perfil
[`18e1_paciente_sin_fecha.json`](errores/18e1_paciente_sin_fecha.json), que
tiene cédula, nombre y sexo, pero no fecha de nacimiento:

```
Patient.birthDate: minimum required = 1, but only found 0 (from https://f-slg.github.io/aprende-fhir/StructureDefinition/paciente-taller|1.0.0)
```

**Fíjate en el código HTTP: `200 OK`.** `$validate` responde bien porque la
**operación** salió bien; el resultado de la validación está en los `issue`
del `OperationOutcome`. Lee siempre los `issue` con `severity: error`.

El mismo paciente es válido para la especificación base (`birthDate` es
opcional): solo el perfil lo hace obligatorio.

### 18d · El servidor también valida sin perfil

```http
POST {{FHIRURL}}/Observation/$validate
```

Con la observación sin código del módulo 06, que el servidor **aceptó** al
guardarla:

```
Observation.code: minimum required = 1, but only found 0
```

El servidor sabía que estaba mal; simplemente no valida al guardar, salvo
que se configure para hacerlo. Si tu sistema envía datos a un servidor, puedes
llamar a `$validate` antes de guardar.

### 18e a 18i · El sistema de códigos propio, en el servidor

| Paso | Petición | Resultado |
|---|---|---|
| 18e | `POST /CodeSystem` con `If-None-Exist: url=…/CodeSystem/ecog` | `codeSystemId` |
| 18f | `POST /ValueSet` con `If-None-Exist: url=…/ValueSet/ecog` | `valueSetId` |
| 18g | `GET /CodeSystem/$lookup?system=https://f-slg.github.io/aprende-fhir/CodeSystem/ecog&code=1` | *Síntomas, pero ambulatorio y capaz de trabajos ligeros* |
| 18h | `GET /ValueSet/$validate-code?url=…/ValueSet/ecog&system=…/CodeSystem/ecog&code=1` | `result: true` |
| 18i | igual, con `code=9` | `result: false`: *Unknown code '…#9'* |

Las respuestas de las operaciones de terminología son recursos
**Parameters**: una lista de pares nombre-valor (`name`, `display`, `result`,
`message`...).

> El servidor HAPI de prueba no puede **expandir** (`$expand`) un ValueSet
> propio en su configuración de fábrica: responde *"Hibernate Search was not
> initialized"*, porque ese motor de búsqueda viene desactivado. Por eso
> `$expand` lo hacemos en el servidor de terminología.

### 18j a 18n · El servidor de terminología

```http
GET {{TXURL}}/CodeSystem/$lookup?system=http://loinc.org&code=8310-5
GET {{TXURL}}/CodeSystem/$lookup?system=http://snomed.info/sct&code=254837009
GET {{TXURL}}/CodeSystem/$subsumes?system=http://snomed.info/sct&codeA=363346000&codeB=254837009
GET {{TXURL}}/ValueSet/$validate-code?url=http://hl7.org/fhir/ValueSet/administrative-gender&system=http://hl7.org/fhir/administrative-gender&code=masculino
GET {{TXURL}}/ValueSet/$expand?url=http://hl7.org/fhir/ValueSet/allergy-intolerance-criticality
```

| Paso | Qué obtienes |
|---|---|
| 18j | LOINC `8310-5` es *Body temperature* |
| 18k | SNOMED CT `254837009` es *Malignant neoplasm of breast* |
| 18l | `subsumes`: *Malignant neoplastic disease* (`363346000`) **incluye** al cáncer de mama. Así un sistema sabe que "todas las neoplasias malignas" abarca el diagnóstico de Luis. |
| 18m | `result: false`: *Unknown code 'masculino'*. Es exactamente lo que vio el servidor en el reto del módulo 03. |
| 18n | Los tres códigos de criticidad: `low`, `high`, `unable-to-assess` |

## Para pensar

Para un sistema de vigilancia, ¿cómo usarías `$subsumes` (o un ValueSet con
`filter` de tipo `is-a`) para contar **todos** los casos de neoplasias
malignas, sin tener que listar a mano cada código de cada tipo de cáncer?

## Autoevaluación

<details><summary>1. ¿LOINC es un CodeSystem o un ValueSet?</summary>

Un **CodeSystem**: define los códigos. "Los códigos LOINC de signos vitales"
sería un ValueSet.
</details>

<details><summary>2. Un perfil, ¿puede volver opcional un elemento obligatorio de la base?</summary>

No. Un perfil solo **restringe**: puede volver obligatorio lo opcional, pero
no al revés.
</details>

<details><summary>3. <code>$validate</code> respondió <code>200 OK</code>. ¿El recurso es válido?</summary>

No necesariamente: hay que leer los `issue` del `OperationOutcome`. El `200`
solo dice que la operación se ejecutó.
</details>

## Resumen

- **CodeSystem** define códigos; **ValueSet** elige los códigos para un uso.
- Un servidor de terminología responde `$lookup`, `$validate-code`,
  `$expand` y `$subsumes`.
- Un **perfil** (StructureDefinition con `derivation: constraint`) restringe
  un recurso; una **guía de implementación** reúne perfiles y terminologías.
- `$validate` revisa un recurso sin guardarlo, con o sin perfil, y el
  resultado está en el `OperationOutcome`.

## Ejecutar este módulo

- **Postman:** carpeta *18 · Terminologías y perfiles* (variable `TXURL` para
  el servidor de terminología).
- **curl:** `curl/taller.sh 18` (necesita los módulos anteriores: ejecuta todo)
- **R:**

  ```r
  # ¿Qué significa un código? Preguntándole al servidor de terminología
  r <- fhir("GET", "CodeSystem/$lookup?system=http://loinc.org&code=8310-5", base = tx_url())
  Filter(function(p) p$name == "display", r$parameter)[[1]]$valueString

  # Validar contra el perfil sin guardar
  v <- fhir("POST", "Patient/$validate?profile=https://f-slg.github.io/aprende-fhir/StructureDefinition/paciente-taller",
            "modulos/18-terminologias-y-perfiles/errores/18e1_paciente_sin_fecha.json")
  vapply(v$issue, function(i) paste(i$severity, i$diagnostics), "")
  ```
