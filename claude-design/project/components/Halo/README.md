# Halo

A faint radial glow behind ONE element (an instrument or a person), in the color pair of its axis. It is the only color in the system.

| Axis | Center | Edge |
|---|---|---|
| Capture | sky #7FB8E6 | lilac #A99BE0 |
| Intelligence | lilac #A99BE0 | rose #E59BC0 |
| Delivery | peach #F2B48C | coral #EE7F6E |
| Innovation | rose #E59BC0 | coral #EE7F6E |

- Radial gradient: center opacity .30 (hard ceiling), .13 at 55% of the radius, 0 at the edge. Radius 460-520 px on a 1080p canvas.
- Tied to the element it belongs to. Never a full-slide background, never a decorative orb, never behind plain text.
- In motion it breathes (scale .96-1.05 over two bars) and pulses lightly on beats 2 and 4.
- Asset: `assets/halo.svg` (example in the repo). Tokens: `halo-<axis>-center`, `halo-<axis>-edge`.
