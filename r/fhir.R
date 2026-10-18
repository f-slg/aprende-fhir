# -----------------------------------------------------------------------------
# Aprende FHIR desde cero · Funciones para trabajar con un servidor FHIR desde R
#
# Requiere: install.packages(c("httr2", "jsonlite"))
# Uso:      source("r/fhir.R")
# -----------------------------------------------------------------------------
library(httr2)

# Servidor por defecto: el público de HAPI (solo datos sintéticos).
# Para usar otro: Sys.setenv(FHIRURL = "http://localhost:8080/fhir")
fhir_url <- function() Sys.getenv("FHIRURL", "https://hapi.fhir.org/baseR4")

# Ids guardados durante el taller (patientId, encounterId, ...)
.fhir_ids <- new.env()
fhir_ids <- function() as.list(.fhir_ids)

# Reemplaza los marcadores {{variable}} por los ids guardados
fhir_sustituir <- function(texto) {
  for (var in ls(.fhir_ids)) {
    texto <- gsub(paste0("{{", var, "}}"), get(var, envir = .fhir_ids), texto, fixed = TRUE)
  }
  texto
}

#' Enviar una petición FHIR
#'
#' @param metodo "GET", "POST", "PUT" o "DELETE".
#' @param ruta Ruta relativa al servidor, por ejemplo "Patient" o
#'   "Patient/{{patientId}}/_history". Los marcadores se reemplazan.
#' @param archivo Archivo JSON con el cuerpo de la petición (POST y PUT).
#' @param guarda Nombre con el que guardar el id del recurso creado.
#' @return La respuesta del servidor como lista de R.
fhir <- function(metodo, ruta = "", archivo = NULL, guarda = NULL) {
  url <- paste0(fhir_url(), if (nzchar(ruta)) paste0("/", fhir_sustituir(ruta)))
  req <- request(url) |>
    req_method(metodo) |>
    req_headers(Accept = "application/fhir+json") |>
    req_error(is_error = function(resp) FALSE)
  if (!is.null(archivo)) {
    cuerpo <- fhir_sustituir(paste(readLines(archivo, encoding = "UTF-8", warn = FALSE),
                                   collapse = "\n"))
    req <- req_body_raw(req, cuerpo, type = "application/fhir+json")
  }
  resp <- req_perform(req)
  contenido <- resp_body_json(resp, simplifyVector = FALSE)
  if (resp_status(resp) >= 300) {
    mensajes <- vapply(contenido$issue %||% list(), function(i) i$diagnostics %||% "", "")
    stop("El servidor respondió ", resp_status(resp), ":\n", paste(mensajes, collapse = "\n"),
         call. = FALSE)
  }
  if (!is.null(guarda)) assign(guarda, contenido$id, envir = .fhir_ids)
  invisible(contenido)
}

# Atajos
fhir_crear      <- function(tipo, archivo, guarda = NULL) fhir("POST", tipo, archivo, guarda)
fhir_leer       <- function(ruta) fhir("GET", ruta)
fhir_actualizar <- function(ruta, archivo) fhir("PUT", ruta, archivo)
fhir_buscar     <- function(consulta) fhir("GET", consulta)

# Convierte un Bundle de búsqueda en una tabla con los campos que elijas
#   campos: lista con nombre = función que recibe el recurso
fhir_tabla <- function(bundle, campos = list(id = function(r) r$id)) {
  recursos <- lapply(bundle$entry %||% list(), function(e) e$resource)
  if (!length(recursos)) return(data.frame())
  filas <- lapply(recursos, function(r) {
    as.data.frame(lapply(campos, function(f) f(r) %||% NA), stringsAsFactors = FALSE)
  })
  do.call(rbind, filas)
}
