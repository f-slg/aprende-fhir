# Módulo 08 · Anatomía patológica

[← Módulo 07](../07-documentos-clinicos/README.md) · [Inicio](../../README.md) · [Módulo 09 →](../09-procedimientos/README.md)

## Objetivos

- Describir una lesión con `BodyStructure` y una muestra con `Specimen`.
- Registrar resultados y **corregirlos** (`amended`) dejando rastro.
- Agrupar resultados en un `DiagnosticReport`.
- Registrar un diagnóstico basado en un informe.

## El caso

Meses después, Luis consulta por un nódulo en la mama izquierda. El cáncer de
mama en hombres es poco frecuente, pero existe. El 6 de mayo de 2025 se toma
una **biopsia**. El 8 de mayo se informa un tumor de 2,5 cm, medida que se
corrige a **3,5 cm** al revisar la pieza. El 12 de mayo la
inmunohistoquímica muestra **receptor de estrógeno positivo** (90 %, Allred
8). El informe concluye **carcinoma ductal infiltrante** de mama izquierda.

## Conceptos clave

- **`BodyStructure`**: una estructura anatómica concreta *del paciente* (este
  tumor), con su morfología y ubicación. Las observaciones lo referencian con
  `focus`.
- **`Specimen`**: la muestra física. Tiene `status` (`available`,
  `unavailable`...) y datos de la toma en `collection`.
- **Corregir un resultado**: no se borra ni se crea otro, se hace `PUT` del
  mismo recurso con `status = amended`. El historial (`_history`) conserva la
  versión anterior: así se ve qué se informó y cuándo se corrigió.
- **`DiagnosticReport`** agrupa los resultados (`result`), la muestra, la
  conclusión en texto y codificada (`conclusionCode`).
- **`Condition.evidence.detail`** enlaza el diagnóstico con el informe que lo
  sustenta.

## Ejercicios

| Paso | Qué hacer | Solución |
|---|---|---|
| 08a | Registrar el tumor (morfología SNOMED `82711006`, mama izquierda `80248007`) | [`08a`](soluciones/08a_bodystructure_tumor.json) |
| 08b | Precisar la ubicación (cuadrante superior externo, lateralidad) | [`08b`](soluciones/08b_bodystructure_actualizar.json) |
| 08c | Registrar la biopsia (`Specimen`, tejido tumoral `258435002`) | [`08c`](soluciones/08c_specimen_crear.json) |
| 08d | Marcar la muestra como agotada (`unavailable`) | [`08d`](soluciones/08d_specimen_actualizar.json) |
| 08e | Tamaño del tumor: 2,5 cm, enlazado al tumor y a la muestra | [`08e`](soluciones/08e_observation_tamano_tumor.json) |
| 08f | Corregir a 3,5 cm con `status = amended` y una nota | [`08f`](soluciones/08f_observation_tamano_tumor_actualizar.json) |
| 08g | Receptor de estrógeno positivo (LOINC `85337-4`) | [`08g`](soluciones/08g_observation_receptor_estrogeno.json) |
| 08h | Ampliar el resultado: interpretación y porcentaje | [`08h`](soluciones/08h_observation_receptor_estrogeno_actualizar.json) |
| 08i | Informe de patología (LOINC `11526-1`) con los dos resultados | [`08i`](soluciones/08i_diagnosticreport_patologia.json) |
| 08j | Diagnóstico de cáncer de mama (CIE-10 `C50.9` y SNOMED `254837009`) | [`08j`](soluciones/08j_condition_cancer_mama.json) |

### 08k · El informe con sus resultados

```http
GET {{FHIRURL}}/DiagnosticReport?subject=Patient/{{patientId}}&_include=DiagnosticReport:result
GET {{FHIRURL}}/Observation/{{obsTumorId}}/_history
```

En el historial del tamaño del tumor verás las dos versiones: 2,5 cm (`final`)
y 3,5 cm (`amended`).

## Para pensar

El diagnóstico tiene dos códigos: CIE-10 y SNOMED CT. ¿Para qué sirve cada
uno? Piensa en la estadística de morbilidad frente a la historia clínica.

## Ejecutar este módulo

- **Postman:** carpeta *08 · Anatomía patológica*.
- **curl:** `curl/taller.sh 08`
- **R:** `fhir_leer("Observation/{{obsTumorId}}/_history")$total`
