# Motion

Grid: 110 BPM, 4/4. Beat 545.45 ms, "and" +272.7 ms, bar 2181.8 ms. Express positions as bar.beat (e.g. 9.2y = the "and" of beat 2 of bar 9) and never as loose seconds.

| Event | Where | Why |
|---|---|---|
| Scene entrance, hard cuts | Beat 1 | The scene "arrives" with the music; no crossfades |
| Secondary elements (labels, captions) | The "and" | Swing feel: slightly late on purpose |
| Hits, bounces, pulses | Beats 2 and 4 | The backbeat |
| Response to a voice | 1-2 beats after it ends | Call and response |
| Line draw-on | 1, 2 or 4 whole beats | Stays on the grid |

## Nothing is still
- Instrument sway: rotation +/-0.7 degrees and 3 px bob over one bar, pivot at the foot.
- Halo breathing: scale .96-1.05 over two bars, slow drift (a few px), a small pulse on 2 and 4. Opacity never above .30 of the skin.
- Ring or hub pulse: +2.5% (ring) or +50% ping on beats 2 and 4.
- Staff may carry a very faint wave (about 2 px) that crosses once per bar.

## Easing
Entrances: spring with low damping (about 7% overshoot) or exponential-out; exits: faster than entrances. Blur only on fast moves. Never shake the camera, split RGB, add lens flares, particle bursts or crossfades.

## Text reveals
Phrases reveal word by word, each word rising inside a clipped box (0.1 beat between words). Labels type in letter by letter over about half a beat.

## Determinism and accessibility
Motion is a function of time (seeded noise, no per-frame random). Honor `prefers-reduced-motion`: show the final state, no loops.
CSS vars used in the template: --beat 545.45ms, --and 272.7ms, --bar 2181.8ms.
