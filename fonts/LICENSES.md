# Font licenses / Licencias de las fuentes

All four font files in this folder are **web subsets (Latin) in WOFF2** of fonts released under the
**SIL Open Font License 1.1 (OFL)**. You may use, embed, redistribute and modify them, including commercially,
as long as the copyright notice and license travel with them and they are not sold on their own.
Los cuatro archivos son subconjuntos latinos en WOFF2 de fuentes con licencia **SIL OFL 1.1**: se pueden usar,
incrustar y redistribuir (también en proyectos comerciales) conservando el aviso de copyright y la licencia.

| File | Family | Role in the kit | Copyright | Source | License text |
|---|---|---|---|---|---|
| `instrument-serif-latin-400-italic.woff2` | Instrument Serif Italic | Accent word, display, outlined titles | Copyright 2022 The Instrument Serif Project Authors | https://github.com/Instrument/instrument-serif | `licenses/OFL-InstrumentSerif.txt` |
| `inter-tight-latin-wght-normal.woff2` | Inter Tight (variable, wght 100-900) | Phrases (300), body | Copyright 2022 The Inter Project Authors | https://github.com/rsms/inter-tight | `licenses/OFL-InterTight.txt` |
| `geist-mono-latin-400-normal.woff2` | Geist Mono 400 | Notes, captions | Copyright 2024 The Geist Project Authors | https://github.com/vercel/geist-font | `licenses/OFL-GeistMono.txt` |
| `geist-mono-latin-500-normal.woff2` | Geist Mono 500 | Uppercase labels | Copyright 2024 The Geist Project Authors | https://github.com/vercel/geist-font | `licenses/OFL-GeistMono.txt` |

Notes
- The WOFF2 files were obtained as Latin subsets (Fontsource distribution); the OFL texts above were downloaded from
  the upstream repositories (`google/fonts`) and are unmodified. Copyright lines are quoted exactly as they appear there.
- The OFL applies to the fonts only. The rest of this repository is MIT (see `../LICENSE`).
- Reserved Font Names, if declared by the authors, are respected: these files are not renamed.
- Because these are Latin subsets, characters outside Latin (Greek, Cyrillic, CJK...) fall back to system fonts.

## Installable TTF (`ttf/`) for PowerPoint / Word / Copilot

PowerPoint on Windows does not install WOFF2. `ttf/` holds desktop TTF versions **derived from the same WOFF2 files**
with fontTools (WOFF2 decompressed to TTF; Inter Tight's variable axis instanced to static Light 300 and Regular 400,
family names set so both can be installed side by side: "Inter Tight Light" and "Inter Tight"). Same OFL 1.1 license and
copyright as above; they are modified derivatives of the Latin subsets and keep the original authors' notices.
To install: select the files, right-click, "Install for all users" (or double click, Install). Restart PowerPoint.
Los TTF de `ttf/` son para PowerPoint/Word: doble clic en cada archivo y pulsa Instalar.
