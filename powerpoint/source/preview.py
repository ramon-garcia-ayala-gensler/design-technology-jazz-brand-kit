"""Render aproximado (Pillow) de las 8 laminas del ejemplo a partir del mismo modelo de escena. Se usa cuando no hay
LibreOffice/PowerPoint; no sustituye una revision en PowerPoint real. Uso: python preview.py <carpeta powerpoint> <carpeta fuentes ttf> <salida png dir>"""
import sys, pathlib, io
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont
sys.argv = [sys.argv[0]] + sys.argv[1:]
OUT = pathlib.Path(sys.argv[1]); FD = pathlib.Path(sys.argv[2]); PD = pathlib.Path(sys.argv[3])
FD.mkdir(parents=True, exist_ok=True); PD.mkdir(parents=True, exist_ok=True)
import build_template as B  # noqa
B.OUT = OUT; B.INST = OUT / "assets" / "instrumentos"
SRC = pathlib.Path("C:/dev/DT-Summit-video/public/fonts")
FILES = {"serif": "instrument-serif-latin-400-italic", "sans": "inter-tight-latin-wght-normal", "mono": "geist-mono-latin-500-normal"}
for k, f in FILES.items():
    t = FD / f"{k}.ttf"
    if not t.exists():
        tf = TTFont(SRC / f"{f}.woff2"); tf.flavor = None; tf.save(t)
COL = {"tx1": "#F2EFE8", "tx2": "#B9B4AA", "accent1": "#7FB8E6", "accent2": "#A99BE0", "accent3": "#E59BC0",
       "accent4": "#F2B48C", "accent5": "#EE7F6E", "bg1": "#0B0B0D"}
rgb = lambda c: tuple(int(COL[c][i:i+2], 16) for i in (1, 3, 5))
warn = []


def font(kind, px):
    f = ImageFont.truetype(str(FD / f"{kind}.ttf"), int(px))
    if kind == "sans":
        try: f.set_variation_by_axes([400])
        except Exception: pass
    return f


def halo(base, e):
    r = int(e["r"]); S = 2 * r
    yy, xx = np.mgrid[0:S, 0:S]
    d = np.hypot(xx - r, yy - r) / r
    c1, c2 = np.array(rgb(e["c1"]), float), np.array(rgb(e["c2"]), float)
    a1, a2 = e["a"], e["a"] * .43
    t = np.clip(d / .55, 0, 1)[..., None]
    col = c1 * (1 - t) + c2 * t
    al = np.where(d <= .55, a1 + (a2 - a1) * np.clip(d / .55, 0, 1), a2 * np.clip((1 - d) / .45, 0, 1))
    al = np.where(d > 1, 0, al)
    x0, y0 = int(e["cx"] - r), int(e["cy"] - r)
    reg = np.array(base.crop((x0, y0, x0 + S, y0 + S)).convert("RGB"), float) if x0 >= 0 and y0 >= 0 and x0 + S <= 1920 and y0 + S <= 1080 else None
    big = np.zeros((1080, 1920, 3), float); big[:] = np.array(base.convert("RGB"), float)
    ax0, ay0 = max(x0, 0), max(y0, 0); ax1, ay1 = min(x0 + S, 1920), min(y0 + S, 1080)
    sub = big[ay0:ay1, ax0:ax1]
    cs = col[ay0 - y0:ay1 - y0, ax0:ax1 - x0 + 0 if False else ax1 - x0][:, ax0 - x0:]
    cs = col[ay0 - y0:ay1 - y0, ax0 - x0:ax1 - x0]; als = al[ay0 - y0:ay1 - y0, ax0 - x0:ax1 - x0][..., None]
    big[ay0:ay1, ax0:ax1] = sub * (1 - als) + cs * als
    return Image.fromarray(big.astype("uint8"))


def line(img, x1, y1, x2, y2, w, color, alpha=1.0, dash=False):
    ov = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    c = rgb(color) + (int(255 * (alpha or 1)),)
    if dash:
        x = x1
        while x < x2:
            d.line((x, y1, min(x + 14, x2), y1), fill=c, width=w); d.line((x, y2, min(x + 14, x2), y2), fill=c, width=w); x += 26
    else: d.line((x1, y1, x2, y2), fill=c, width=w)
    return Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB")


def draw_text(img, e, paras):
    sz = e["sz"] * 2; f = font(e["font"], sz)
    caps, spc = e["caps"], e["spc"] * 2
    def meas(s): return sum(f.getlength(ch) + spc for ch in s) if spc else f.getlength(s)
    lines = []
    for p in paras:
        p = p.upper() if caps else p
        for seg in p.split("\n"):
            cur = ""
            for wd in seg.split(" "):
                t = (cur + " " + wd).strip()
                if meas(t) <= e["w"] or not cur: cur = t
                else: lines.append(cur); cur = wd
            lines.append(cur)
        lines.append(None) if False else None
    lh = sz * 1.2 * e["lnspc"]
    gap = e["aft"] * 2
    nl = len(lines); total = nl * lh + gap * (len(paras) - 1)
    for ln in lines:
        if meas(ln) > e["w"] + 1: warn.append(f'ancho excedido "{ln[:30]}" en {e["name"]}')
    if total > e["h"] + 2: warn.append(f'ALTO excedido {total:.0f}>{e["h"]} en {e["name"]}')
    y = e["y"] + {"t": 0, "ctr": (e["h"] - total) / 2, "b": e["h"] - total}[e["anchor"]]
    d = ImageDraw.Draw(img); c = rgb(e["color"])
    # parrafos: recalcular salto de linea por parrafo para aplicar gap
    li = 0
    for p in paras:
        p2 = p.upper() if caps else p
        n = 0
        for seg in p2.split("\n"):
            cur = ""; sl = []
            for wd in seg.split(" "):
                t = (cur + " " + wd).strip()
                if meas(t) <= e["w"] or not cur: cur = t
                else: sl.append(cur); cur = wd
            sl.append(cur)
            for ln in sl:
                w = meas(ln); x = e["x"] + {"l": 0, "ctr": (e["w"] - w) / 2, "r": e["w"] - w}[e["algn"]]
                if spc:
                    for ch in ln: d.text((x, y), ch, font=f, fill=c); x += f.getlength(ch) + spc
                else: d.text((x, y), ln, font=f, fill=c)
                y += lh
        y += gap
    return img


def render(lay, content, avatar):
    img = Image.new("RGB", (1920, 1080), rgb("bg1"))
    for e in lay["els"]:
        k = e["kind"]
        if k == "halo": img = halo(img, e)
        elif k == "staff":
            for n in range(5): img = line(img, e["x"], e["y"] + n * e["gap"], e["x"] + e["w"], e["y"] + n * e["gap"], 2, "tx1", .35)
        elif k == "line": img = line(img, e["x1"], e["y1"], e["x2"], e["y2"], 3, e["color"], e.get("alpha"))
        elif k in ("ellipse", "rect"):
            ov = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
            c = rgb(e["color"]) + (int(255 * (e.get("alpha") or 1)),)
            if k == "ellipse": d.ellipse((e["x"], e["y"], e["x"] + e["w"], e["y"] + e["h"]), outline=c, width=int(e["lw"] * 2))
            else:
                for x in range(int(e["x"]), int(e["x"] + e["w"]), 26):
                    xe = min(x + 14, e["x"] + e["w"])
                    d.line((x, e["y"], xe, e["y"]), fill=c, width=2); d.line((x, e["y"] + e["h"], xe, e["y"] + e["h"]), fill=c, width=2)
                for y in range(int(e["y"]), int(e["y"] + e["h"]), 26):
                    ye = min(y + 14, e["y"] + e["h"])
                    d.line((e["x"], y, e["x"], ye), fill=c, width=2); d.line((e["x"] + e["w"], y, e["x"] + e["w"], ye), fill=c, width=2)
            img = Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB")
        elif k == "note":
            t = Image.new("RGBA", (200, 200), (0, 0, 0, 0)); d = ImageDraw.Draw(t); d.ellipse((52, 66, 148, 134), fill=rgb("tx1") + (255,))
            t = t.rotate(20, resample=Image.BICUBIC); img.paste(t, (int(e["x"] - 100), int(e["y"] - 100)), t)
            img = line(img, e["x"] + 21, e["y"] - 120, e["x"] + 21, e["y"] - 4, 3, "tx1")
        elif k == "img":
            im = Image.open(B.INST / e["file"]).convert("RGBA").resize((int(e["w"]), int(e["h"])), Image.LANCZOS)
            img.paste(im, (int(e["x"]), int(e["y"])), im)
        elif k == "text":
            e2 = dict(e, italic=False, lnspc=1, aft=0, anchor="ctr", sz=e["sz"]); img = draw_text(img, e2, [e["text"]])
        elif k == "ph" and e["type"] not in ("ftr", "sldNum"):
            v = content.get(e["idx"])
            if v is None: continue
            if e["type"] == "pic":
                im = Image.open(avatar).convert("RGB").resize((int(e["w"]), int(e["h"])))
                m = Image.new("L", im.size, 0); ImageDraw.Draw(m).ellipse((0, 0, im.size[0] - 1, im.size[1] - 1), fill=255)
                img.paste(im, (int(e["x"]), int(e["y"])), m)
            else: img = draw_text(img, e, B.text_paras(v))
    return img


lays = B.build_layouts(); tiles = []
for i, (lay, c) in enumerate(zip(lays, B.SLIDES), 1):
    im = render(lay, c, OUT / "assets" / "avatar.png"); im.save(PD / f"slide-{i}.png"); tiles.append(im)
tw, th = 960, 540
m = Image.new("RGB", (tw * 2 + 30, th * 4 + 50), "#1A1A1F")
for i, im in enumerate(tiles):
    m.paste(im.resize((tw, th), Image.LANCZOS), (10 + (i % 2) * (tw + 10), 10 + (i // 2) * (th + 10)))
m.save(PD / "mosaico.png")
m.resize((m.width * 3 // 4, m.height * 3 // 4), Image.LANCZOS).save(OUT / "preview.png", optimize=True)
print("\n".join(warn) or "sin avisos de desborde")
