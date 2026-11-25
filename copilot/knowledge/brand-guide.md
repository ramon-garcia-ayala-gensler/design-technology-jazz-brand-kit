# Design Technology · Jazz — Brand guide / Guía de marca

Bilingual: English first, Español después. Style names: "DT Jazz", "Design Technology Jazz", "Amplify style".

---
# English

## 1. Idea
A team is a jazz band. Every axis of work is an instrument, every concept is written as music, and everything lives on a
dark jazz-club stage drawn with a single thin line. The concept in one line: "a line becomes a band".

| Axis | Instrument | Halo (center to edge) |
|---|---|---|
| Capture (reality to data) | Double bass | sky #7FB8E6 to lilac #A99BE0 |
| Intelligence (data to decisions) | Piano | lilac #A99BE0 to rose #E59BC0 |
| Delivery (everyone lands together) | Drums | peach #F2B48C to coral #EE7F6E |
| Innovation (improvise, then ship) | Saxophone | rose #E59BC0 to coral #EE7F6E |

The axis names are examples; any four disciplines can take the four instruments.

## 2. Color
| Token | Value | Use |
|---|---|---|
| bg | #0B0B0D | Canvas, always with grain at 6% and a black-only vignette |
| ink | #F2EFE8 | Lines, note heads, headlines, labels (16:1 on bg) |
| ink-soft | #A9A59C | Secondary text and captions (7.6:1) |
| ink-faint | #6F6C66 | Decorative only, never text (3.5:1) |
| staff | ink at 35% | Five staff lines, 1 px |
| halo pairs | see table above | A faint glow behind ONE element. Max 30% opacity at the center, 13% mid radius, 0 at the edge |

No gradient backgrounds, no orbs, no colored fills. Color lives only in halos.

## 3. Typography
- **Instrument Serif Italic**: the accent. One key word per phrase at 1.35x the phrase size (e.g. "Everyone lands together" with "together" in serif), big outlined titles (260 px, stroke 1.5 px, no fill), big numerals.
- **Inter Tight Light (300)**: phrases at 56-76 px (1080p), body at 32 px, line height 1.1 for phrases, 1.45 for body, tracking -0.01em for phrases.
- **Geist Mono Medium (500)**: labels, uppercase, 28 px, tracking 0.12em. Names, roles, axis names, step names, captions. Mono 400 at 24 px for notes.
- Minimum text on screen: 48 px for phrases at 1080p (readable at 6 m), 24 px for captions.
- PowerPoint/Word need the TTF files in `fonts/ttf/`; web uses the WOFF2 in `fonts/`.

## 4. Line and components
- Line: 1.5 px warm white, round caps and joins; 1 px for details; 0.66 px for strings and keys. No fills.
- **Instruments** (`assets/instruments/*.svg`): drawn as line art; use at a size where the line stays 1.5 px.
- **Staff**: 5 lines, 24 px apart, 1 px, 35% opacity, usually across the lower third.
- **Notation** (`assets/notation/*.svg`): quarter/half/whole notes, X head (cymbal), chord (5 stacked heads), hit with accent ">", beamed eighths, walking line. Heads are ovals tilted -20 degrees (rx 14, ry 10), stems 68 px.
- **Halo**: radial gradient circle, radius 460-520 px at 1080p, one per axis element.
- **Person**: circle 220 px with a thin ring at 236 px, black-and-white photo (grayscale + contrast 1.1), mono label "NAME · ROLE" beneath.
- **Label**: mono uppercase text, optionally with a thin line to what it names.
- **Phrase**: Inter Tight 300 with one serif accent word.
- **Grain**: `assets/textures/grain.svg` (feTurbulence, seed 11, baseFrequency 0.85) at 6% opacity.

## 5. Concepts as notation
| Idea | Notation |
|---|---|
| A step / a task | A note on the staff |
| A combination of capabilities | A chord (stacked notes) |
| An emphasis or milestone | An accent ">" or a hollow note |
| A rhythm / cadence | A group of beamed eighths |
| Progress over time | A walking line of notes rising and falling |
| A team working in sync | Four instruments on one staff |
Never use bar charts, isometric diagrams or generic line icons. If a concept does not fit, use a mono label.

## 6. Layout
Canvas 1920x1080. Margins: 120 px sides, 96 px top, 48 px footer. Flush-left text, generous empty space. One idea per slide.
Text that shares a slide appears in reading order and accumulates (title, label, phrase, caption).

## 7. Motion
110 BPM, 4/4 (beat = 545 ms, bar = 2.18 s). Entrances land on the "and" of the beat (+273 ms); hits and bounces on beats 2 and 4;
cuts on beat 1; lines draw in a whole number of beats. Nothing is still: instruments sway slightly, halos breathe, small pulses on 2 and 4.
Honor "reduce motion".

## 8. Voice
Plain, warm, confident. Phrases of 6-12 words. Say what it does and for whom. Metaphors from music, used lightly ("lands together", "in time", "improvise").

## 9. Do / Don't
Do: dark canvas, one thin line, mono labels, one serif word, notation, faint halos, grain, generous space.
Don't: bar charts, isometric 3D, clip-art icons, stock photos, colored photos, gradient backgrounds, orbs, drop shadows, lens flares, shaking cameras, crossfades, more than one serif word per phrase, text below 24 px, invented logos or figures.

## 10. Logo
The logo is not part of this kit. Place the current logo from the official brand source in the reserved space of the closing slide, in warm white on the dark canvas.

---
# Español

## 1. Idea
Un equipo es una banda de jazz. Cada eje de trabajo es un instrumento, cada concepto se escribe como música y todo vive en
el escenario oscuro de un club de jazz, dibujado con una sola línea fina. En una línea: «una línea se vuelve banda».

| Eje | Instrumento | Halo (centro a borde) |
|---|---|---|
| Capture (realidad a datos) | Contrabajo | cielo #7FB8E6 a lila #A99BE0 |
| Intelligence (datos a decisiones) | Piano | lila #A99BE0 a rosa #E59BC0 |
| Delivery (todos aterrizan juntos) | Batería | durazno #F2B48C a coral #EE7F6E |
| Innovation (improvisa y luego entrega) | Saxofón | rosa #E59BC0 a coral #EE7F6E |

Los nombres de eje son ejemplos; cualquier cuarteto de disciplinas puede usar los cuatro instrumentos.

## 2. Color
Fondo #0B0B0D con grano al 6 % y viñeta solo negra; tinta #F2EFE8 para líneas, cabezas de nota, titulares y etiquetas;
tinta suave #A9A59C para texto secundario (7.6:1); #6F6C66 solo decorativo. Pentagrama: tinta al 35 %. Los halos son el único color:
tenues (máximo 30 % en el centro, 13 % a media distancia, 0 en el borde) y siempre detrás de UN elemento.
Sin fondos con degradado, sin orbes, sin rellenos de color.

## 3. Tipografía
- **Instrument Serif Itálica**: el acento. Una palabra clave por frase a 1.35× el tamaño; títulos grandes en contorno (260 px, línea 1.5 px, sin relleno); cifras grandes.
- **Inter Tight Light (300)**: frases de 56-76 px (a 1080p) y cuerpo de 32 px; interlínea 1.1 en frases y 1.45 en cuerpo.
- **Geist Mono Medium (500)**: etiquetas en mayúsculas, 28 px, espaciado 0.12em: nombres, roles, ejes, pasos y pies.
- Mínimo en pantalla: 48 px para frases (se lee a 6 m), 24 px para pies.
- PowerPoint y Word necesitan los TTF de `fonts/ttf/` (doble clic, Instalar); la web usa los WOFF2 de `fonts/`.

## 4. Línea y componentes
Línea blanca cálida de 1.5 px con terminaciones redondas; 1 px en detalles; 0.66 px en cuerdas y teclas; sin rellenos.
Instrumentos en `assets/instruments/`; pentagrama de 5 líneas a 24 px, 1 px, 35 %; notación en `assets/notation/` (cabezas ovaladas
inclinadas -20°, plicas de 68 px); halo radial de 460-520 px; persona = círculo de 220 px con anillo de 236 px, foto en blanco y negro
y etiqueta mono «NOMBRE · ROL»; grano en `assets/textures/grain.svg` al 6 %.

## 5. Conceptos como notación
Paso o tarea = nota. Combinación de capacidades = acorde. Énfasis o hito = acento «>» o nota hueca. Ritmo = corcheas unidas por una barra.
Avance en el tiempo = línea de notas que sube y baja. Equipo en sincronía = cuatro instrumentos en un pentagrama.
Nunca barras, planos isométricos ni íconos genéricos; si un concepto no cabe, va como etiqueta mono.

## 6. Composición
Lienzo 1920×1080. Márgenes de 120 px a los lados, 96 px arriba. Texto alineado a la izquierda, mucho aire, una idea por lámina.
Los textos que comparten pantalla entran en orden de lectura y se acumulan.

## 7. Movimiento
110 BPM en 4/4 (tiempo 545 ms, compás 2.18 s). Las entradas caen en el «y» del tiempo (+273 ms); golpes y rebotes en 2 y 4; cortes en el 1;
las líneas se dibujan en un número entero de tiempos. Nada queda quieto: balanceo leve, halos que respiran, pulsos en 2 y 4. Respeta «reducir movimiento».

## 8. Voz
Clara, cálida y segura. Frases de 6 a 12 palabras. Metáforas de música con ligereza («aterrizan juntos», «a tiempo», «improvisar»).

## 9. Sí / No
Sí: lienzo oscuro, una línea fina, etiquetas mono, una palabra serif, notación, halos tenues, grano, aire.
No: barras, 3D isométrico, íconos clip-art, fotos de stock o a color, degradados de fondo, orbes, sombras, destellos, cámara temblorosa,
fundidos cruzados, más de una palabra serif por frase, texto menor de 24 px, logos o cifras inventados.

## 10. Logo
El logo no forma parte de este kit. Coloca el logo vigente desde la fuente oficial de marca en el espacio reservado del cierre, en blanco cálido sobre fondo oscuro.
