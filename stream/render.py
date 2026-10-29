"""Timeline -> frames, drawn with Pillow and piped straight into ffmpeg (no browser).

Speed comes from two things: every visual element is a cached sprite keyed by its exact state (a token with its
suspicion arc, a quote card at word k of the karaoke, a caption), and a frame whose layer list is identical to
the previous frame's is not composited again (most of an episode is a still picture with a moving word).
`render(tl, out, workers)` splits the frames into chunks, renders them in parallel processes, and joins them.
"""
import math, os, random, subprocess, time
from functools import lru_cache
from multiprocessing import Pool

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS = 1920, 1080, 30
C = dict(bg=(13, 16, 23), panel=(24, 29, 40), ink=(238, 241, 246), muted=(139, 149, 168), dim=(92, 101, 118),
         line=(44, 52, 67), good=(134, 184, 255), evil=(255, 95, 95), poison=(180, 140, 255), amber=(255, 194, 77),
         secret=(52, 22, 28), think=(36, 28, 54), tok=(28, 35, 49), tokborder=(62, 72, 92))
FONTDIR = "/usr/share/fonts/opentype/inter/"
CX, CY, R, D = 560, 528, 300, 96
PX, PY, PW = 1100, 168, 770                      # right-hand panel
ENC = ["-c:v", "libx264", "-preset", "veryfast", "-profile:v", "high", "-pix_fmt", "yuv420p", "-r", str(FPS),
       "-g", str(2 * FPS), "-keyint_min", str(2 * FPS), "-sc_threshold", "0",
       "-b:v", "3000k", "-maxrate", "4500k", "-bufsize", "6000k", "-x264-params", "nal-hrd=vbr"]


@lru_cache(None)
def F(size, w="Regular", display=False):
    return ImageFont.truetype(FONTDIR + ("InterDisplay-" if display else "Inter-") + w + ".otf", size)


def ease(x):
    x = min(max(x, 0.0), 1.0); return x * x * (3 - 2 * x)


def fin(t, t0, d=0.35):
    return ease((t - t0) / d)


def q(a, n=12):
    return round(a * n) / n


def mix(a, b, k):
    return tuple(int(a[i] + (b[i] - a[i]) * k) for i in range(3))


def seat_xy(i, n):
    a = -math.pi / 2 + 2 * math.pi * i / n
    return CX + R * math.cos(a), CY + R * math.sin(a), a


# ---------------------------------------------------------------- text layout
def wrap(text, font, width):
    lines, cur = [], []
    for w in text.split():
        trial = " ".join(cur + [w])
        if cur and font.getlength(trial) > width:
            lines.append(cur); cur = [w]
        else:
            cur.append(w)
    if cur: lines.append(cur)
    return lines


def draw_words(d, x, y, lines, font, lh, k=None, on=C["ink"], off=C["dim"]):
    """Draw wrapped word lines; words before index k in `on`, the rest in `off` (k=None: all `on`)."""
    i = 0; sp = font.getlength(" ")
    for ln in lines:
        xx = x
        for w in ln:
            d.text((xx, y), w, font=font, fill=on if (k is None or i < k) else off)
            xx += font.getlength(w) + sp; i += 1
        y += lh
    return y


# ---------------------------------------------------------------- backgrounds
@lru_cache(None)
def background(nq, plain=False):
    """nq in 0..8: 0 = day (warm candle glow), 8 = night (cold, starry)."""
    k = nq / 8
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    base = np.array(mix((17, 20, 28), (9, 12, 20), k), np.float32)
    img = np.ones((H, W, 3), np.float32) * base
    r = np.sqrt(((xx - CX) / 760) ** 2 + ((yy - CY) / 620) ** 2)
    glow = np.clip(1 - r, 0, 1) ** 2
    warm = np.array(mix((70, 48, 22), (24, 36, 70), k), np.float32)
    img += glow[..., None] * warm * 0.55
    vig = np.clip(np.sqrt(((xx - W / 2) / (W * 0.62)) ** 2 + ((yy - H / 2) / (H * 0.62)) ** 2), 0, 1.4)
    img *= (1 - 0.35 * np.clip(vig - 0.55, 0, 1))[..., None]
    im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8), "RGB")
    if k > 0:
        rnd = random.Random(7); st = Image.new("RGBA", (W, H), (0, 0, 0, 0)); sd = ImageDraw.Draw(st)
        for _ in range(140):
            x, y = rnd.uniform(0, W), rnd.uniform(0, H * 0.9)
            if (not plain and (math.hypot(x - CX, y - CY) < R + 120 or x > PX - 40)) or y < 150: continue
            a = int(rnd.uniform(40, 150) * k); s = rnd.choice([1, 1, 1.5, 2])
            sd.ellipse([x - s, y - s, x + s, y + s], fill=(220, 228, 255, a))
        im.paste(st, (0, 0), st)
    d = ImageDraw.Draw(im, "RGBA")
    if plain: return im
    big = Image.new("RGBA", ((2 * R + 40) * 2, (2 * R + 40) * 2), (0, 0, 0, 0)); bd = ImageDraw.Draw(big)
    c = R + 20
    bd.ellipse([(c - R) * 2, (c - R) * 2, (c + R) * 2, (c + R) * 2], outline=(60, 70, 90, 120), width=4)
    big = big.resize((2 * R + 40, 2 * R + 40), Image.LANCZOS)
    im.paste(big, (CX - c, CY - c), big)
    d.line([(PX - 34, 150), (PX - 34, 900)], fill=(40, 47, 62, 255), width=2)
    return im


# ---------------------------------------------------------------- sprites
SS = 3


TS = 180                                          # token sprite size; token centre at (90, 90)


@lru_cache(4096)
def token(name, evil, demon, dead, hl, p, voted):
    """Seat token with its suspicion arc (the village's average P(Demon) for this seat)."""
    SW, SH, tx, ty = TS, TS, TS // 2, TS // 2
    big = Image.new("RGBA", (SW * SS, SH * SS), (0, 0, 0, 0)); b = ImageDraw.Draw(big)
    r = D / 2
    def circ(rad, **kw):
        b.ellipse([(tx - rad) * SS, (ty - rad) * SS, (tx + rad) * SS, (ty + rad) * SS], **kw)
    fill = (58, 26, 32) if evil else C["tok"]
    border = C["evil"] if evil else C["tokborder"]
    if hl:
        circ(r + 12, outline=C["amber"] + (90,), width=8 * SS)
    circ(r + 6, outline=(38, 44, 58, 255), width=5 * SS)                     # arc track
    if p > 0.004 and not dead:
        b.arc([(tx - r - 6) * SS, (ty - r - 6) * SS, (tx + r + 6) * SS, (ty + r + 6) * SS], -90, -90 + 360 * p,
              fill=C["amber"] + (255,), width=5 * SS)
    circ(r - 1, fill=fill + (255,), outline=border + (255,), width=(5 if demon else 3) * SS)
    sm = big.resize((SW, SH), Image.LANCZOS)
    if hl:
        g = Image.new("RGBA", (SW, SH), (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
        gd.ellipse([tx - r - 14, ty - r - 14, tx + r + 14, ty + r + 14], outline=C["amber"] + (150,), width=10)
        g = g.filter(ImageFilter.GaussianBlur(7)); g.alpha_composite(sm); sm = g
    d = ImageDraw.Draw(sm)
    nf = F(23, "Bold")
    d.text((tx, ty - (8 if p >= 0.05 else 0)), name, font=nf, fill=(255, 225, 225) if evil else C["ink"], anchor="mm")
    if p >= 0.05 and not dead:
        d.text((tx, ty + 18), f"{round(100 * p)}%", font=F(18, "SemiBold"), fill=C["amber"], anchor="mm")
    if voted:
        d.ellipse([tx + 26, ty - r - 4, tx + 56, ty - r + 26], fill=C["amber"])
        d.text((tx + 41, ty - r + 11), "✓", font=F(18, "Bold"), fill=(30, 22, 6), anchor="mm")
    if dead:
        sm.putalpha(sm.getchannel("A").point(lambda v: int(v * 0.38)))
    return sm


@lru_cache(4096)
def labels(role, evil, claim, lie, deadlabel, align):
    """Role / claim / death labels beside a token. align: 'below' (centred), 'right' (text starts at x=0), 'left'."""
    w, h = 250, 52
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    x, an = {"below": (w / 2, "m"), "right": (0, "l"), "left": (w, "r")}[align]
    l2 = deadlabel or (f"claims {claim}" if claim else "")
    y1 = 14 if (l2 or align == "below") else 26
    d.text((x, y1), role, font=F(18, "SemiBold"), fill=C["evil"] if evil else C["good"], anchor=an + "m")
    if l2:
        col = C["muted"] if deadlabel or not lie else (255, 150, 120)
        d.text((x, 38), l2, font=F(16, "Medium"), fill=col, anchor=an + "m")
    if deadlabel:
        im.putalpha(im.getchannel("A").point(lambda v: int(v * 0.6)))
    return im


@lru_cache(512)
def links_sprite(items, p):
    """Lines between tokens: whisper (dotted blue-grey), nominate (white arrow), kill (red), poison (purple), shoot."""
    big = Image.new("RGBA", (1100 * 2, H * 2), (0, 0, 0, 0)); b = ImageDraw.Draw(big)
    col = {"whisper": (170, 185, 210), "nominate": C["ink"], "kill": C["evil"], "poison": C["poison"], "shoot": C["good"]}
    for (style, ax, ay, bx, by) in items:
        dx, dy = bx - ax, by - ay; L = math.hypot(dx, dy) or 1; ux, uy = dx / L, dy / L
        pad = D / 2 + 14
        x1, y1 = ax + ux * pad, ay + uy * pad; x2, y2 = bx - ux * (pad + 4), by - uy * (pad + 4)
        ex, ey = x1 + (x2 - x1) * p, y1 + (y2 - y1) * p
        c = col[style] + (235,); w = 5 if style != "whisper" else 4
        if style in ("whisper", "poison"):
            n = int(math.hypot(ex - x1, ey - y1) / 18)
            for i in range(n):
                sx, sy = x1 + ux * i * 18, y1 + uy * i * 18
                b.line([(sx * 2, sy * 2), ((sx + ux * 9) * 2, (sy + uy * 9) * 2)], fill=c, width=w * 2)
        else:
            b.line([(x1 * 2, y1 * 2), (ex * 2, ey * 2)], fill=c, width=w * 2)
        if p > 0.1 and style != "whisper":
            s = 20; hx, hy = ex - ux * s, ey - uy * s; nx, ny = -uy * s * 0.6, ux * s * 0.6
            b.polygon([(ex * 2, ey * 2), ((hx + nx) * 2, (hy + ny) * 2), ((hx - nx) * 2, (hy - ny) * 2)], fill=c)
    return big.resize((1100, H), Image.LANCZOS)


def lock_icon(d, x, y, col):
    d.rounded_rectangle([x, y + 9, x + 18, y + 24], 3, fill=col)
    d.arc([x + 3, y, x + 15, y + 16], 180, 360, fill=col, width=3)


@lru_cache(256)
def card(kind, who, role, side, to, secret, text, k):
    """A quote card (say / whisper / think / nom / defense), karaoke-highlighted up to word k."""
    pad = 34; inner = PW - 2 * pad - 10
    italic = kind == "think"
    qf = F(35, "Italic" if italic else "Regular") if True else None
    lines = wrap("“" + text + "”", qf, inner)
    lh = 48
    h = 150 + lh * len(lines) + 20
    im = Image.new("RGBA", (PW, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    bgc = C["secret"] if (secret or (kind == "think" and side == "evil")) else (C["think"] if kind == "think" else C["panel"])
    d.rounded_rectangle([0, 0, PW - 1, h - 1], 20, fill=bgc + (245,))
    acc = C["evil"] if side == "evil" else C["good"]
    d.rounded_rectangle([0, 0, 9, h - 1], 4, fill=acc + (255,))
    label = {"say": "TOWN SQUARE · EVERYONE HEARS", "whisper": "WHISPER · PRIVATE", "think": "PRIVATE THOUGHTS · ONLY YOU SEE THIS",
             "nom": "NOMINATION", "defense": "DEFENCE · ON TRIAL"}[kind]
    if secret: label = "SECRET · EVIL TEAM CHAT"
    x = pad + 10; y = 26
    if secret or kind == "think":
        lock_icon(d, x, y - 4, C["evil"] if side == "evil" else C["poison"]); x2 = x + 30
    else:
        x2 = x
    d.text((x2, y), label, font=F(20, "Bold"), fill=C["evil"] if secret else (C["poison"] if kind == "think" else C["muted"]))
    y = 62
    nf = F(34, "Bold")
    d.text((x, y), who, font=nf, fill=C["ink"]); xx = x + nf.getlength(who)
    if to:
        s = "  →  " + ", ".join(to)
        d.text((xx, y + 3), s, font=F(28, "SemiBold"), fill=C["ink"]); xx += F(28, "SemiBold").getlength(s)
    rs = f"  ·  {role} · {side}"
    d.text((xx, y + 6), rs, font=F(25, "SemiBold"), fill=acc)
    draw_words(d, x, 122, lines, qf, lh, k, on=(255, 255, 255), off=(118, 127, 145))
    return im


def nwords(text):
    return len(("“" + text + "”").split())


@lru_cache(64)
def night_card(title, lines, n_shown):
    pad = 34; inner = PW - 2 * pad - 40
    f = F(26, "Medium"); rows = []
    for (t, c, tag) in lines:
        rows.append((wrap(t, f, inner - (110 if tag else 0)), c, tag))
    h = 120 + sum(36 * len(r[0]) + 14 for r in rows) + 20
    im = Image.new("RGBA", (PW, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, PW - 1, h - 1], 20, fill=(18, 22, 36, 240))
    d.ellipse([pad, 30, pad + 34, 64], fill=(230, 226, 205)); d.ellipse([pad + 10, 24, pad + 44, 58], fill=(18, 22, 36))
    d.text((pad + 56, 30), title.upper(), font=F(30, "Bold"), fill=C["ink"])
    d.text((pad + 56 + F(30, "Bold").getlength(title.upper()) + 18, 37), "WHAT HAPPENED IN THE DARK", font=F(19, "Bold"), fill=C["muted"])
    y = 100
    colmap = {"poison": C["poison"], "evil": C["evil"], "good": C["good"], "info": C["muted"]}
    for i, (ls, c, tag) in enumerate(rows):
        if i >= n_shown: break
        d.ellipse([pad, y + 11, pad + 12, y + 23], fill=colmap[c])
        yy = draw_words(d, pad + 26, y, ls, f, 36, on=C["ink"] if c != "info" else (205, 211, 222))
        if tag:
            tw = F(18, "Bold").getlength(tag) + 22
            d.rounded_rectangle([PW - pad - tw, y + 4, PW - pad, y + 32], 14, fill=C["poison"])
            d.text((PW - pad - tw / 2, y + 18), tag, font=F(18, "Bold"), fill=(22, 12, 34), anchor="mm")
        y = yy + 14
    return im


@lru_cache(64)
def dawn_card(title, text, deaths):
    pad = 34; f = F(30, "Italic"); lines = wrap(text, f, PW - 2 * pad)
    h = 130 + 42 * len(lines) + (70 if deaths else 30)
    im = Image.new("RGBA", (PW, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, PW - 1, h - 1], 20, fill=C["panel"] + (240,))
    d.ellipse([pad, 30, pad + 34, 64], fill=C["amber"])
    d.text((pad + 56, 30), title.upper(), font=F(30, "Bold"), fill=C["ink"])
    d.text((pad + 56 + F(30, "Bold").getlength(title.upper()) + 18, 37), "DAWN", font=F(19, "Bold"), fill=C["muted"])
    y = draw_words(d, pad, 100, lines, f, 42, on=(214, 219, 229))
    if deaths:
        d.text((pad, y + 16), "Dead: " + ", ".join(deaths), font=F(28, "Bold"), fill=C["evil"])
    return im


@lru_cache(32)
def poll_card(values, top, demon, alive):
    pad = 34
    rows = sorted([(v, n) for n, v in values if n in alive], reverse=True)[:6]
    h = 150 + 62 * len(rows) + 60
    im = Image.new("RGBA", (PW, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, PW - 1, h - 1], 20, fill=C["panel"] + (240,))
    d.text((pad, 28), "PRIVATE POLL · WHO IS THE DEMON?", font=F(20, "Bold"), fill=C["muted"])
    d.text((pad, 62), "Average belief of the living good players", font=F(26, "Medium"), fill=C["ink"])
    y = 120; bw = PW - 2 * pad - 300
    for v, n in rows:
        d.text((pad, y + 6), n, font=F(28, "Bold"), fill=C["ink"])
        x0 = pad + 140
        d.rounded_rectangle([x0, y + 14, x0 + bw, y + 30], 8, fill=(38, 44, 58))
        d.rounded_rectangle([x0, y + 14, x0 + max(bw * v, 10), y + 30], 8, fill=C["amber"])
        d.text((x0 + bw + 18, y + 4), f"{round(100 * v)}%", font=F(30, "Bold"), fill=C["amber"])
        if n == demon:
            d.rounded_rectangle([PW - pad - 76, y + 6, PW - pad, y + 38], 16, fill=C["evil"])
            d.text((PW - pad - 38, y + 22), "Demon", font=F(17, "Bold"), fill=(30, 10, 12), anchor="mm")
        y += 62
    d.text((pad, y + 14), "Only you can see who the Demon really is.", font=F(22, "Medium"), fill=C["muted"])
    return im


@lru_cache(8)
def roles_card(seats, focus):
    pad = 34; n = len(seats); rows = (n + 1) // 2
    h = 84 + rows * 58 + 16
    im = Image.new("RGBA", (PW, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, PW - 1, h - 1], 20, fill=C["panel"] + (240,))
    lock_icon(d, pad, 24, C["evil"])
    d.text((pad + 30, 28), "WHO'S WHO · ONLY YOU SEE THIS", font=F(20, "Bold"), fill=C["muted"])
    for i, (name, role, evil) in enumerate(seats):
        cx = pad + (i // rows) * (PW // 2 - 10); y = 84 + (i % rows) * 58
        on = not focus or name in focus
        a = 255 if on else 110
        d.text((cx, y), name, font=F(28, "Bold"), fill=C["ink"] + (a,))
        d.text((cx + 120, y + 3), role, font=F(25, "SemiBold"), fill=(C["evil"] if evil else C["good"]) + (a,))
    return im


@lru_cache(64)
def section_card(title, sub):
    pad = 34; f = F(28, "Medium"); lines = wrap(sub, f, PW - 2 * pad)
    h = 110 + 40 * len(lines) + 30
    im = Image.new("RGBA", (PW, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, PW - 1, h - 1], 20, fill=C["panel"] + (225,))
    d.text((pad, 30), title.upper(), font=F(34, "Bold"), fill=C["ink"])
    draw_words(d, pad, 92, lines, f, 40, on=C["muted"])
    return im


@lru_cache(4)
def legend_card():
    pad = 34; h = 420
    im = Image.new("RGBA", (PW, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, PW - 1, h - 1], 20, fill=C["panel"] + (240,))
    d.text((pad, 28), "HOW TO READ THE TABLE", font=F(20, "Bold"), fill=C["muted"])
    rows = [(C["evil"], "Red seats are evil. The village can't see this."),
            (C["amber"], "The amber ring is the village's average belief that the player is the Demon, from private polls of the good players."),
            (C["muted"], "Faded seats are dead. The dead keep talking, and keep one last vote."),
            (C["poison"], "Purple panels are private thoughts; red panels are the evil team's secret chat.")]
    y = 80; f = F(26, "Medium")
    for col, t in rows:
        d.ellipse([pad, y + 8, pad + 18, y + 26], fill=col)
        y = draw_words(d, pad + 36, y, wrap(t, f, PW - 2 * pad - 40), f, 36) + 18
    return im


@lru_cache(8)
def outcome_card(team, text, reason, evil_list):
    pad = 34; f = F(28, "Medium"); lines = wrap(reason, f, PW - 2 * pad)
    h = 170 + 40 * len(lines) + 40 + 34 * len(wrap("Evil team: " + evil_list, F(25, "SemiBold"), PW - 2 * pad)) + 30
    im = Image.new("RGBA", (PW, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    col = C["evil"] if team == "evil" else C["good"]
    d.rounded_rectangle([0, 0, PW - 1, h - 1], 20, fill=C["panel"] + (245,), outline=col, width=4)
    d.text((pad, 26), "GAME OVER", font=F(20, "Bold"), fill=C["muted"])
    d.text((pad, 58), text, font=F(64, "ExtraBold", True), fill=col)
    y = draw_words(d, pad, 150, lines, f, 40, on=C["ink"])
    ef = F(25, "SemiBold")
    draw_words(d, pad, y + 20, wrap("Evil team: " + evil_list, ef, PW - 2 * pad), ef, 34, on=C["evil"])
    return im


@lru_cache(256)
def caption(text):
    f = F(46, "SemiBold"); w = int(f.getlength(text)) + 64
    lines = [text]
    if w > 1700:
        lines = [" ".join(l) for l in wrap(text, f, 1640)]; w = int(max(f.getlength(l) for l in lines)) + 64
    h = 30 + 58 * len(lines)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], 14, fill=(5, 7, 11, 215))
    for i, l in enumerate(lines):
        d.text((w / 2, 15 + 29 + 58 * i), l, font=f, fill=(255, 255, 255), anchor="mm")
    return im


@lru_cache(64)
def center(phase, sub, vote, outcome):
    """Ring centre: day/night label, the vote counter, the result."""
    im = Image.new("RGBA", (440, 380), (0, 0, 0, 0)); d = ImageDraw.Draw(im); x = 220
    y = 70 if not vote and not outcome else 34
    d.text((x, y), phase.upper(), font=F(34, "Bold"), fill=C["muted"], anchor="mm")
    if sub: d.text((x, y + 40), sub, font=F(24, "Medium"), fill=C["dim"], anchor="mm")
    if vote:
        nominee, n, need, total = vote
        d.text((x, 118), f"vote on {nominee}", font=F(26, "SemiBold"), fill=C["ink"], anchor="mm")
        d.text((x, 200), str(n), font=F(120, "ExtraBold", True), fill=C["amber"] if n >= need else C["ink"], anchor="mm")
        d.text((x, 282), f"votes · {need} needed", font=F(24, "SemiBold"), fill=C["muted"], anchor="mm")
    if outcome:
        team, text = outcome
        d.text((x, 200), text, font=F(58, "ExtraBold", True), fill=C["evil"] if team == "evil" else C["good"], anchor="mm")
    return im


@lru_cache(4)
def header(evil, good, title):
    im = Image.new("RGBA", (W, 130), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    x = 56; y = 34
    if title:
        d.text((x, y - 4), title, font=F(40, "ExtraBold", True), fill=C["ink"]); y += 52
    for lab, name, col in (("EVIL", evil, C["evil"]), ("GOOD", good, C["good"])):
        tw = F(17, "Bold").getlength(lab) + 20
        d.rounded_rectangle([x, y, x + tw, y + 28], 14, fill=col)
        d.text((x + tw / 2, y + 14), lab, font=F(17, "Bold"), fill=(15, 15, 20), anchor="mm")
        d.text((x + tw + 10, y + 1), name, font=F(23, "SemiBold"), fill=C["ink"])
        x += tw + 26 + F(23, "SemiBold").getlength(name) + 22
    d.text((W - 56, 40), "clocktowerbench.com", font=F(24, "SemiBold"), fill=C["muted"], anchor="ra")
    d.text((W - 56, 72), "AI models playing Blood on the Clocktower", font=F(18, "Medium"), fill=C["dim"], anchor="ra")
    return im


def tower(d, x, y, s, col):
    """A simple original clock-tower silhouette (base at x, y; scale s)."""
    d.rectangle([x - 60 * s, y - 330 * s, x + 60 * s, y], fill=col)
    d.polygon([(x - 78 * s, y - 330 * s), (x + 78 * s, y - 330 * s), (x, y - 520 * s)], fill=col)
    d.rectangle([x - 90 * s, y - 120 * s, x + 90 * s, y], fill=col)
    d.ellipse([x - 42 * s, y - 290 * s, x + 42 * s, y - 206 * s], fill=(13, 16, 23, 255))
    d.ellipse([x - 36 * s, y - 284 * s, x + 36 * s, y - 212 * s], outline=col, width=max(2, int(4 * s)))
    d.line([(x, y - 248 * s), (x, y - 274 * s)], fill=col, width=max(2, int(5 * s)))
    d.line([(x, y - 248 * s), (x + 20 * s, y - 238 * s)], fill=col, width=max(2, int(5 * s)))
    d.rectangle([x - 14 * s, y - 60 * s, x + 14 * s, y], fill=(255, 190, 90, 200))


@lru_cache(4)
def title_card(title, evil, good, sub, highlight):
    im = Image.new("RGBA", (W, H), (9, 11, 17, 255)); d = ImageDraw.Draw(im, "RGBA")
    g = Image.new("RGBA", (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
    gd.ellipse([1340, 560, 1700, 920], fill=(255, 170, 70, 60)); g = g.filter(ImageFilter.GaussianBlur(90)); im.alpha_composite(g)
    tower(d, 1520, 980, 1.25, (34, 40, 56, 255))
    d.text((140, 300), "CLOCKTOWER BENCH · " + ("FEATURED GAME" if highlight else "REPLAY"), font=F(28, "Bold"), fill=C["amber"])
    tf = F(104 if len(title) < 22 else 80, "ExtraBold", True)
    lines = wrap(title, tf, 1150); y = 350
    for ln in lines:
        d.text((136, y), " ".join(ln), font=tf, fill=C["ink"]); y += int(tf.size * 1.12)
    y += 30
    for lab, name, col in (("EVIL", evil, C["evil"]), ("GOOD", good, C["good"])):
        d.text((140, y), lab, font=F(30, "Bold"), fill=col); d.text((250, y), name, font=F(36, "SemiBold"), fill=C["ink"]); y += 56
    d.text((140, y + 20), sub, font=F(24, "Medium"), fill=C["muted"])
    return im


@lru_cache(2)
def chart_card(points, demons, evil, seats, winner, roles):
    """End card: the village's average P(Demon) on every player, poll by poll."""
    points = [(dd, pp, dict(m)) for dd, pp, m in points]; roles = dict(roles)
    im = Image.new("RGBA", (W, H), (11, 14, 20, 255)); big = Image.new("RGBA", (W * 2, H * 2), (0, 0, 0, 0))
    b = ImageDraw.Draw(big); d = ImageDraw.Draw(im)
    d.text((120, 70), "WHO THE VILLAGE SUSPECTED", font=F(26, "Bold"), fill=C["muted"])
    d.text((120, 108), "Average belief of the living good players that each player is the Demon, at each poll",
           font=F(32, "Medium"), fill=C["ink"])
    x0, x1, y0, y1 = 200, 1500, 220, 900
    labels = [("Day %d dawn" if p == "dawn" else "Day %d") % dd for dd, p, _ in points]
    n = len(points)
    X = lambda i: x0 + (x1 - x0) * (i / max(n - 1, 1)); Y = lambda v: y1 - (y1 - y0) * v
    for v in (0, 0.25, 0.5, 0.75, 1.0):
        d.line([(x0, Y(v)), (x1, Y(v))], fill=(40, 47, 62), width=2)
        d.text((x0 - 20, Y(v)), f"{int(v * 100)}%", font=F(22, "Medium"), fill=C["muted"], anchor="rm")
    step = max(1, n // 8)
    for i, l in enumerate(labels):
        if i % step == 0 or i == n - 1:
            d.text((X(i), y1 + 30), l, font=F(20, "Medium"), fill=C["muted"], anchor="mm")
    order = sorted(seats, key=lambda s: (s in demons, s in evil))
    ends = []
    for s in order:
        pts = [(X(i), Y(m[s])) for i, (_, _, m) in enumerate(points) if s in m]
        if len(pts) < 1: continue
        col = C["evil"] + (255,) if s in demons else ((255, 140, 120, 200) if s in evil else (120, 135, 160, 150))
        w = 10 if s in demons else (6 if s in evil else 4)
        b.line([(x * 2, y * 2) for x, y in pts], fill=col, width=w, joint="curve")
        for x, y in pts:
            b.ellipse([x * 2 - w, y * 2 - w, x * 2 + w, y * 2 + w], fill=col)
        ends.append((pts[-1][1], s, col))
    im.alpha_composite(big.resize((W, H), Image.LANCZOS))
    used = []
    for y, s, col in sorted(ends, reverse=True):
        if s not in demons and s not in evil and y > Y(0.12): continue
        yy = min(y, y1 - 10)
        while any(abs(yy - u) < 30 for u in used): yy -= 30
        used.append(yy)
        lab = f"{s} ({'Demon' if s in demons else roles.get(s, '')})"
        d.text((x1 + 24, yy), lab, font=F(26, "Bold"), fill=col[:3], anchor="lm")
    d.text((120, 990), ("Evil wins." if winner == "evil" else "Good wins.") + "  Red: the evil team. Thick red: the Demon.",
           font=F(26, "SemiBold"), fill=C["evil"] if winner == "evil" else C["good"])
    return im


@lru_cache(8)
def promo_card(board, games, variant, next_title, next_sub):
    """Between-games card: what this is, the leaderboard, the URL, and what's next."""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im, "RGBA")
    g = Image.new("RGBA", (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
    gd.ellipse([60, 560, 700, 1080], fill=(255, 170, 70, 40)); g = g.filter(ImageFilter.GaussianBlur(80)); im.alpha_composite(g)
    x = 120
    d.text((x, 110), "CLOCKTOWER BENCH", font=F(30, "Bold"), fill=C["amber"])
    tf = F(64, "ExtraBold", True); y = 160
    for ln in wrap("AI models playing Blood on the Clocktower", tf, 860):
        d.text((x, y), " ".join(ln), font=tf, fill=C["ink"]); y += 74
    body = ["One model plays the village. Another plays the Demon and its Minions, who lie for it.",
            "These are replays of real games, condensed. You see every secret; the village doesn't."][:2]
    f = F(30, "Medium"); y += 24
    for para in body:
        y = draw_words(d, x, y, wrap(para, f, 860), f, 42, on=(205, 211, 222)) + 16
    d.text((x, y + 20), "clocktowerbench.com", font=F(52, "ExtraBold", True), fill=C["amber"])
    # leaderboard
    lx, ly, lw = 1120, 110, 680
    d.rounded_rectangle([lx - 30, ly - 30, lx + lw + 30, ly + 110 + 52 * len(board) + 30], 22, fill=(20, 25, 35, 235))
    d.text((lx, ly), "LEADERBOARD", font=F(24, "Bold"), fill=C["muted"])
    d.text((lx, ly + 34), f"Elo from {games} games · good and evil combined", font=F(22, "Medium"), fill=C["dim"])
    lo, hi = min(b[1] for b in board) - 120, max(b[1] for b in board)
    for i, (name, elo, lab) in enumerate(board):
        yy = ly + 96 + 52 * i
        d.text((lx, yy), f"{i + 1}", font=F(26, "Bold"), fill=C["muted"])
        d.text((lx + 44, yy), name, font=F(27, "SemiBold"), fill=C["ink"])
        bx = lx + 330; bw = (lw - 330 - 80) * (elo - lo) / (hi - lo)
        col = (214, 160, 120) if lab == "Anthropic" else (120, 190, 170)
        d.rounded_rectangle([bx, yy + 8, bx + bw, yy + 26], 8, fill=col)
        d.text((lx + lw, yy), str(elo), font=F(26, "Bold"), fill=C["ink"], anchor="ra")
    yy = ly + 96 + 52 * len(board) + 4
    d.ellipse([lx, yy + 6, lx + 14, yy + 20], fill=(214, 160, 120)); d.text((lx + 22, yy), "Anthropic", font=F(20, "Medium"), fill=C["muted"])
    d.ellipse([lx + 150, yy + 6, lx + 164, yy + 20], fill=(120, 190, 170)); d.text((lx + 172, yy), "OpenAI", font=F(20, "Medium"), fill=C["muted"])
    # up next
    d.text((x, 700), "UP NEXT", font=F(24, "Bold"), fill=C["muted"])
    d.text((x, 732), next_title, font=F(48, "ExtraBold", True), fill=C["ink"])
    d.text((x, 796), next_sub, font=F(26, "Medium"), fill=C["muted"])
    return im


# ---------------------------------------------------------------- state fold
class State:
    def __init__(self, tl):
        self.tl = tl; self.i = 0
        self.seats = []; self.dead = {}; self.role = {}; self.claim = {}; self.hl = ((), 0); self.links = ((), 0)
        self.votes = None; self.phase = ("", False, -9, False); self.panel = None; self.prev_panel = None
        self.title = None; self.untitle = None; self.outcome = None; self.chart = None; self.fade = None
        self.susp = {}; self.susp_prev = {}; self.susp_t = -9; self.ring_t = 0; self.promo = None

    def advance(self, t):
        ev = self.tl["events"]
        while self.i < len(ev) and ev[self.i]["t"] <= t:
            self.apply(ev[self.i]); self.i += 1

    def apply(self, e):
        k, t = e["k"], e["t"]
        if k == "ring": self.seats = e["seats"]; self.ring_t = t
        elif k == "title": self.title = (e, t)
        elif k == "untitle": self.untitle = t
        elif k == "phase": self.phase = (e["text"], e.get("night", False), t, self.phase[1])
        elif k == "panel":
            self.prev_panel = (self.panel[0], t) if self.panel else None; self.panel = (e, t)
        elif k == "hl": self.hl = (tuple(e["names"]), t)
        elif k == "links": self.links = (tuple((x["style"], x["from"], tuple(x["to"])) for x in e["items"]), t)
        elif k == "dead": self.dead.setdefault(e["name"], (t, e.get("how", "")))
        elif k == "role": self.role[e["name"]] = (e["role"], e.get("demon", False))
        elif k == "claim": self.claim[e["name"]] = (e["role"], e.get("lie", False))
        elif k == "susp":
            self.susp_prev = self.cur_susp(t); self.susp = e["values"]; self.susp_t = t
        elif k == "votes": self.votes = (e, t)
        elif k == "clearvotes": self.votes = None
        elif k == "outcome": self.outcome = (e, t); self.votes = None
        elif k == "chart": self.chart = (e, t)
        elif k == "fade": self.fade = t
        elif k == "promo": self.promo = (e, t)

    def cur_susp(self, t):
        a = ease((t - self.susp_t) / 0.9)
        names = set(self.susp) | set(self.susp_prev)
        return {n: self.susp_prev.get(n, 0) + (self.susp.get(n, 0) - self.susp_prev.get(n, 0)) * a for n in names}


def karaoke_k(tl, e, t):
    if "clip" not in e: return None
    c = tl["clips"][e["clip"]]; ct = c["chartime"]
    if t >= c["start"] + c["dur"]: return 10 ** 6
    if t < c["start"]: return 0
    spoken = sum(1 for x in ct if x <= t) / max(len(ct), 1)
    shown = "“" + c["show"] + "”"; ws = shown.split(); pos = 0; k = 0
    for i, w in enumerate(ws):
        j = shown.find(w, pos); pos = j + len(w)
        if j / max(len(shown), 1) <= spoken: k = i + 1
    return k


def panel_sprite(tl, st, e, t):
    ty = e.get("type")
    if ty in ("say", "whisper", "think", "nom", "defense"):
        k = karaoke_k(tl, e, t)
        n = nwords(e["text"])
        k = n if k is None or k >= n else k
        return ("card", e["text"][:40], k), card(ty, e["who"], e.get("role", ""), e.get("side", "good"), tuple(e.get("to") or ()),
                                                bool(e.get("secret")), e["text"], k)
    if ty == "night":
        lines = tuple((x["t"], x["c"], x.get("tag") or "") for x in e["lines"])
        return ("night", e["title"]), night_card(e["title"], lines, len(lines))
    if ty == "dawn":
        return ("dawn", e["title"]), dawn_card(e["title"], e.get("text", ""), tuple(e.get("deaths", [])))
    if ty == "poll":
        alive = tuple(s["name"] for s in st.seats if s["name"] not in st.dead or st.dead[s["name"]][0] > e["t"])
        vals = tuple(sorted(e["values"].items()))
        return ("poll", vals), poll_card(vals, e["top"], e["demon"], alive)
    if ty == "roles":
        seats = tuple((s["name"], s["role"], s["evil"]) for s in st.seats)
        return ("roles", tuple(e.get("focus", []))), roles_card(seats, tuple(e.get("focus", [])))
    if ty == "legend":
        return ("legend",), legend_card()
    if ty == "section":
        return ("section", e["title"], e["sub"]), section_card(e["title"], e["sub"])
    return None, None


class Frame:
    def __init__(self, tl):
        self.tl = tl; self.st = State(tl); self.prev_key = None; self.prev_bytes = None
        self.alpha_cache = {}
        n = len(tl["seats"]); self.pos = {s: seat_xy(i, n)[:2] for i, s in enumerate(tl["seats"])}
        self.align = {}
        for i, s in enumerate(tl["seats"]):
            a = seat_xy(i, n)[2]
            self.align[s] = "below" if abs(math.cos(a)) < 0.45 else ("right" if math.cos(a) > 0 else "left")
        self.stats = [0, 0]

    def faded(self, key, img, a):
        if a >= 0.999: return img
        k = (key, a)
        if k not in self.alpha_cache:
            if len(self.alpha_cache) > 400: self.alpha_cache.clear()
            im = img.copy(); im.putalpha(img.getchannel("A").point(lambda v: int(v * a))); self.alpha_cache[k] = im
        return self.alpha_cache[k]

    def layers(self, t):
        st = self.st; st.advance(t); tl = self.tl; L = []
        nq = 8 if st.phase[1] else 0
        if st.phase[1] != st.phase[3]:
            k = fin(t, st.phase[2], 1.2); nq = round(8 * (k if st.phase[1] else 1 - k))
        card = tl.get("kind") == "card"
        L.append((("bg", nq, card), lambda: background(nq, card), 0, 0, 1.0))
        if tl.get("kind") == "card":
            if st.promo:
                e, t0 = st.promo
                pk = (tuple(tuple(b) for b in e["board"]), e["games"], e["variant"], e["next_title"], e["next_sub"])
                L.append((("promo",) + pk, lambda: promo_card(*pk), 0, 0, q(fin(t, t0, 0.8))))
        elif st.chart and fin(t, st.chart[1], 0.8) >= 1:
            pass
        else:
            ring_a = q(fin(t, st.ring_t + 0.2, 0.8))
            # links
            if st.links[0]:
                p = q(fin(t, st.links[1], 0.5), 10)
                items = tuple((s, *self.pos[a], *self.pos[b]) for s, a, bs in st.links[0] for b in bs if a in self.pos and b in self.pos)
                L.append((("links", items, p), lambda items=items, p=p: links_sprite(items, p), 0, 0, 1.0))
            # tokens
            sus = st.cur_susp(t)
            hl = st.hl[0]; voters = ()
            if st.votes:
                ve, vt = st.votes; nshow = min(len(ve["voters"]), max(0, int((t - vt - 0.15) / 0.16) + 1)) if t >= vt + 0.15 else 0
                voters = tuple(ve["voters"][:nshow])
            for s in st.seats:
                n = s["name"]; role, demon = st.role.get(n, (s["role"], s["demon"]))
                dead = n in st.dead and t >= st.dead[n][0] + 0.2
                cl = st.claim.get(n, (None, False))
                args = (n, s["evil"], demon or s["demon"], dead, n in hl, q(sus.get(n, 0), 100), n in voters)
                x, y = self.pos[n]
                L.append((("tok",) + args, lambda args=args: token(*args), int(x - TS // 2), int(y - TS // 2), ring_a))
                al = self.align[n]
                la = (role, s["evil"], cl[0], cl[1], st.dead[n][1] if dead else "", al)
                lx = {"below": x - 125, "right": x + D / 2 + 14, "left": x - D / 2 - 14 - 250}[al]
                ly = y + D / 2 + 6 if al == "below" else y - 26
                L.append((("lab",) + la, lambda la=la: labels(*la), int(lx), int(ly), ring_a))
            # centre
            ph = st.phase[0]; main, _, sub = ph.partition(" · ")
            vote = None
            if st.votes:
                ve, vt = st.votes
                vote = (ve["nominee"], len(voters), ve["needed"], len(ve["voters"]))
            oc = (st.outcome[0]["team"], st.outcome[0]["text"]) if st.outcome else None
            ck = (main, sub, vote, oc)
            L.append((("ctr",) + ck, lambda ck=ck: center(*ck), CX - 220, CY - 190, ring_a))
            # panel
            if st.outcome:
                oe = st.outcome[0]; ev = "  ·  ".join(f"{s['name']}: {st.role.get(s['name'], (s['role'],))[0]}" for s in st.seats if s["evil"])
                key = ("outcome", oe["text"])
                L.append((key, lambda: outcome_card(oe["team"], oe["text"], oe["reason"], ev), PX, PY, q(fin(t, st.outcome[1], 0.5))))
            elif st.panel:
                e, t0 = st.panel
                a = q(fin(t, t0, 0.3), 10)
                if st.prev_panel and a < 1:
                    pe, _ = st.prev_panel
                    pk, pim = panel_sprite(tl, st, pe, t)
                    if pk: L.append((pk, lambda pim=pim: pim, PX, PY, q(1 - a, 10)))
                key, im = panel_sprite(tl, st, e, t)
                if key:
                    dy = int(14 * (1 - a))
                    L.append((key, lambda im=im: im, PX, PY + dy, a))
            hk = (tl["evil"], tl["good"], tl.get("title") or "")
            L.append((("hdr",) + hk, lambda: header(*hk), 0, 0, q(fin(t, st.ring_t + 0.4, 0.8))))
        # title overlay
        if st.title:
            e, t0 = st.title
            a = 1.0 if st.untitle is None else 1 - fin(t, st.untitle, 0.6)
            a = q(a * fin(t, t0 - 0.3, 0.3), 12)
            if a > 0:
                tk = (e["title"], e["evil"], e["good"], e["sub"], e["highlight"])
                L.append((("title",) + tk, lambda: title_card(*tk), 0, 0, a))
        if st.chart:
            e, t0 = st.chart
            ck = (tuple((d, p, tuple(sorted(m.items()))) for d, p, m in e["points"]), tuple(e["demons"]), tuple(e["evil"]),
                  tuple(tl["seats"]), e["winner"], tuple(sorted(e.get("roles", {}).items())))
            L.append((("chart", ck), lambda: chart_card(*ck), 0, 0, q(fin(t, t0, 0.8))))
        # caption
        cap = next((c for c in tl["captions"] if c["start"] <= t < c["end"]), None)
        if cap:
            a = q(min(fin(t, cap["start"], 0.08), 1 - fin(t, cap["end"] - 0.08, 0.08)), 6)
            im = caption(cap["text"])
            L.append((("cap", cap["text"]), lambda im=im: im, (W - im.width) // 2, H - 40 - im.height, a))
        if st.fade:
            a = q(fin(t, st.fade, 1.2), 12)
            L.append((("black",), lambda: BLACK, 0, 0, a))
        return L

    def frame(self, t):
        L = self.layers(t)
        key = tuple((l[0], l[2], l[3], l[4]) for l in L if l[4] > 0)
        if key == self.prev_key:
            self.stats[1] += 1; return self.prev_bytes
        self.stats[0] += 1
        base = None
        for k, fn, x, y, a in L:
            if a <= 0: continue
            img = fn()
            if base is None:
                base = img.convert("RGB").copy() if img.mode != "RGB" else img.copy(); continue
            im = self.faded(k, img, a)
            base.paste(im, (x, y), im)
        self.prev_key, self.prev_bytes = key, base.tobytes()
        return self.prev_bytes


BLACK = Image.new("RGBA", (W, H), (0, 0, 0, 255))


def _chunk(args):
    tl, a, b, out = args
    fr = Frame(tl)
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", *ENC, "-threads", "2", "-an", out], stdin=subprocess.PIPE)
    for i in range(a, b):
        p.stdin.write(fr.frame(i / FPS))
    p.stdin.close(); p.wait()
    return fr.stats


def render(tl, out_mp4, wav, workers=4, tmp=None, t0=0.0, t1=None):
    """Render frames [t0, t1) in `workers` parallel chunks, join them and add the soundtrack."""
    n0 = int(t0 * FPS); n1 = int((t1 or tl["total"]) * FPS)
    tmp = tmp or (os.path.splitext(out_mp4)[0] + "_parts"); os.makedirs(tmp, exist_ok=True)
    k = max(1, workers); cuts = [n0 + (n1 - n0) * i // k for i in range(k + 1)]
    # cut on 2 s boundaries so every chunk starts on a keyframe of the joined stream
    cuts = [cuts[0]] + [c - (c - n0) % (2 * FPS) for c in cuts[1:-1]] + [cuts[-1]]
    jobs = [(tl, cuts[i], cuts[i + 1], f"{tmp}/part{i:02d}.mp4") for i in range(k) if cuts[i + 1] > cuts[i]]
    s = time.time()
    with Pool(len(jobs)) as pool:
        stats = pool.map(_chunk, jobs)
    with open(f"{tmp}/list.txt", "w") as f:
        for j in jobs: f.write(f"file '{os.path.abspath(j[3])}'\n")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", f"{tmp}/list.txt",
                    "-ss", str(t0), "-t", str((n1 - n0) / FPS), "-i", str(wav),
                    "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "128k", "-ar", "44100", "-ac", "2",
                    "-shortest", "-movflags", "+faststart", out_mp4], check=True)
    el = time.time() - s
    drawn = sum(x[0] for x in stats); reused = sum(x[1] for x in stats)
    return {"frames": n1 - n0, "seconds": round(el, 1), "fps": round((n1 - n0) / el, 1), "drawn": drawn, "reused": reused}


def stills(tl, times, outdir):
    os.makedirs(outdir, exist_ok=True); fr = Frame(tl); paths = []
    for t in sorted(times):
        img = Image.frombytes("RGB", (W, H), fr.frame(t)); p = f"{outdir}/t{t:07.1f}.png"; img.save(p); paths.append(p)
    return paths
