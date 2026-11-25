---
name: dt-jazz
description: Apply the "Design Technology · Jazz" visual style (a.k.a. DT Jazz, Design Technology jazz, Amplify style) to presentations, slide decks, posters, social images, web pages and motion/video. Dark jazz-club line art on #0B0B0D with grain, warm-white 1.5 px line, one faint halo per axis, Instrument Serif italic accent, Inter Tight 300 phrases, Geist Mono uppercase labels, musical notation instead of charts, motion at 110 BPM. Use whenever the user mentions DT Jazz style, Design Technology jazz, Amplify style, jazz band metaphor, or asks for slides, posters or motion in that look.
---

# DT Jazz (Design Technology · Jazz)

A team is a jazz band: each axis is an instrument, concepts are notation, the stage is dark and drawn with one thin line.
Concept in one line: "a line becomes a band".

## Start here
1. Read `references/tokens.md` for exact colors, type and sizes (machine-readable: `tokens/tokens.json`, `tokens/tokens.css`).
2. Read `references/components.md` to pick and place components; reuse the SVGs in `assets/` instead of redrawing them.
3. For decks read `references/slides.md` and start from `templates/slides/index.html` (1920x1080 HTML, 8 layouts, arrow-key navigation).
4. For anything animated read `references/motion.md`.
5. Before delivering, run the checklist in `references/dos-and-donts.md`.

## Non-negotiables
- Metaphor: each axis = an instrument (Capture = double bass, Intelligence = piano, Delivery = drums, Innovation = saxophone). The axis names are examples; any four disciplines map to the four instruments.
- Concepts are notation (notes, chords, accents, beamed eighths, a staff) plus mono labels. Never bar charts, isometric diagrams or generic icons.
- Text that shares a screen accumulates in reading order.
- Halos: faint (max opacity 0.30), tied to the element they belong to, never decorative backgrounds. No gradient backgrounds, no orbs.
- Background #0B0B0D + 6% grain + black vignette. Line #F2EFE8 at 1.5 px (1 px details).
- Text contrast at least 4.5:1; phrases never under 48 px on a 1080p canvas.
- Motion: nothing is still (sway, breathing halos, pulses on beats 2 and 4); entrances on the "and"; hard cuts on beat 1; honor reduced motion.
- Never invent logos, photos, names or figures. Logo = documented gap: "place the current logo from the official brand source".

## Fonts
Instrument Serif Italic (accent), Inter Tight (300 phrases), Geist Mono 500 (labels), all OFL, in `fonts/` (WOFF2). For Office use the TTF in the repo's `fonts/ttf/`.

## Files
- `assets/instruments/{double-bass,piano,drums,saxophone}.svg`, `assets/notation/*.svg`, `assets/halo*.svg`, `assets/textures/grain.svg`
- `tokens/tokens.json`, `tokens/tokens.css`
- `templates/slides/index.html`
