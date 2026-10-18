# -----------------------------------------------------------------------------
# Aprende FHIR desde cero · Primeros pasos en RStudio
#
# 1. Abre aprende-fhir.Rproj en RStudio.
# 2. Instala los paquetes (una sola vez):
#      install.packages(c("httr2", "jsonlite"))
# 3. Ejecuta este archivo línea por línea con Ctrl + Enter.
# -----------------------------------------------------------------------------
source("r/fhir.R")

# Servidor: por defecto el público de HAPI. Para uno local:
# Sys.setenv(FHIRURL = "http://localhost:8080/fhir")
fhir_url()

# ¿Qué versión de FHIR implementa el servidor?
fhir_leer("metadata")$fhirVersion

# Crear el paciente del caso y guardar su id
paciente <- fhir_crear("Patient", "modulos/02-patient/soluciones/02a_patient_crear.json",
                       guarda = "patientId")
paciente$id

# Leerlo de nuevo desde el servidor
fhir_leer("Patient/{{patientId}}")$name[[1]]$text

# Buscar a todos los Paredes y verlos como tabla
paredes <- fhir_buscar("Patient?family=Paredes")
fhir_tabla(paredes, list(
  id = function(r) r$id,
  nombre = function(r) r$name[[1]]$text,
  nacimiento = function(r) r$birthDate
))

# Para ejecutar todo el taller de una vez:
# source("r/taller.R")
