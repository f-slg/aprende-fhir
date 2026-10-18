# -----------------------------------------------------------------------------
# Aprende FHIR desde cero · Logo (hexágono)
#
# Misma familia visual que geoecu, pobecu y Agenda FHIR (azul marino y
# dorado). Unas llaves de JSON al centro, enlazadas con recursos alrededor,
# como las referencias que unen los recursos del taller. No usa marcas de HL7.
#
# Uso: Rscript herramientas/logo.R   (genera imagenes/logo.png)
# -----------------------------------------------------------------------------
library(grid)

azul   <- "#0F2233"
azul2  <- "#1B3A52"
dorado <- "#F2B705"
blanco <- "#F4F6F8"
teal   <- "#3FB8A6"

alto <- 1200
ancho <- round(alto * sqrt(3) / 2)
dir.create("imagenes", showWarnings = FALSE)
png("imagenes/logo.png", width = ancho, height = alto, bg = "transparent",
    type = "cairo", antialias = "subpixel")

hexagono <- function(r) {
  ang <- pi / 2 + (0:5) * pi / 3
  list(x = 0.5 + r * cos(ang) * alto / ancho / 2, y = 0.5 + r * sin(ang) / 2)
}
h_ext <- hexagono(0.995); h_med <- hexagono(0.955); h_int <- hexagono(0.925)
grid.newpage()
grid.polygon(h_ext$x, h_ext$y, gp = gpar(fill = dorado, col = NA))
grid.polygon(h_med$x, h_med$y,
             gp = gpar(col = NA, fill = radialGradient(c(azul2, azul),
                                                       cx1 = 0.5, cy1 = 0.6, r2 = 0.7)))
grid.polygon(h_int$x, h_int$y,
             gp = gpar(fill = NA, col = adjustcolor(dorado, 0.35), lwd = 1.6))

# --- Red de recursos -------------------------------------------------------------
pushViewport(viewport(x = 0.5, y = 0.585, width = 0.62, height = 0.62 * ancho / alto * 1.0))
cx <- 0.5; cy <- 0.5
ang <- pi / 2 + seq(0, 2 * pi, length.out = 7)[-7]
rad <- 0.39
nodos <- data.frame(x = cx + rad * cos(ang), y = cy + rad * sin(ang),
                    col = c(dorado, blanco, teal, dorado, blanco, teal))
# Enlaces: del centro a cada nodo y entre algunos vecinos
for (i in seq_len(nrow(nodos))) {
  grid.lines(c(cx, nodos$x[i]), c(cy, nodos$y[i]),
             gp = gpar(col = adjustcolor(blanco, 0.55), lwd = 7, lineend = "round"))
}
for (par in list(c(1, 2), c(3, 4), c(5, 6))) {
  grid.lines(nodos$x[par], nodos$y[par],
             gp = gpar(col = adjustcolor(blanco, 0.3), lwd = 5, lty = "22", lineend = "round"))
}
for (i in seq_len(nrow(nodos))) {
  grid.circle(nodos$x[i], nodos$y[i], r = 0.075,
              gp = gpar(fill = nodos$col[i], col = azul, lwd = 8))
}
# Centro: llaves de JSON
grid.roundrect(cx, cy, width = 0.36, height = 0.30, r = unit(0.06, "snpc"),
               gp = gpar(fill = azul, col = blanco, lwd = 9))
grid.text("{ }", cx, cy - 0.005, gp = gpar(col = dorado, fontsize = 118, fontface = "bold"))
popViewport()

# --- Nombre ----------------------------------------------------------------------
tam <- 122
g1 <- textGrob("aprende", gp = gpar(fontsize = tam, fontface = "bold"))
g2 <- textGrob("fhir", gp = gpar(fontsize = tam, fontface = "bold"))
w1 <- convertWidth(grobWidth(g1), "npc", valueOnly = TRUE)
w2 <- convertWidth(grobWidth(g2), "npc", valueOnly = TRUE)
x0 <- 0.5 - (w1 + w2) / 2
grid.text("aprende", x = x0, y = 0.235, just = "left",
          gp = gpar(fontsize = tam, fontface = "bold", col = blanco))
grid.text("fhir", x = x0 + w1, y = 0.235, just = "left",
          gp = gpar(fontsize = tam, fontface = "bold", col = dorado))

invisible(dev.off())
message("Escrito: imagenes/logo.png")
