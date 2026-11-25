# Components

All SVGs are in `assets/`, stroke #F2EFE8 1.5, fill none unless noted. Open and hand-clean; edit freely.

| Component | File / recipe | Rules |
|---|---|---|
| Instrument | `assets/instruments/double-bass.svg`, `piano.svg`, `drums.svg`, `saxophone.svg` | Line only. Keep the visual stroke at 1.5 px when scaling (set stroke-width = 1.5 / scale). One per axis. Sway slightly in motion, pivot at the foot. |
| Halo | `assets/halo.svg`, `halo-<axis>.svg` | Faint radial glow behind ONE instrument or person. Radius 460-520. Max .30. Breathes (scale +/-6%) and pulses on 2 and 4. |
| Staff | `assets/notation/staff.svg` | 5 lines, 24 px apart, 1 px, 35% opacity. Usually in the lower third, full width. |
| Notes | `assets/notation/note-quarter.svg`, `note-half.svg`, `note-whole.svg` | Oval head rx 14 ry 10 rotated -20 degrees; stem 68 px on the right side going up. Filled = ink. Open = outline. |
| Cymbal / hit | `note-head-x.svg`, `hit-accent.svg` | X head for cymbals; accent ">" above a hit on beats 2 and 4. |
| Chord | `chord.svg` | 3-6 stacked heads, one stem. A chord = a combination of capabilities. |
| Beamed eighths | `eighths-beam.svg` | Rhythm or cadence; beam 5 px. A label can sit on the second note (on the "and"). |
| Walking line | `walking-line.svg` | Quarter notes rising and falling: progress over time. |
| Label | Geist Mono 500, 28 px, UPPERCASE, .12em | Names, roles, axes, steps. Optional thin leader line (1 px, ink at .5). |
| Phrase | Inter Tight 300, 56-76 px | One serif accent word (Instrument Serif Italic 1.35x). |
| Outlined title | Instrument Serif Italic 260 px | stroke ink 1.5, fill none, round joins; draw-on in motion. |
| Person | Circle 220 px + ring 236 px; B/W photo (grayscale(1) contrast(1.1)) | Placeholder = line silhouette. Label "NAME - ROLE" below. Never color photos. |
| Dot field | seeded random dots r 1.5-3.3, ink at .35-.95 | Data as points (map or distribution), hubs as 9 px dots with a 24 px ping ring. Use a seeded PRNG, never fully random per frame. |
| Grain | `assets/textures/grain.svg` | Overlay at 6%; plus black vignette. |
| Logo | none | Documented gap: place the current logo from the official brand source, warm white, on the closing. |

Concept -> notation: step = note; combination = chord; emphasis = accent or open note; rhythm = beamed eighths; progress = walking line; team in sync = four instruments on one staff.
