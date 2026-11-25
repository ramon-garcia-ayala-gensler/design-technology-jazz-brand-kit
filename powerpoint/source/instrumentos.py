"""Exporta los 4 instrumentos de linea (instrumentos.data.ts) a SVG y PNG transparentes (linea blanca calida)."""
import re, sys, pathlib, fitz

SRC = pathlib.Path(sys.argv[1])  # instrumentos.data.ts
OUT = pathlib.Path(sys.argv[2])
INK = "#F2EFE8"
SW = 2.6  # grosor en unidades del viewBox (~1.3 pt a la escala usada en las laminas)
NAMES = {"capture": "contrabajo", "intelligence": "piano", "delivery": "bateria", "innovation": "saxofon"}
txt = SRC.read_text(encoding="utf8")
OUT.mkdir(parents=True, exist_ok=True)
for key, nombre in NAMES.items():
    m = re.search(key + r": \{ w: (\d+), h: (\d+), els: \[(.*?)\] \},?\n", txt, re.S)
    w, h, body = int(m[1]), int(m[2]), m[3]
    paths = []
    for line in body.strip().splitlines():
        d = re.search(r"d:'([^']+)'", line)
        if not d: continue
        a = f'<path d="{d[1]}"'
        sw = SW
        if "w:'fine'" in line: sw = SW * 0.66
        tf = re.search(r"tf:'([^']+)'", line)
        if tf: a += f' transform="{tf[1]}"'
        if "fijo:true" in line:
            da = re.search(r"dash:'([^']+)'", line)[1]; sw = float(re.search(r"sw:([\d.]+)", line)[1])
            a += f' stroke-dasharray="{da}" stroke-opacity="0.6"'
            if "cap:'butt'" in line: a += ' stroke-linecap="butt"'
        a += f' stroke-width="{sw:.2f}"/>'
        paths.append(a)
    pad = 6
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{-pad} {-pad} {w+2*pad} {h+2*pad}" width="{w+2*pad}" height="{h+2*pad}" '
           f'fill="none" stroke="{INK}" stroke-linecap="round" stroke-linejoin="round">' + "".join(paths) + "</svg>")
    (OUT / f"{nombre}.svg").write_text(svg, encoding="utf8")
    doc = fitz.open(str(OUT / f"{nombre}.svg"))
    pg = doc[0]
    z = 1400 / pg.rect.height if pg.rect.height > pg.rect.width else 1400 / pg.rect.width
    pix = pg.get_pixmap(matrix=fitz.Matrix(z, z), alpha=True)
    pix.save(str(OUT / f"{nombre}.png"))
    print(nombre, w, h, pix.width, pix.height)
