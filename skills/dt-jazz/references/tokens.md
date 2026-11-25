# Tokens

Source of truth: `tokens/tokens.json` (list format) and `tokens/tokens.css` (CSS variables). Values below are the same.

## Color
| Name | Value | Use |
|---|---|---|
| bg | #0B0B0D | Canvas. Always with grain (6%) and a black-only vignette (inner .62, outer opacity .38) |
| ink | #F2EFE8 | Every line, note head, headline, label. 16:1 on bg |
| ink-soft | #A9A59C | Secondary text, captions. 7.6:1 |
| ink-faint | #6F6C66 | Decorative only (3.5:1). Never text |
| staff | rgba(242,239,232,.35) | Staff lines |
| hairline | rgba(242,239,232,.18) | Frames, outlines |

### Halos (one pair per axis; center to edge)
| Axis | Instrument | Center | Edge |
|---|---|---|---|
| Capture | double bass | #7FB8E6 sky | #A99BE0 lilac |
| Intelligence | piano | #A99BE0 lilac | #E59BC0 rose |
| Delivery | drums | #F2B48C peach | #EE7F6E coral |
| Innovation | saxophone | #E59BC0 rose | #EE7F6E coral |

Radial gradient stops: 0 -> center color at opacity .30; .55 -> edge color at .13; 1 -> edge color at 0. Radius 460-520 px on 1080p. Never above .30.

## Type (1920x1080 canvas)
| Style | Family | Size | Weight | Notes |
|---|---|---|---|---|
| display | Instrument Serif Italic | 260 | 400 | Outlined (stroke 1.5, fill none), line-height 1 |
| accent | Instrument Serif Italic | 1.35 x phrase | 400 | One word per phrase, line-height .8 |
| phrase-lg / phrase / phrase-sm | Inter Tight | 76 / 60 / 56 | 300 | tracking -0.01em, lh 1.1 |
| label | Geist Mono | 28 | 500 | UPPERCASE, tracking .12em |
| caption | Geist Mono | 24 | 400 | ink-soft |
| eyebrow | Geist Mono | 22 | 500 | UPPERCASE, ink-soft, section headers |
| body | Inter Tight | 32 | 300 | lh 1.45, max ~60 characters per line |
For other canvas sizes scale proportionally (e.g. 1280x720 = x0.667).

## Line, spacing, radius
- stroke: main 1.5, detail 1, fine 0.66 (px at 1080p). Round caps and joins.
- spacing: 8 16 24 32 48 64 96 120 144. Margins 120 sides / 96 top / 48 footer.
- radius: none (default), 4, 12, pill, round (people).
- Grain: feTurbulence fractalNoise baseFrequency .85, 2 octaves, seed 11, opacity .06.
- Person: circle 220 px, ring 236 px (1 px), box 240.
