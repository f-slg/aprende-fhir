# -----------------------------------------------------------------------------
# Aprende FHIR desde cero · Ejecuta todo el taller desde R, en orden
#
# Uso (desde la carpeta del repositorio):
#   Rscript r/taller.R                    # servidor público de HAPI
#   FHIRURL=http://localhost:8080/fhir Rscript r/taller.R
#   Rscript r/taller.R 06                 # solo hasta el módulo 06
# -----------------------------------------------------------------------------
source("r/fhir.R")
args <- commandArgs(trailingOnly = TRUE)
hasta <- if (length(args)) args[[1]] else "19"

pasos <- jsonlite::fromJSON("herramientas/pasos.json", simplifyVector = FALSE)$pasos
cat("Servidor:", fhir_url(), "\n")
for (p in pasos) {
  if (substr(p$modulo, 1, 2) > hasta) break
  rechazo <- identical(p$espera$servidor, "rechaza")
  r <- fhir(p$metodo, p$ruta, p$archivo, if (!rechazo) p$guarda, espera_rechazo = rechazo)
  extra <- if (!is.null(p$guarda) && !rechazo) paste0(" -> ", p$guarda, " = ", r$id) else ""
  if (rechazo) extra <- paste0(" (rechazado, como se esperaba: ",
                               substr(r$issue[[1]]$diagnostics, 1, 70), "...)")
  cat(sprintf("OK  %-4s %-6s %s%s\n", p$id, p$metodo, p$nombre, extra))
}
cat("\nListo. Expediente completo:",
    paste0(fhir_url(), "/Patient/", fhir_ids()$patientId, "/$everything"), "\n")
