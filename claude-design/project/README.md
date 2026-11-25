# DT Jazz

**Design Technology · Jazz** is a dark jazz-club, line-art system: a team is a band, each axis of work is an instrument, and every concept is written as musical notation on a single thin line.

> "A line becomes a band."

## Principles

1. **One line.** The only graphic resource is a warm-white line (`ink` #F2EFE8) at 1.5 px (1 px details, 0.66 px fine). No fills except note heads and text.
2. **Dark stage.** Canvas `bg` #0B0B0D with fine film grain (6%) and a black-only vignette. Never a gradient background.
3. **Each axis is an instrument.** Capture = double bass, Intelligence = piano, Delivery = drums, Innovation = saxophone (names are examples; any four disciplines work).
4. **Notation, not diagrams.** Step = note, combination = chord, emphasis = accent, rhythm = beamed eighths, progress = walking line. Never bar charts, isometric diagrams or generic icons.
5. **Faint halos.** One radial glow per axis, max opacity .30, tied to the element it belongs to. It is the only color.
6. **One serif word.** Instrument Serif Italic carries a single key word per phrase (or outlined titles); Inter Tight 300 carries phrases; Geist Mono 500 uppercase carries labels.
7. **Nothing is still.** Motion lives on a 110 BPM grid: entrances on the "and", hits on beats 2 and 4, cuts on beat 1.

## Color

Tokens in `tokens.json`: `bg`, `ink`, `ink-soft` (secondary text, 7.6:1), `ink-faint` (decorative only), `staff`, `hairline`, and eight halo tokens: `halo-<axis>-center` / `halo-<axis>-edge`.

| Axis | Center | Edge |
|---|---|---|
| Capture | #7FB8E6 sky | #A99BE0 lilac |
| Intelligence | #A99BE0 lilac | #E59BC0 rose |
| Delivery | #F2B48C peach | #EE7F6E coral |
| Innovation | #E59BC0 rose | #EE7F6E coral |

Halo stops: center .30, 55% radius .13, edge 0. Text contrast is at least 4.5:1.

## Typography

| Style | Family | Size (1080p) | Use |
|---|---|---|---|
| display | Instrument Serif Italic | 260 | Outlined titles (stroke 1.5, no fill) |
| accent | Instrument Serif Italic | 1.35x phrase | One key word per phrase |
| phrase-lg / phrase / phrase-sm | Inter Tight 300 | 76 / 60 / 56 | Statements, never below 48 |
| label | Geist Mono 500 | 28 | UPPERCASE, tracking .12em |
| body | Inter Tight 300 | 32 | Slide body, max ~60 characters per line |

## Components

- **Instrument**, **Halo**, **Staff**, **Notation**: the visual vocabulary.
- **PersonRing**: black-and-white circle (220 px) with a ring (236 px) and a mono label.
- **Label**, **Phrase**: the type system in use.
- **SlideCover**, **SlideSection**: 1920x1080 slide patterns.

Instrument SVGs are assets under `assets/Instruments/` (stroke is #F2EFE8; they are single-ink marks designed for the dark `bg`, so place them on it).

## Layout and spacing

1920x1080 canvas. Margins 120 px sides, 96 px top, 48 px footer; spacing scale 8, 16, 24, 32, 48, 64, 96, 120, 144. Flush-left text, generous empty space, one idea per slide. Radii are minimal: square by default, round only for people.

## Motion

Beat 545 ms, "and" +273 ms, bar 2.18 s. Sway +/-0.7 degrees, halos breathe, pulses on 2 and 4. Respect reduced motion. Details in the repo skill (`skills/dt-jazz/references/motion.md`).

## Voice

Plain, warm, confident. Phrases of 6-12 words. Light music metaphors ("lands together", "in time", "improvise").

## Do / Don't

Do: dark canvas, one thin line, mono labels, one serif word, notation, faint halos, grain, space.
Don't: bar charts, isometric 3D, clip-art icons, stock or color photos, gradient backgrounds, orbs, shadows, lens flares, invented logos or figures, text below 24 px.

## Logo

Not included. Place the current logo from the official brand source in the reserved space of the closing slide, in warm white.

## Fonts

Instrument Serif Italic, Inter Tight (variable) and Geist Mono 400/500, all SIL OFL 1.1 (see the repo `fonts/LICENSES.md`).
