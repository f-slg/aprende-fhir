# Módulo 09 · Procedimientos

[← Módulo 08](../08-anatomia-patologica/README.md) · [Inicio](../../README.md) · [Módulo 10 →](../10-medicamentos/README.md)

## Objetivos

- Registrar una cirugía con `Procedure`.
- Enlazar el procedimiento con su motivo (`reasonReference`).
- Completar el registro con el resultado y el seguimiento.

## El caso

El 10 de junio de 2025 se realiza una **mastectomía parcial** de la mama
izquierda. Al terminar se registra el procedimiento. Después se agrega el
resultado (exitoso, márgenes libres) y el plan de seguimiento.

## Conceptos clave

- **`Procedure`**: algo que se *hizo* al paciente (cirugía, curación,
  colocación de un catéter). Lo que se *pide* hacer es un `ServiceRequest`.
- **`reasonReference`**: apunta a la `Condition` que motivó el procedimiento:
  el cáncer de mama del módulo 08.
- **`performer.onBehalfOf`**: quién lo hizo y en nombre de qué organización.
- **`outcome`** y **`followUp`**: el resultado y las indicaciones posteriores.

## Ejercicios

### 09a · La cirugía

Registra la mastectomía parcial (SNOMED `64368001`), con categoría
quirúrgica, fecha, cirujana, hospital, motivo y sitio anatómico.

Solución: [`09a_procedure_mastectomia.json`](soluciones/09a_procedure_mastectomia.json)

### 09b · Resultado y seguimiento

Agrega `outcome` (exitoso, `385669000`), `followUp` y una nota sobre los
márgenes.

Solución: [`09b_procedure_actualizar.json`](soluciones/09b_procedure_actualizar.json)

## Para pensar

En este caso, la cirujana es la misma médica del módulo 04. En la realidad
serían personas distintas: ¿qué recursos crearías para modelar al equipo
quirúrgico (cirujano, anestesiólogo, instrumentista)?

## Ejecutar este módulo

- **Postman:** carpeta *09 · Procedimientos*.
- **curl:** `curl/taller.sh 09`
- **R:** `fhir_crear("Procedure", "modulos/09-procedimientos/soluciones/09a_procedure_mastectomia.json", guarda = "procedureId")`
