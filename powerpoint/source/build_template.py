"""Genera DT-Jazz.potx (plantilla) y DT-Jazz-ejemplo.pptx (8 laminas) escribiendo el OOXML a mano.

Uso: python build_template.py <carpeta powerpoint>
El mismo modelo de escena alimenta a preview.py (render aproximado con Pillow cuando no hay LibreOffice).
Coordenadas en px sobre un lienzo de 1920x1080 (1 px = 6350 EMU; 1 px = 0.5 pt).
"""
import sys, zipfile, pathlib
from xml.sax.saxutils import escape
from PIL import Image, ImageDraw

OUT = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(".")
INST = OUT / "assets" / "instrumentos"
E = 6350
W, H = 1920, 1080

NS = ('xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
      'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
      'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"')
HDR = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'

COLORS = dict(dk1="0B0B0D", lt1="F2EFE8", dk2="1A1A1F", lt2="B9B4AA", accent1="7FB8E6", accent2="A99BE0",
              accent3="E59BC0", accent4="F2B48C", accent5="EE7F6E", accent6="F2EFE8", hlink="7FB8E6", folHlink="A99BE0")
# halos por eje: (de, a)
HALO = {"capture": ("accent1", "accent2"), "intelligence": ("accent2", "accent3"),
        "delivery": ("accent4", "accent5"), "innovation": ("accent3", "accent5")}


def px(v): return int(round(v * E))


def xfrm(x, y, w, h, rot=0, tag="a:xfrm"):
    r = f' rot="{int(rot*60000)}"' if rot else ""
    return f'<{tag}{r}><a:off x="{px(x)}" y="{px(y)}"/><a:ext cx="{px(w)}" cy="{px(h)}"/></{tag}>'


def clr(c, alpha=None):
    a = f'<a:alpha val="{int(alpha*100000)}"/>' if alpha is not None else ""
    return f'<a:schemeClr val="{c}">{a}</a:schemeClr>'


# ------------------------------------------------------------------ modelo de escena
# elementos: dict(kind=...). kinds: halo, staff, line, ellipse, rect, img, label, ph
def halo(cx, cy, r, key, a=0.30):
    return dict(kind="halo", cx=cx, cy=cy, r=r, c1=HALO[key][0], c2=HALO[key][1], a=a, name="Halo")


def staff(x=0, y=820, w=1920, gap=24, name="Pentagrama"):
    return dict(kind="staff", x=x, y=y, w=w, gap=gap, name=name)


def img(file, x, y, w, h, name, alt):
    return dict(kind="img", file=file, x=x, y=y, w=w, h=h, name=name, alt=alt)


def fit(file, bx, by, bw, bh, name, alt, align="bottom"):
    """Coloca la imagen del instrumento dentro de una caja (alineada abajo, centrada)."""
    iw, ih = Image.open(INST / file).size
    s = min(bw / iw, bh / ih)
    w, h = iw * s, ih * s
    return img(file, bx + (bw - w) / 2, by + bh - h if align == "bottom" else by, w, h, name, alt)


MONO = dict(font="mono", sz=14, caps=True, spc=1.7, color="tx2")


def ph(name, typ, idx, x, y, w, h, prompt, sz=24, font="sans", italic=False, color="tx1", algn="l", anchor="t",
       lnspc=1.0, caps=False, spc=0, aft=0, geom="rect", **kw):
    return dict(kind="ph", name=name, type=typ, idx=idx, x=x, y=y, w=w, h=h, prompt=prompt, sz=sz, font=font,
                italic=italic, color=color, algn=algn, anchor=anchor, lnspc=lnspc, caps=caps, spc=spc, aft=aft,
                geom=geom, **kw)


def label(name, idx, x, y, w, h, prompt, algn="l", anchor="t"):
    return ph(name, "body", idx, x, y, w, h, prompt, sz=14, font="mono", caps=True, spc=1.7, color="tx2", algn=algn, anchor=anchor)


def footer():
    return [
        ph("Pie / Footer", "ftr", 20, 120, 990, 900, 40, "Footer", sz=12, font="mono", caps=True, spc=1.2, color="tx2", anchor="ctr"),
        ph("Numero / Slide number", "sldNum", 21, 1500, 990, 300, 40, "‹#›", sz=12, font="mono", color="tx2", algn="r", anchor="ctr"),
    ]


def build_layouts():
    L = []
    # 1 Portada
    L.append(dict(name="Portada · Cover", type="title", els=[
        halo(440, 480, 540, "capture", .32), staff(),
        fit("contrabajo.png", 190, 180, 300, 640, "Contrabajo", "Line drawing of a double bass"),
        label("Etiqueta superior / Eyebrow", 10, 640, 200, 1160, 50, "EVENT · DATE"),
        ph("Titulo / Title", "ctrTitle", 0, 640, 260, 1160, 380, "Presentation title", sz=80, font="serif", italic=True, anchor="b", lnspc=.9),
        ph("Subtitulo / Subtitle", "body", 1, 640, 670, 1160, 100, "One-line subtitle or presenter", sz=24, color="tx2"),
    ] + footer()))
    # 2 Seccion
    L.append(dict(name="Sección · Section", type="secHead", els=[
        halo(1400, 500, 560, "intelligence", .30), staff(),
        fit("piano.png", 1020, 192, 760, 628, "Piano", "Line drawing of a piano"),
        label("Numero de seccion / Section number", 10, 120, 330, 800, 50, "01"),
        ph("Titulo / Title", "title", 0, 120, 380, 840, 270, "Section title", sz=72, font="serif", italic=True, anchor="b", lnspc=.9),
        ph("Texto / Text", "body", 1, 120, 680, 800, 130, "One sentence that introduces the section", sz=24, color="tx2"),
    ] + footer()))
    # 3 Frase grande
    L.append(dict(name="Frase grande · Big quote", type="cust", els=[
        halo(960, 450, 640, "delivery", .20), staff(),
        ph("Frase / Quote", "title", 0, 200, 170, 1520, 480, "A big statement, one or two lines", sz=88, font="serif", italic=True, algn="ctr", anchor="ctr", lnspc=.9),
        label("Autoria / Attribution", 10, 200, 690, 1520, 50, "WHO SAID IT · CONTEXT", algn="ctr"),
    ] + footer()))
    # 4 Persona
    L.append(dict(name="Persona · Person", type="cust", els=[
        halo(1560, 450, 470, "capture", .30), staff(),
        dict(kind="ellipse", x=1328, y=218, w=464, h=464, name="Anillo", lw=1.5, color="tx1", alpha=.9),
        label("Etiqueta superior / Eyebrow", 10, 120, 250, 1100, 50, "SPEAKER"),
        ph("Titulo / Name", "title", 0, 120, 310, 1100, 200, "Full name", sz=80, font="serif", italic=True, anchor="b", lnspc=.9),
        label("Rol / Role", 11, 120, 535, 1100, 50, "ROLE · TEAM"),
        ph("Texto / Short bio", "body", 1, 120, 610, 1000, 180, "Two or three lines about the person", sz=22, color="tx2"),
        ph("Imagen circular / Round picture", "pic", 13, 1340, 230, 440, 440, "Insert a round portrait", geom="ellipse", sz=14, color="tx2"),
    ] + footer()))
    # 5 Concepto en notacion
    sx0, sx1, sy = 960, 1800, 400
    notes = [(1090, sy + 120, "up"), (1330, sy + 40, "up"), (1570, sy + 160, "up")]
    nel = []
    for i, (nx, ny, d) in enumerate(notes):
        nel.append(dict(kind="note", x=nx, y=ny, name=f"Nota {i+1}"))
    L.append(dict(name="Concepto en notación · Concept in notation", type="cust", els=[
        halo(1380, 480, 520, "innovation", .16),
        staff(sx0, sy, sx1 - sx0, 40, "Pentagrama grande"),
        dict(kind="line", x1=sx0, y1=sy, x2=sx0, y2=sy + 160, lw=1.5, color="tx1", alpha=.9, name="Barra inicial"),
        dict(kind="line", x1=sx1, y1=sy, x2=sx1, y2=sy + 160, lw=1.5, color="tx1", alpha=.9, name="Barra final"),
    ] + nel + [
        ph("Titulo / Title", "title", 0, 120, 96, 1680, 170, "The concept in one line", sz=54, font="serif", italic=True, anchor="t", lnspc=.9),
        ph("Texto / Explanation", "body", 1, 120, 330, 700, 440, "Explain the concept in two or three short paragraphs", sz=22, color="tx2", aft=10),
        label("Etiqueta nota 1 / Note label 1", 11, 1000, 640, 180, 80, "FIRST IDEA", algn="ctr"),
        label("Etiqueta nota 2 / Note label 2", 12, 1240, 640, 180, 80, "SECOND IDEA", algn="ctr"),
        label("Etiqueta nota 3 / Note label 3", 13, 1480, 640, 180, 80, "THIRD IDEA", algn="ctr"),
    ] + footer()))
    # 6 Cuatro ejes
    cols = [(120, "capture", "contrabajo.png", "Contrabajo"), (560, "intelligence", "piano.png", "Piano"),
            (1000, "delivery", "bateria.png", "Bateria"), (1440, "innovation", "saxofon.png", "Saxofon")]
    els = [staff()]
    for cx, key, f, nm in cols:
        els.append(halo(cx + 180, 440, 270, key, .28))
    for cx, key, f, nm in cols:
        els.append(fit(f, cx, 250, 360, 330, nm, f"Line drawing of a {nm.lower()}"))
    els.append(ph("Titulo / Title", "title", 0, 120, 70, 1680, 130, "Four axes, one band", sz=48, font="serif", italic=True, anchor="t", lnspc=.9))
    for i, (cx, key, f, nm) in enumerate(cols):
        els.append(label(f"Eje {i+1} nombre / Axis {i+1} name", 11 + i, cx, 620, 360, 44, f"AXIS {i+1}"))
        els.append(ph(f"Eje {i+1} texto / Axis {i+1} text", "body", 21 + i, cx, 672, 360, 130, "One or two short lines", sz=16, color="tx2"))
    L.append(dict(name="Cuatro ejes · Four axes", type="cust", els=els + footer()))
    # 7 Dos columnas
    L.append(dict(name="Contenido de dos columnas · Two columns", type="cust", els=[
        halo(1700, 180, 520, "intelligence", .14), staff(),
        ph("Titulo / Title", "title", 0, 120, 96, 1680, 170, "Slide title", sz=54, font="serif", italic=True, anchor="t", lnspc=.9),
        ph("Columna izquierda / Left column", "body", 1, 120, 310, 780, 470, "Left column text", sz=22, aft=10),
        ph("Columna derecha / Right column", "body", 2, 1020, 310, 780, 470, "Right column text", sz=22, aft=10),
    ] + footer()))
    # 8 Cierre
    L.append(dict(name="Cierre · Closing", type="cust", els=[
        halo(960, 420, 640, "delivery", .20), staff(),
        ph("Frase / Closing line", "title", 0, 120, 180, 1100, 400, "A closing line", sz=72, font="serif", italic=True, anchor="b", lnspc=.9),
        ph("Contacto / Contact", "body", 1, 120, 620, 1000, 140, "Name · email · next step", sz=22, color="tx2"),
        dict(kind="rect", x=1400, y=330, w=400, h=200, name="Marco de logo", dash=True, lw=1, color="tx2", alpha=.7),
        dict(kind="text", x=1400, y=410, w=400, h=44, text="LOGO", name="Marcador Logo", **MONO, algn="ctr"),
        ph("Logo", "pic", 14, 1400, 330, 400, 200, "Insert logo", sz=14, color="tx2"),
    ] + footer()))
    return L


# ------------------------------------------------------------------ OOXML
class Ids:
    def __init__(self): self.n = 1
    def __call__(self): self.n += 1; return self.n


FONTREF = {"serif": "+mj-lt", "sans": "+mn-lt", "mono": None}


def rpr_attrs(e):
    a = f'lang="en-US" sz="{int(e["sz"]*100)}"'
    if e["italic"]: a += ' i="1"'
    if e["caps"]: a += ' cap="all"'
    if e["spc"]: a += f' spc="{int(e["spc"]*100)}"'
    return a


def defrpr(e):
    inner = f'<a:solidFill>{clr(e["color"])}</a:solidFill>'
    if e["font"] == "mono":
        inner += '<a:latin typeface="Geist Mono"/><a:cs typeface="Geist Mono"/>'
    else:
        inner += f'<a:latin typeface="{FONTREF[e["font"]]}"/>'
    a = rpr_attrs(e).replace('lang="en-US" ', "")
    return f'<a:defRPr {a}>{inner}</a:defRPr>'


def lststyle(e):
    ls = f'<a:lnSpc><a:spcPct val="{int(e["lnspc"]*100000)}"/></a:lnSpc>'
    ls += f'<a:spcBef><a:spcPts val="0"/></a:spcBef><a:spcAft><a:spcPts val="{int(e["aft"]*200)}"/></a:spcAft>'
    algn = e["algn"]
    return (f'<a:lstStyle><a:lvl1pPr marL="0" indent="0" algn="{algn}">{ls}<a:buNone/>{defrpr(e)}</a:lvl1pPr></a:lstStyle>')


def ph_tag(e):
    t = e["type"]
    idx = f' idx="{e["idx"]}"' if (e["idx"] or t not in ("title", "ctrTitle")) else ""
    typ = "" if t == "body" and False else f' type="{t}"'
    sz = ' sz="quarter"' if t in ("ftr", "sldNum") else ""
    return f'<p:ph{typ}{idx}{sz}/>'


def layout_ph(e, ids):
    i = ids()
    geom = "ellipse" if e["geom"] == "ellipse" else "rect"
    extra = ""
    if e["type"] == "pic":
        extra = (f'<a:prstGeom prst="{geom}"><a:avLst/></a:prstGeom>'
                 + ('<a:ln w="19050"><a:noFill/></a:ln>' if geom == "ellipse" else
                    '<a:noFill/>'))
        sp = f'<p:spPr>{xfrm(e["x"],e["y"],e["w"],e["h"])}{extra}</p:spPr>'
    else:
        sp = f'<p:spPr>{xfrm(e["x"],e["y"],e["w"],e["h"])}</p:spPr>'
    anchor = e["anchor"]
    body = (f'<a:bodyPr lIns="0" tIns="0" rIns="0" bIns="0" anchor="{anchor}"><a:normAutofit/></a:bodyPr>')
    pr = f'<a:p><a:r><a:rPr lang="en-US"/><a:t>{escape(e["prompt"])}</a:t></a:r></a:p>'
    if e["type"] == "sldNum":
        pr = '<a:p><a:fld id="{B6F15528-21DE-4FAA-801E-634DDDAF4B2B}" type="slidenum"><a:rPr lang="en-US"/><a:t>‹#›</a:t></a:fld></a:p>'
    return (f'<p:sp><p:nvSpPr><p:cNvPr id="{i}" name="{escape(e["name"])}"/><p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr>'
            f'<p:nvPr>{ph_tag(e)}</p:nvPr></p:nvSpPr>{sp}<p:txBody>{body}{lststyle(e)}{pr}</p:txBody></p:sp>')


def stroke(lw, color, alpha=None, dash=False):
    d = '<a:prstDash val="dash"/>' if dash else ""
    return f'<a:ln w="{int(lw*12700)}" cap="rnd"><a:solidFill>{clr(color, alpha)}</a:solidFill>{d}</a:ln>'


def shape_xml(e, ids, rels):
    k = e["kind"]
    i = ids()
    nm = escape(e.get("name", k))
    if k == "halo":
        r = e["r"]
        g = (f'<a:gradFill rotWithShape="1"><a:gsLst>'
             f'<a:gs pos="0">{clr(e["c1"], e["a"])}</a:gs><a:gs pos="55000">{clr(e["c2"], e["a"]*.43)}</a:gs>'
             f'<a:gs pos="100000">{clr(e["c2"], 0)}</a:gs></a:gsLst><a:path path="circle"><a:fillToRect l="50000" t="50000" r="50000" b="50000"/></a:path></a:gradFill>')
        return (f'<p:sp><p:nvSpPr><p:cNvPr id="{i}" name="{nm}" descr="Soft decorative glow"/><p:cNvSpPr/><p:nvPr userDrawn="1"/></p:nvSpPr>'
                f'<p:spPr>{xfrm(e["cx"]-r, e["cy"]-r, 2*r, 2*r)}<a:prstGeom prst="ellipse"><a:avLst/></a:prstGeom>{g}<a:ln><a:noFill/></a:ln></p:spPr>'
                f'<p:txBody><a:bodyPr/><a:lstStyle/><a:p><a:endParaRPr lang="en-US"/></a:p></p:txBody></p:sp>')
    if k == "staff":
        lines = ""
        for n in range(5):
            y = e["y"] + n * e["gap"]
            j = ids()
            lines += (f'<p:cxnSp><p:nvCxnSpPr><p:cNvPr id="{j}" name="Linea {n+1}"/><p:cNvCxnSpPr/><p:nvPr userDrawn="1"/></p:nvCxnSpPr>'
                      f'<p:spPr>{xfrm(e["x"], y, e["w"], 0)}<a:prstGeom prst="line"><a:avLst/></a:prstGeom>{stroke(1, "tx1", .35)}</p:spPr></p:cxnSp>')
        gh = 4 * e["gap"]
        gx = xfrm(e["x"], e["y"], e["w"], gh, tag="a:xfrm").replace("</a:xfrm>", "")
        off = f'<a:off x="{px(e["x"])}" y="{px(e["y"])}"/><a:ext cx="{px(e["w"])}" cy="{px(gh)}"/>'
        return (f'<p:grpSp><p:nvGrpSpPr><p:cNvPr id="{i}" name="{nm}" descr="Five thin staff lines"/><p:cNvGrpSpPr/><p:nvPr userDrawn="1"/></p:nvGrpSpPr>'
                f'<p:grpSpPr><a:xfrm>{off}<a:chOff x="{px(e["x"])}" y="{px(e["y"])}"/><a:chExt cx="{px(e["w"])}" cy="{px(gh)}"/></a:xfrm></p:grpSpPr>{lines}</p:grpSp>')
    if k == "line":
        x, y = min(e["x1"], e["x2"]), min(e["y1"], e["y2"])
        return (f'<p:cxnSp><p:nvCxnSpPr><p:cNvPr id="{i}" name="{nm}"/><p:cNvCxnSpPr/><p:nvPr userDrawn="1"/></p:nvCxnSpPr>'
                f'<p:spPr>{xfrm(x, y, abs(e["x2"]-e["x1"]), abs(e["y2"]-e["y1"]))}<a:prstGeom prst="line"><a:avLst/></a:prstGeom>{stroke(e["lw"], e["color"], e.get("alpha"))}</p:spPr></p:cxnSp>')
    if k in ("ellipse", "rect"):
        geom = "ellipse" if k == "ellipse" else "rect"
        return (f'<p:sp><p:nvSpPr><p:cNvPr id="{i}" name="{nm}"/><p:cNvSpPr/><p:nvPr userDrawn="1"/></p:nvSpPr>'
                f'<p:spPr>{xfrm(e["x"], e["y"], e["w"], e["h"])}<a:prstGeom prst="{geom}"><a:avLst/></a:prstGeom><a:noFill/>'
                f'{stroke(e["lw"], e["color"], e.get("alpha"), e.get("dash", False))}</p:spPr>'
                f'<p:txBody><a:bodyPr/><a:lstStyle/><a:p><a:endParaRPr lang="en-US"/></a:p></p:txBody></p:sp>')
    if k == "note":  # cabeza llena inclinada + plica
        x, y = e["x"], e["y"]
        head = (f'<p:sp><p:nvSpPr><p:cNvPr id="{i}" name="{nm} cabeza"/><p:cNvSpPr/><p:nvPr userDrawn="1"/></p:nvSpPr>'
                f'<p:spPr>{xfrm(x-24, y-17, 48, 34, rot=-20)}<a:prstGeom prst="ellipse"><a:avLst/></a:prstGeom><a:solidFill>{clr("tx1")}</a:solidFill><a:ln><a:noFill/></a:ln></p:spPr>'
                f'<p:txBody><a:bodyPr/><a:lstStyle/><a:p><a:endParaRPr lang="en-US"/></a:p></p:txBody></p:sp>')
        j = ids()
        stem = (f'<p:cxnSp><p:nvCxnSpPr><p:cNvPr id="{j}" name="{nm} plica"/><p:cNvCxnSpPr/><p:nvPr userDrawn="1"/></p:nvCxnSpPr>'
                f'<p:spPr>{xfrm(x+21, y-120, 0, 116)}<a:prstGeom prst="line"><a:avLst/></a:prstGeom>{stroke(1.5, "tx1")}</p:spPr></p:cxnSp>')
        return head + stem
    if k == "img":
        rid = rels.add_media(e["file"])
        return (f'<p:pic><p:nvPicPr><p:cNvPr id="{i}" name="{nm}" descr="{escape(e["alt"])}"/><p:cNvPicPr><a:picLocks noChangeAspect="1"/></p:cNvPicPr><p:nvPr userDrawn="1"/></p:nvPicPr>'
                f'<p:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></p:blipFill>'
                f'<p:spPr>{xfrm(e["x"], e["y"], e["w"], e["h"])}<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr></p:pic>')
    if k == "text":
        e2 = dict(e, italic=False, lnspc=1, aft=0)
        return (f'<p:sp><p:nvSpPr><p:cNvPr id="{i}" name="{nm}"/><p:cNvSpPr txBox="1"/><p:nvPr userDrawn="1"/></p:nvSpPr>'
                f'<p:spPr>{xfrm(e["x"], e["y"], e["w"], e["h"])}<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/></p:spPr>'
                f'<p:txBody><a:bodyPr lIns="0" tIns="0" rIns="0" bIns="0" anchor="ctr"/>{lststyle(e2)}<a:p><a:pPr algn="{e["algn"]}"/><a:r><a:rPr {rpr_attrs(e2)}>'
                f'<a:solidFill>{clr(e["color"])}</a:solidFill><a:latin typeface="Geist Mono"/></a:rPr><a:t>{escape(e["text"])}</a:t></a:r></a:p></p:txBody></p:sp>')
    raise ValueError(k)


class Rels:
    def __init__(self, base): self.items = []; self.base = base; self.media = {}
    def add(self, typ, target):
        rid = f"rId{len(self.items)+1}"; self.items.append((rid, typ, target)); return rid
    def add_media(self, f):
        if f in self.media: return self.media[f]
        rid = self.add("image", f"../media/{f}"); self.media[f] = rid; return rid
    def xml(self):
        base = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/"
        body = "".join(f'<Relationship Id="{r}" Type="{base}{t}" Target="{tg}"/>' for r, t, tg in self.items)
        return HDR + f'<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">{body}</Relationships>'


def sptree(inner):
    return ('<p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>'
            '<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>'
            + inner + '</p:spTree>')


def layout_xml(lay, rels):
    ids = Ids()
    inner = "".join(layout_ph(e, ids) if e["kind"] == "ph" else shape_xml(e, ids, rels) for e in lay["els"])
    return (HDR + f'<p:sldLayout {NS} type="{lay["type"]}" preserve="1"><p:cSld name="{escape(lay["name"])}">{sptree(inner)}</p:cSld>'
            '<p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sldLayout>')


def master_xml(n_layouts):
    ids = Ids()
    title = dict(sz=54, font="serif", italic=True, color="tx1", algn="l", anchor="t", lnspc=.9, caps=False, spc=0, aft=0)
    base = dict(italic=False, caps=False, spc=0)
    tx = (f'<p:sp><p:nvSpPr><p:cNvPr id="{ids()}" name="Titulo / Title"/><p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr><p:nvPr><p:ph type="title"/></p:nvPr></p:nvSpPr>'
          f'<p:spPr>{xfrm(120, 96, 1680, 170)}</p:spPr><p:txBody><a:bodyPr lIns="0" tIns="0" rIns="0" bIns="0" anchor="t"><a:normAutofit/></a:bodyPr><a:lstStyle/>'
          '<a:p><a:r><a:rPr lang="en-US"/><a:t>Click to edit the title</a:t></a:r></a:p></p:txBody></p:sp>')
    tx += (f'<p:sp><p:nvSpPr><p:cNvPr id="{ids()}" name="Texto / Body"/><p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr><p:nvPr><p:ph type="body" idx="1"/></p:nvPr></p:nvSpPr>'
           f'<p:spPr>{xfrm(120, 310, 1680, 470)}</p:spPr><p:txBody><a:bodyPr lIns="0" tIns="0" rIns="0" bIns="0"><a:normAutofit/></a:bodyPr><a:lstStyle/>'
           '<a:p><a:pPr lvl="0"/><a:r><a:rPr lang="en-US"/><a:t>Click to edit the text</a:t></a:r></a:p>'
           '<a:p><a:pPr lvl="1"/><a:r><a:rPr lang="en-US"/><a:t>Second level</a:t></a:r></a:p></p:txBody></p:sp>')
    for e in footer():
        e = dict(e)
        tx += layout_ph(e, ids)
    def lvl(n, sz, bu, marL):
        b = '<a:buNone/>' if not bu else f'<a:buFont typeface="Geist Mono"/><a:buChar char="–"/>'
        return (f'<a:lvl{n}pPr marL="{marL}" indent="{-marL if bu else 0}" algn="l"><a:lnSpc><a:spcPct val="105000"/></a:lnSpc><a:spcBef><a:spcPts val="0"/></a:spcBef>'
                f'<a:spcAft><a:spcPts val="800"/></a:spcAft>{b}<a:defRPr sz="{sz}" kern="1200"><a:solidFill>{clr("tx1")}</a:solidFill><a:latin typeface="+mn-lt"/></a:defRPr></a:lvl{n}pPr>')
    body = lvl(1, 2400, False, 0) + lvl(2, 2000, True, 285750) + lvl(3, 1800, True, 571500) + lvl(4, 1600, True, 857250) + lvl(5, 1600, True, 1143000)
    other = "".join(f'<a:lvl{n}pPr marL="{(n-1)*457200}" algn="l"><a:defRPr sz="1800"><a:solidFill>{clr("tx1")}</a:solidFill><a:latin typeface="+mn-lt"/></a:defRPr></a:lvl{n}pPr>' for n in range(1, 10))
    tstyle = (f'<p:titleStyle><a:lvl1pPr algn="l"><a:lnSpc><a:spcPct val="90000"/></a:lnSpc><a:spcBef><a:spcPts val="0"/></a:spcBef><a:buNone/>'
              f'<a:defRPr sz="5400" i="1" kern="1200"><a:solidFill>{clr("tx1")}</a:solidFill><a:latin typeface="+mj-lt"/></a:defRPr></a:lvl1pPr></p:titleStyle>')
    lids = "".join(f'<p:sldLayoutId id="{2147483649+i}" r:id="rId{i+1}"/>' for i in range(n_layouts))
    return (HDR + f'<p:sldMaster {NS}><p:cSld><p:bg><p:bgPr><a:solidFill>{clr("bg1")}</a:solidFill><a:effectLst/></p:bgPr></p:bg>{sptree(tx)}</p:cSld>'
            '<p:clrMap bg1="dk1" tx1="lt1" bg2="dk2" tx2="lt2" accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/>'
            f'<p:sldLayoutIdLst>{lids}</p:sldLayoutIdLst><p:txStyles>{tstyle}<p:bodyStyle>{body}</p:bodyStyle><p:otherStyle><a:defPPr><a:defRPr lang="en-US"/></a:defPPr>{other}</p:otherStyle></p:txStyles></p:sldMaster>')


def theme_xml():
    c = "".join(f'<a:{k}><a:srgbClr val="{v}"/></a:{k}>' for k, v in COLORS.items())
    fills = ('<a:fillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:fillStyleLst>'
             '<a:lnStyleLst><a:ln w="12700" cap="rnd"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln><a:ln w="19050" cap="rnd"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln><a:ln w="25400" cap="rnd"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln></a:lnStyleLst>'
             '<a:effectStyleLst><a:effectStyle><a:effectLst/></a:effectStyle><a:effectStyle><a:effectLst/></a:effectStyle><a:effectStyle><a:effectLst/></a:effectStyle></a:effectStyleLst>'
             '<a:bgFillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:bgFillStyleLst>')
    return (HDR + '<a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="DT Jazz"><a:themeElements>'
            f'<a:clrScheme name="DT Jazz">{c}</a:clrScheme>'
            '<a:fontScheme name="DT Jazz"><a:majorFont><a:latin typeface="Instrument Serif"/><a:ea typeface=""/><a:cs typeface=""/></a:majorFont>'
            '<a:minorFont><a:latin typeface="Inter Tight"/><a:ea typeface=""/><a:cs typeface=""/></a:minorFont></a:fontScheme>'
            f'<a:fmtScheme name="DT Jazz">{fills}</a:fmtScheme></a:themeElements><a:objectDefaults/><a:extraClrSchemeLst/></a:theme>')


# ------------------------------------------------------------------ laminas de ejemplo
SLIDES = [
    {10: "DESIGN TECHNOLOGY · 2026", 0: "The Jazz Session", 1: "A warm, line-drawn way to tell our story"},
    {10: "01", 0: "Listen first", 1: "Every good piece starts by hearing what the room needs."},
    {0: "Design is a song. Technology is the band.", 10: "OUR WAY OF WORKING"},
    {10: "SPEAKER", 0: "Alex Morgan", 11: "LEAD DESIGNER · STUDIO TEAM",
     1: "Turns rough sketches into tools people reach for every day. Plays the long game and loves a good rehearsal.",
     13: "__avatar__"},
    {0: "Concepts as notation", 1: ["Each idea is a note on the staff: small, clear, and part of a melody.",
                                  "Read left to right, the story builds a phrase the whole room can hum."],
     11: "Sketch", 12: "Build", 13: "Share"},
    {0: "Four axes, one band", 11: "Capture", 12: "Intelligence", 13: "Delivery", 14: "Innovation",
     21: "Gather what is real, from the first sketch.", 22: "Make sense of it with shared models.",
     23: "Ship tools that keep the beat.", 24: "Improvise on what comes next."},
    {0: "What we keep, what we change", 1: ["Keep", "Thin lines and plenty of silence.", "One idea per slide."],
     2: ["Change", "Fewer words, more rhythm.", "A clear next step at the end."]},
    {0: "Let’s make some music together", 1: ["Alex Morgan · alex@example.com", "Next step: book a jam session"]},
]


def write_avatar(path):
    im = Image.new("RGB", (800, 800), "#1A1A1F")
    d = ImageDraw.Draw(im)
    ink = "#B9B4AA"
    d.ellipse((290, 180, 510, 400), outline=ink, width=4)
    d.arc((170, 470, 630, 1000), 180, 360, fill=ink, width=4)
    im.save(path)


def text_paras(val):
    return val if isinstance(val, list) else [val]


def slide_xml(lay, content, rels):
    ids = Ids()
    inner = ""
    for e in lay["els"]:
        if e["kind"] != "ph" or e["type"] in ("ftr", "sldNum"): continue
        v = content.get(e["idx"])
        if v is None: continue
        i = ids()
        if e["type"] == "pic":
            rid = rels.add_media("avatar.png")
            inner += (f'<p:pic><p:nvPicPr><p:cNvPr id="{i}" name="{escape(e["name"])}" descr="Generic portrait placeholder"/><p:cNvPicPr><a:picLocks noGrp="1" noChangeAspect="1"/></p:cNvPicPr><p:nvPr>{ph_tag(e)}</p:nvPr></p:nvPicPr>'
                      f'<p:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></p:blipFill>'
                      f'<p:spPr>{xfrm(e["x"], e["y"], e["w"], e["h"])}<a:prstGeom prst="ellipse"><a:avLst/></a:prstGeom></p:spPr></p:pic>')
            continue
        paras = "".join(f'<a:p><a:r><a:rPr lang="en-US" dirty="0"/><a:t>{escape(t)}</a:t></a:r></a:p>' for t in text_paras(v))
        inner += (f'<p:sp><p:nvSpPr><p:cNvPr id="{i}" name="{escape(e["name"])}"/><p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr><p:nvPr>{ph_tag(e)}</p:nvPr></p:nvSpPr>'
                  f'<p:spPr/><p:txBody><a:bodyPr/><a:lstStyle/>{paras}</p:txBody></p:sp>')
    return HDR + f'<p:sld {NS}><p:cSld>{sptree(inner)}</p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sld>'


# ------------------------------------------------------------------ empaquetado
def build(with_slides, path):
    layouts = build_layouts()
    n = len(layouts)
    parts, ct = {}, []
    REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/"
    media = {}

    # layouts
    for i, lay in enumerate(layouts, 1):
        r = Rels(""); r.add("slideMaster", "../slideMasters/slideMaster1.xml")
        parts[f"ppt/slideLayouts/slideLayout{i}.xml"] = layout_xml(lay, r)
        parts[f"ppt/slideLayouts/_rels/slideLayout{i}.xml.rels"] = r.xml()
        for f in r.media: media[f] = (INST / f)
        ct.append((f"/ppt/slideLayouts/slideLayout{i}.xml", "application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"))
    # master
    mr = Rels("")
    for i in range(1, n + 1): mr.add("slideLayout", f"../slideLayouts/slideLayout{i}.xml")
    mr.add("theme", "../theme/theme1.xml")
    parts["ppt/slideMasters/slideMaster1.xml"] = master_xml(n)
    parts["ppt/slideMasters/_rels/slideMaster1.xml.rels"] = mr.xml()
    parts["ppt/theme/theme1.xml"] = theme_xml()
    ct += [("/ppt/slideMasters/slideMaster1.xml", "application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"),
           ("/ppt/theme/theme1.xml", "application/vnd.openxmlformats-officedocument.theme+xml")]
    # slides
    pr = Rels("")
    pr.add("slideMaster", "slideMasters/slideMaster1.xml")
    sld_ids = ""
    if with_slides:
        for i, (lay, content) in enumerate(zip(layouts, SLIDES), 1):
            r = Rels(""); r.add("slideLayout", f"../slideLayouts/slideLayout{i}.xml")
            parts[f"ppt/slides/slide{i}.xml"] = slide_xml(lay, content, r)
            parts[f"ppt/slides/_rels/slide{i}.xml.rels"] = r.xml()
            for f in r.media: media[f] = (OUT / "assets" / "avatar.png") if f == "avatar.png" else (INST / f)
            rid = pr.add("slide", f"slides/slide{i}.xml")
            sld_ids += f'<p:sldId id="{255+i}" r:id="{rid}"/>'
            ct.append((f"/ppt/slides/slide{i}.xml", "application/vnd.openxmlformats-officedocument.presentationml.slide+xml"))
    for t in ("presProps", "viewProps", "tableStyles"): pr.add(t, f"{t}.xml")
    pr.add("theme", "theme/theme1.xml")
    sldlst = f"<p:sldIdLst>{sld_ids}</p:sldIdLst>" if with_slides else ""
    parts["ppt/presentation.xml"] = (HDR + f'<p:presentation {NS} saveSubsetFonts="1"><p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId1"/></p:sldMasterIdLst>{sldlst}'
                                     '<p:sldSz cx="12192000" cy="6858000"/><p:notesSz cx="6858000" cy="9144000"/>'
                                     '<p:defaultTextStyle><a:lvl1pPr marL="0" algn="l"><a:defRPr sz="2400"><a:solidFill><a:schemeClr val="tx1"/></a:solidFill><a:latin typeface="+mn-lt"/></a:defRPr></a:lvl1pPr></p:defaultTextStyle></p:presentation>')
    parts["ppt/_rels/presentation.xml.rels"] = pr.xml()
    parts["ppt/presProps.xml"] = HDR + f'<p:presentationPr {NS}/>'
    parts["ppt/viewProps.xml"] = HDR + f'<p:viewPr {NS}><p:normalViewPr><p:restoredLeft sz="15620"/><p:restoredTop sz="94660"/></p:normalViewPr></p:viewPr>'
    parts["ppt/tableStyles.xml"] = HDR + '<a:tblStyleLst xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" def="{5C22544A-7EE6-4342-B048-85BDC9FD1C3A}"/>'
    main = "template" if not with_slides else "presentation"
    ct += [("/ppt/presentation.xml", f"application/vnd.openxmlformats-officedocument.presentationml.{main}.main+xml"),
           ("/ppt/presProps.xml", "application/vnd.openxmlformats-officedocument.presentationml.presProps+xml"),
           ("/ppt/viewProps.xml", "application/vnd.openxmlformats-officedocument.presentationml.viewProps+xml"),
           ("/ppt/tableStyles.xml", "application/vnd.openxmlformats-officedocument.presentationml.tableStyles+xml"),
           ("/docProps/core.xml", "application/vnd.openxmlformats-package.core-properties+xml"),
           ("/docProps/app.xml", "application/vnd.openxmlformats-officedocument.extended-properties+xml")]
    title = "DT Jazz template" if not with_slides else "DT Jazz example deck"
    parts["docProps/core.xml"] = (HDR + '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" '
                                  'xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
                                  f'<dc:title>{title}</dc:title><dc:creator>Design Technology</dc:creator></cp:coreProperties>')
    parts["docProps/app.xml"] = HDR + '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"><Application>Microsoft Office PowerPoint</Application></Properties>'
    parts["_rels/.rels"] = (HDR + '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                            f'<Relationship Id="rId1" Type="{REL}officeDocument" Target="ppt/presentation.xml"/>'
                            '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>'
                            f'<Relationship Id="rId3" Type="{REL}extended-properties" Target="docProps/app.xml"/></Relationships>')
    ctx = (HDR + '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
           '<Default Extension="xml" ContentType="application/xml"/><Default Extension="png" ContentType="image/png"/>'
           + "".join(f'<Override PartName="{p}" ContentType="{c}"/>' for p, c in ct) + '</Types>')
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", ctx)
        for k, v in parts.items(): z.writestr(k, v)
        for f, src in media.items(): z.write(src, f"ppt/media/{f}")
    print("escrito", path)


if __name__ == "__main__":
    write_avatar(OUT / "assets" / "avatar.png")
    build(False, OUT / "DT-Jazz.potx")
    build(True, OUT / "DT-Jazz-ejemplo.pptx")
