"""The layers: each one takes an image and returns that image wrapped in one more frame.

Every function is deterministic given its ``rng`` (a ``random.Random``), takes any RGB image
(so layers compose in any order) and returns an RGB image whose long side is at most ``MAX``.

Captions never name the subject: a caption that said "Annunciation" would test reading, not
framing. A separate, explicit caption experiment can be run later with ``caption=``.
"""

from __future__ import annotations

import random
from collections.abc import Callable

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

MAX = 960
SERIF = "/System/Library/Fonts/Supplemental/Times New Roman.ttf"
SERIF_IT = "/System/Library/Fonts/Supplemental/Times New Roman Italic.ttf"
SANS = "/System/Library/Fonts/Helvetica.ttc"

NEUTRAL_CAPTIONS = [
    "Collection particulière.",
    "Musée, inv. {n}.",
    "D'après l'original, cliché de l'auteur.",
    "Coll. de l'auteur.",
    "Reproduction autorisée.",
]
LOREM = (
    "les formes que nous avons décrites plus haut ne se laissent pas réduire à une seule "
    "manière ; elles tiennent ensemble par le jeu des proportions et par la place que "
    "l'artiste leur assigne dans le champ. On remarquera que la lumière vient de la gauche, "
    "comme il est d'usage, et que le regard est conduit vers le centre par une suite de "
    "plans qui se recouvrent. Cette disposition n'est pas propre à l'atelier : elle se "
    "retrouve dans les recueils gravés du temps, où elle prend valeur de convention. "
)


# --------------------------------------------------------------------------- helpers

def _rgb(im: Image.Image) -> Image.Image:
    return im if im.mode == "RGB" else im.convert("RGB")


def _cap(im: Image.Image) -> Image.Image:
    if max(im.size) > MAX:
        im = im.copy()
        im.thumbnail((MAX, MAX), Image.LANCZOS)
    return im


def _fit(im: Image.Image, box: tuple[int, int]) -> Image.Image:
    im = _rgb(im).copy()
    scale = min(box[0] / im.width, box[1] / im.height)
    return im.resize((max(1, round(im.width * scale)), max(1, round(im.height * scale))),
                     Image.LANCZOS)


def _noise(size: tuple[int, int], rng: random.Random, amp: float, blur: float = 0.0) -> np.ndarray:
    from scipy.ndimage import gaussian_filter

    gen = np.random.default_rng(rng.randrange(2**32))
    n = gen.normal(0, 1, (size[1], size[0])).astype(np.float32)
    if blur:
        n = gaussian_filter(n, blur)  # in float: blurring 8-bit noise left hard-edged plateaus
        n = (n - n.mean()) / (n.std() + 1e-6)
    return n * amp


def _paper(size: tuple[int, int], rng: random.Random, tone=(236, 228, 210)) -> Image.Image:
    base = np.ones((size[1], size[0], 3), np.float32) * np.array(tone, np.float32)
    base += _noise(size, rng, 4.0)[..., None]
    base += _noise(size, rng, 3.0, blur=40)[..., None]
    return Image.fromarray(np.clip(base, 0, 255).astype(np.uint8))


def _perspective_coeffs(src, dst):
    """Coefficients for Image.transform(PERSPECTIVE) mapping output dst quad to input src."""
    a = []
    b = []
    for (x, y), (u, v) in zip(dst, src):
        a.append([x, y, 1, 0, 0, 0, -u * x, -u * y])
        a.append([0, 0, 0, x, y, 1, -v * x, -v * y])
        b += [u, v]
    return np.linalg.solve(np.array(a, float), np.array(b, float)).tolist()


def _warp_onto(bg: Image.Image, fg: Image.Image, quad) -> Image.Image:
    """Paste fg onto bg so that fg's corners land on quad (tl, tr, br, bl)."""
    w, h = fg.size
    src = [(0, 0), (w, 0), (w, h), (0, h)]
    coeffs = _perspective_coeffs(src, quad)
    warped = fg.transform(bg.size, Image.PERSPECTIVE, coeffs, Image.BICUBIC)
    mask = Image.new("L", fg.size, 255).transform(bg.size, Image.PERSPECTIVE, coeffs,
                                                   Image.BICUBIC)
    out = bg.copy()
    out.paste(warped, (0, 0), mask)
    return out


def _jitter_quad(rng: random.Random, x0, y0, x1, y1, amount: float):
    w, h = x1 - x0, y1 - y0
    j = lambda s: rng.uniform(-amount, amount) * s  # noqa: E731
    return [(x0 + j(w), y0 + j(h)), (x1 + j(w), y0 + j(h)), (x1 + j(w), y1 + j(h)),
            (x0 + j(w), y1 + j(h))]


def _font(path: str, size: int):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


# --------------------------------------------------------------------------- controls

def shrink_neutral(im: Image.Image, rng: random.Random, scale: float = 0.62) -> Image.Image:
    """Control: the image made as small in its canvas as a framed or paged one, on flat grey,
    with no frame. Separates 'the frame' from 'the work became smaller'."""
    im = _cap(_rgb(im))
    W, H = im.size
    fg = _fit(im, (round(W * scale), round(H * scale)))
    out = Image.new("RGB", (W, H), (128, 128, 128))
    out.paste(fg, ((W - fg.width) // 2, (H - fg.height) // 2))
    return out


def jpeg_resample(im: Image.Image, rng: random.Random) -> Image.Image:
    """Control: the pixel-level damage of a pass through a camera or a screen (down-up
    sampling, JPEG at q=60) with no frame at all."""
    import io

    im = _cap(_rgb(im))
    small = im.resize((im.width // 2, im.height // 2), Image.BILINEAR).resize(im.size,
                                                                               Image.BILINEAR)
    buf = io.BytesIO()
    small.save(buf, "JPEG", quality=60)
    return Image.open(io.BytesIO(buf.getvalue())).convert("RGB")


# --------------------------------------------------------------------------- frames

def gilt_frame(im: Image.Image, rng: random.Random) -> Image.Image:
    """A gilt moulding: bevelled gold profile, darker sight edge, worn texture."""
    im = _cap(_rgb(im))
    fw = max(24, round(min(im.size) * rng.uniform(0.09, 0.14)))
    inner = _fit(im, (MAX - 2 * fw, MAX - 2 * fw)) if max(im.size) + 2 * fw > MAX else im
    W, H = inner.width + 2 * fw, inner.height + 2 * fw
    # profile across the moulding: 0 at outer edge, 1 at sight edge
    t = np.linspace(0, 1, fw, dtype=np.float32)
    profile = (0.55 + 0.35 * np.sin(t * np.pi * 2.6 + 0.4) + 0.25 * np.cos(t * np.pi * 7)
               - 0.35 * (t > 0.86))
    gold = np.array([196, 154, 72], np.float32)
    canvas = np.zeros((H, W, 3), np.float32)
    yy, xx = np.mgrid[0:H, 0:W]
    d = np.minimum.reduce([xx, yy, W - 1 - xx, H - 1 - yy]).clip(0, fw - 1)
    shade = profile[d]
    # light from top-left: top and left bands brighter
    side_light = np.where((yy <= xx) & (yy <= H - 1 - xx), 1.12,
                          np.where((xx < yy) & (xx < H - 1 - yy), 1.05, 0.85))
    canvas = gold[None, None] * (shade * side_light)[..., None]
    canvas += _noise((W, H), rng, 10.0, blur=1.5)[..., None]
    canvas += _noise((W, H), rng, 14.0, blur=6)[..., None] * np.array([1, 0.9, 0.5])
    out = Image.fromarray(np.clip(canvas, 0, 255).astype(np.uint8))
    out.paste(inner, (fw, fw))
    # sight-edge shadow cast by the moulding onto the picture
    shadow = Image.new("L", (W, H), 0)
    ImageDraw.Draw(shadow).rectangle([fw, fw, fw + inner.width, fw + 6], fill=90)
    ImageDraw.Draw(shadow).rectangle([fw, fw, fw + 6, fw + inner.height], fill=90)
    shadow = shadow.filter(ImageFilter.GaussianBlur(3))
    out = Image.composite(Image.new("RGB", (W, H), (20, 14, 6)), out, shadow)
    return _cap(out)


def mat_border(im: Image.Image, rng: random.Random) -> Image.Image:
    """A cream passe-partout with a bevelled window, as for a drawing or print."""
    im = _cap(_rgb(im))
    m = round(min(im.size) * rng.uniform(0.16, 0.24))
    inner = _fit(im, (MAX - 2 * m, MAX - 2 * m)) if max(im.size) + 2 * m > MAX else im
    W, H = inner.width + 2 * m, inner.height + 2 * m
    out = _paper((W, H), rng, tone=(240, 236, 224))
    d = ImageDraw.Draw(out)
    d.rectangle([m - 5, m - 5, m + inner.width + 4, m + inner.height + 4], outline=(250, 248,
                                                                                    240), width=5)
    out.paste(inner, (m, m))
    return _cap(out)


# --------------------------------------------------------------------------- places

def museum_wall(im: Image.Image, rng: random.Random) -> Image.Image:
    """The object hung (or placed) in a gallery: coloured wall, floor, light falloff, a label,
    photographed slightly off-axis."""
    im = _cap(_rgb(im))
    W, H = 960, 720
    wall = rng.choice([(150, 40, 44), (52, 70, 92), (226, 222, 214), (96, 112, 84)])
    bg = np.ones((H, W, 3), np.float32) * np.array(wall, np.float32)
    yy, xx = np.mgrid[0:H, 0:W]
    light = 1.15 - 0.45 * (((xx - W / 2) / W) ** 2 + ((yy - H * 0.35) / H) ** 2)
    bg *= light[..., None]
    floor_y = round(H * 0.84)
    bg[floor_y:] = np.array([96, 74, 52], np.float32) * (0.8 + 0.2 * (yy[floor_y:] - floor_y)
                                                         / (H - floor_y))[..., None]
    bg += _noise((W, H), rng, 3.0)[..., None]
    out = Image.fromarray(np.clip(bg, 0, 255).astype(np.uint8))
    fg = _fit(im, (round(W * rng.uniform(0.34, 0.46)), round(H * 0.56)))
    x = (W - fg.width) // 2 + rng.randint(-60, 20)
    y = round(H * 0.42) - fg.height // 2
    sh = Image.new("L", (W, H), 0)
    ImageDraw.Draw(sh).rectangle([x + 8, y + 10, x + fg.width + 8, y + fg.height + 10], fill=110)
    out = Image.composite(Image.new("RGB", (W, H), (10, 10, 10)), out,
                          sh.filter(ImageFilter.GaussianBlur(9)))
    quad = _jitter_quad(rng, x, y, x + fg.width, y + fg.height, 0.02)
    out = _warp_onto(out, fg, quad)
    # wall label to the right
    d = ImageDraw.Draw(out)
    lx, ly = min(W - 90, x + fg.width + 40), round(H * 0.5)
    d.rectangle([lx, ly, lx + 62, ly + 40], fill=(244, 242, 236))
    for k in range(4):
        d.line([lx + 6, ly + 8 + 8 * k, lx + 6 + rng.randint(30, 50), ly + 8 + 8 * k],
               fill=(70, 70, 70), width=2)
    return out


def book_page(im: Image.Image, rng: random.Random, caption: str | None = None) -> Image.Image:
    """A plate in a printed book: paper, margins, plate number, a caption that does not name
    the subject, a running head and a folio."""
    im = _cap(_rgb(im))
    W, H = 680, 960
    page = _paper((W, H), rng)
    d = ImageDraw.Draw(page)
    margin_x, top = 78, 110
    fg = _fit(im, (W - 2 * margin_x, round(H * 0.58)))
    x = (W - fg.width) // 2
    page.paste(fg, (x, top))
    d.rectangle([x - 1, top - 1, x + fg.width, top + fg.height], outline=(60, 55, 50), width=1)
    n = rng.randint(3, 180)
    head = _font(SERIF_IT, 17)
    d.text((W // 2, 52), "HISTOIRE DE L'ART", fill=(60, 55, 50), font=_font(SERIF, 15),
           anchor="mm")
    cap = caption or rng.choice(NEUTRAL_CAPTIONS).format(n=rng.randint(100, 9999))
    y = top + fg.height + 30
    d.text((W // 2, y), f"Fig. {n}. — {cap}", fill=(40, 36, 32), font=head, anchor="mm")
    body = _font(SERIF, 17)
    words, line, y = LOREM.split(), "", y + 46
    for w in words:
        if d.textlength(line + " " + w, font=body) > W - 2 * margin_x:
            if y > H - 90:
                break
            d.text((margin_x, y), line.strip(), fill=(35, 32, 30), font=body)
            line, y = w, y + 24
        else:
            line += " " + w
    d.text((W // 2, H - 48), str(rng.randint(10, 400)), fill=(60, 55, 50), font=body,
           anchor="mm")
    return page


def book_photo(im: Image.Image, rng: random.Random) -> Image.Image:
    """The page photographed lying in an open book on a table: second page of text, gutter
    shadow, page curl, wood, perspective."""
    page = _rgb(im) if im.height > im.width else book_page(im, rng)
    page = _fit(page, (420, 600))
    W, H = 960, 720
    wood = np.ones((H, W, 3), np.float32) * np.array([120, 82, 52], np.float32)
    grain = np.sin(np.linspace(0, 60, W)[None, :] + _noise((W, H), rng, 1.5, blur=30))
    wood += (grain * 12)[..., None] + _noise((W, H), rng, 6, blur=2)[..., None]
    bg = Image.fromarray(np.clip(wood, 0, 255).astype(np.uint8))
    left = _paper(page.size, rng)
    d = ImageDraw.Draw(left)
    body, y = _font(SERIF, 12), 50
    for k in range(32):
        d.line([40, y, page.width - 40 - (rng.randint(0, 120) if k % 7 == 6 else 0), y],
               fill=(110, 104, 98), width=4)
        y += 16
    spread = Image.new("RGB", (page.width * 2, page.height))
    spread.paste(left, (0, 0))
    spread.paste(page, (page.width, 0))
    arr = np.asarray(spread, np.float32)
    xs = np.arange(spread.width, dtype=np.float32)
    gutter = 1 - 0.55 * np.exp(-((xs - page.width) / 28) ** 2)
    edge = 1 - 0.15 * (np.abs(xs - page.width) / page.width) ** 2
    arr = arr * (gutter * edge)[None, :, None]
    spread = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    sw, sh = spread.size
    x0, y0 = (W - sw) // 2, (H - sh) // 2 + 10
    quad = _jitter_quad(rng, x0, y0, x0 + sw, y0 + sh, 0.04)
    shadow = Image.new("L", (W, H), 0)
    ImageDraw.Draw(shadow).polygon([(px + 10, py + 14) for px, py in quad], fill=140)
    bg = Image.composite(Image.new("RGB", (W, H), (20, 12, 6)), bg,
                         shadow.filter(ImageFilter.GaussianBlur(12)))
    out = _warp_onto(bg, spread, quad)
    return out.filter(ImageFilter.GaussianBlur(0.6))


def screenshot_ui(im: Image.Image, rng: random.Random) -> Image.Image:
    """The image shown in a web page of an online collection: browser chrome, address bar,
    a header, thumbnails, metadata lines. No real brand or institution."""
    im = _cap(_rgb(im))
    W, H = 960, 640
    dark = rng.random() < 0.3
    page_bg = (28, 28, 30) if dark else (250, 250, 250)
    ink = (210, 210, 210) if dark else (40, 40, 40)
    out = Image.new("RGB", (W, H), page_bg)
    d = ImageDraw.Draw(out)
    d.rectangle([0, 0, W, 34], fill=(222, 224, 228))
    for k, c in enumerate([(236, 95, 87), (245, 190, 79), (98, 197, 84)]):
        d.ellipse([12 + 18 * k, 12, 24 + 18 * k, 24], fill=c)
    d.rounded_rectangle([90, 6, 300, 30], 6, fill=(250, 250, 250))
    d.text((100, 12), "Collection en ligne", fill=(60, 60, 60), font=_font(SANS, 12))
    d.rectangle([0, 34, W, 70], fill=(240, 241, 244))
    d.rounded_rectangle([60, 41, W - 60, 63], 10, fill=(255, 255, 255))
    d.text((76, 46), f"https://collection.example.org/objet/{rng.randint(10000, 99999)}",
           fill=(90, 90, 90), font=_font(SANS, 12))
    d.text((40, 88), "Collections  ·  Rechercher  ·  Visiter", fill=ink, font=_font(SANS, 15))
    fg = _fit(im, (560, 470))
    out.paste(fg, (40 + (560 - fg.width) // 2, 130 + (470 - fg.height) // 2))
    for k in range(9):
        d.line([640, 150 + 26 * k, 640 + rng.randint(120, 270), 150 + 26 * k], fill=ink,
               width=6 if k == 0 else 3)
    for k in range(4):
        th = _fit(im, (52, 52))
        out.paste(th, (640 + 62 * k, 420))
    return out


def screen_photo(im: Image.Image, rng: random.Random) -> Image.Image:
    """The image (or page) on a monitor photographed in a room: bezel, glare, moiré, tilt."""
    im = _cap(_rgb(im))
    W, H = 960, 720
    room = np.ones((H, W, 3), np.float32) * np.array([70, 66, 60], np.float32)
    room += _noise((W, H), rng, 25, blur=40)[..., None]
    bg = Image.fromarray(np.clip(room, 0, 255).astype(np.uint8))
    sw, sh = 720, 450
    screen = _fit(im, (sw, sh))
    disp = Image.new("RGB", (sw, sh), (8, 8, 8))
    disp.paste(screen, ((sw - screen.width) // 2, (sh - screen.height) // 2))
    arr = np.asarray(disp, np.float32)
    yy, xx = np.mgrid[0:sh, 0:sw]
    f = rng.uniform(0.9, 1.3)
    moire = 1 + 0.07 * np.sin(xx * f + yy * 0.17 * f) * np.sin(yy * 1.07 * f)
    glare = 38 * np.exp(-(((xx - sw * 0.7) / (sw * 0.25)) ** 2 + ((yy - sh * 0.25) / (sh * 0.3))
                          ** 2))
    arr = arr * moire[..., None] * 0.92 + glare[..., None] + 6
    disp = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    bez = 18
    monitor = Image.new("RGB", (sw + 2 * bez, sh + 2 * bez + 8), (24, 24, 26))
    monitor.paste(disp, (bez, bez))
    mw, mh = monitor.size
    x0, y0 = (W - mw) // 2, (H - mh) // 2 - 20
    # stand
    ImageDraw.Draw(bg).rectangle([W // 2 - 30, y0 + mh - 10, W // 2 + 30, y0 + mh + 70],
                                 fill=(30, 30, 32))
    quad = _jitter_quad(rng, x0, y0, x0 + mw, y0 + mh, 0.035)
    out = _warp_onto(bg, monitor, quad)
    return out.filter(ImageFilter.GaussianBlur(0.8))


def halftone_print(im: Image.Image, rng: random.Random) -> Image.Image:
    """Offset reproduction: CMY halftone screens at classic angles on off-white paper."""
    im = _cap(_rgb(im))
    W, H = im.size
    arr = np.asarray(im, np.float32) / 255
    cmy = 1 - arr
    cell = rng.choice([4, 5, 6])
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    out = np.ones_like(arr)
    for ch, angle in zip(range(3), (15, 75, 0)):
        a = np.deg2rad(angle)
        u = (xx * np.cos(a) + yy * np.sin(a)) / cell
        v = (-xx * np.sin(a) + yy * np.cos(a)) / cell
        du, dv = u - np.round(u), v - np.round(v)
        dist = np.sqrt(du ** 2 + dv ** 2)
        coverage = Image.fromarray((cmy[..., ch] * 255).astype(np.uint8)).filter(
            ImageFilter.BoxBlur(cell / 2))
        r = np.sqrt(np.asarray(coverage, np.float32) / 255 / np.pi) * 1.1
        dots = (dist < r).astype(np.float32)
        out[..., ch] -= dots * 0.92
    paper = np.array([246, 242, 232], np.float32) / 255
    out = np.clip(out, 0, 1) * paper
    return Image.fromarray((out * 255).astype(np.uint8))


def rephotograph(im: Image.Image, rng: random.Random) -> Image.Image:
    """A casual photograph of a flat print lying on a surface: tilt, warm or cool cast,
    vignette, slight blur, phone JPEG."""
    import io

    im = _cap(_rgb(im))
    W, H = 960, 720
    surface = rng.choice([(200, 196, 188), (60, 58, 56), (150, 120, 90)])
    bg = Image.fromarray(np.clip(np.ones((H, W, 3), np.float32) * np.array(surface)
                                 + _noise((W, H), rng, 8, blur=6)[..., None], 0, 255)
                         .astype(np.uint8))
    fg = _fit(im, (round(W * 0.78), round(H * 0.82)))
    x0, y0 = (W - fg.width) // 2, (H - fg.height) // 2
    quad = _jitter_quad(rng, x0, y0, x0 + fg.width, y0 + fg.height, 0.05)
    out = _warp_onto(bg, fg, quad)
    arr = np.asarray(out, np.float32)
    cast = np.array(rng.choice([(1.06, 1.0, 0.88), (0.92, 0.98, 1.08), (1.0, 1.0, 1.0)]))
    yy, xx = np.mgrid[0:H, 0:W]
    vig = 1 - 0.35 * (((xx - W / 2) / W) ** 2 + ((yy - H / 2) / H) ** 2) * 2
    arr = arr * cast * vig[..., None]
    out = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).filter(
        ImageFilter.GaussianBlur(1.0))
    buf = io.BytesIO()
    out.save(buf, "JPEG", quality=70)
    return Image.open(io.BytesIO(buf.getvalue())).convert("RGB")


LAYERS: dict[str, Callable[[Image.Image, random.Random], Image.Image]] = {
    "gilt_frame": gilt_frame,
    "mat_border": mat_border,
    "museum_wall": museum_wall,
    "book_page": book_page,
    "book_photo": book_photo,
    "screenshot_ui": screenshot_ui,
    "screen_photo": screen_photo,
    "halftone_print": halftone_print,
    "rephotograph": rephotograph,
    "shrink_neutral": shrink_neutral,
    "jpeg_resample": jpeg_resample,
}


def apply_chain(im: Image.Image, chain: list[str], seed: int) -> list[Image.Image]:
    """All the stages of a chain, starting with the given image (stage 0)."""
    rng = random.Random(seed)
    stages = [_cap(_rgb(im))]
    for name in chain:
        stages.append(LAYERS[name](stages[-1], rng))
    return stages


def content_mask(size: tuple[int, int], chain: list[str], seed: int) -> list[np.ndarray]:
    """Where the original work's pixels end up at each stage of a chain.

    The chain is run twice with the same seed, on an all-white and an all-black image of the
    original's size; the layers draw their randomness independently of the image content, so
    the two runs differ only where the work itself is shown. Returns one boolean mask per stage.
    """
    white = apply_chain(Image.new("RGB", size, (255, 255, 255)), chain, seed)
    black = apply_chain(Image.new("RGB", size, (0, 0, 0)), chain, seed)
    return [np.abs(np.asarray(w, np.int16) - np.asarray(b, np.int16)).mean(2) > 60
            for w, b in zip(white, black)]


def area_matched(im: Image.Image, stage_size: tuple[int, int], area_fraction: float,
                 grey: int = 128) -> Image.Image:
    """Control for any stage: the work alone, scaled so that it covers the same share of a
    canvas of the stage's size, centred on flat grey. Same size, no frame, no support."""
    im = _cap(_rgb(im))
    W, H = stage_size
    target = max(area_fraction, 1e-4) * W * H
    scale = min((target / (im.width * im.height)) ** 0.5, W / im.width, H / im.height)
    fg = im.resize((max(1, round(im.width * scale)), max(1, round(im.height * scale))),
                   Image.LANCZOS)
    out = Image.new("RGB", (W, H), (grey, grey, grey))
    out.paste(fg, ((W - fg.width) // 2, (H - fg.height) // 2))
    return out


# --------------------------------------------------------------------------- E4b: the screen

INKS = {  # process inks on paper, as RGB reflectance multipliers
    "c": np.array([0.0, 0.68, 0.94]), "m": np.array([0.93, 0.0, 0.55]),
    "y": np.array([1.0, 0.95, 0.0]), "k": np.array([0.08, 0.08, 0.08]),
}


def halftone_cmyk(im: Image.Image, rng: random.Random, cell: float = 5.0) -> Image.Image:
    """A proper four-colour screen: grey-component replacement into black, classic screen
    angles, neutral paper, inks multiplied. Unlike ``halftone_print`` (CMY only, which leaves a
    strong violet/yellow cast), the average colour stays close to the original."""
    im = _cap(_rgb(im))
    W, H = im.size
    rgb = np.asarray(im, np.float32) / 255
    k = 1 - rgb.max(2)
    cmy = (1 - rgb - k[..., None]) / (1 - k[..., None] + 1e-6)
    planes = {"c": cmy[..., 0], "m": cmy[..., 1], "y": cmy[..., 2], "k": k}
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    paper = np.array([0.97, 0.96, 0.93], np.float32)
    out = np.ones((H, W, 3), np.float32) * paper
    for name, angle in zip("cmyk", (15, 75, 0, 45)):
        a = np.deg2rad(angle)
        u = (xx * np.cos(a) + yy * np.sin(a)) / cell
        v = (-xx * np.sin(a) + yy * np.cos(a)) / cell
        dist = np.sqrt((u - np.round(u)) ** 2 + (v - np.round(v)) ** 2)
        cov = np.asarray(Image.fromarray((np.clip(planes[name], 0, 1) * 255).astype(np.uint8))
                         .filter(ImageFilter.BoxBlur(max(1, cell / 2))), np.float32) / 255
        dots = dist < np.sqrt(cov / np.pi)
        out = np.where(dots[..., None], out * INKS[name], out)
    return Image.fromarray((np.clip(out, 0, 1) * 255).astype(np.uint8))


def colour_only(layer: Callable, cell: float = 5.0) -> Callable:
    """The average colour a screen produces, without its dots: the screened image blurred at
    the scale of one cell. Separates 'the colour shifted' from 'the surface became dots'."""
    def apply(im: Image.Image, rng: random.Random) -> Image.Image:
        screened = layer(im, rng)
        return screened.filter(ImageFilter.GaussianBlur(cell * 0.9))
    return apply


LAYERS.update({
    "cmyk_fine": lambda im, rng: halftone_cmyk(im, rng, 3.0),
    "cmyk_medium": lambda im, rng: halftone_cmyk(im, rng, 5.0),
    "cmyk_coarse": lambda im, rng: halftone_cmyk(im, rng, 8.0),
    "cmy_colour_only": colour_only(halftone_print, 5.0),
})


# --------------------------------------------------------------------------- E10b controls

def degraded_matched(stage: Image.Image, mask: np.ndarray, grey: int = 128) -> Image.Image:
    """Control 'same degradation': the stage itself, with every pixel that is not the work's
    replaced by flat grey. Same area, same position, same resampling, blur, perspective and
    moiré as in the chain — only the supports are gone."""
    arr = np.asarray(_rgb(stage), np.uint8).copy()
    arr[~mask] = grey
    return Image.fromarray(arr)


def clutter_matched(im: Image.Image, stage_size: tuple[int, int], area_fraction: float,
                    background: Image.Image) -> Image.Image:
    """Control 'clutter': the work at the same area, pasted with no frame onto a busy picture
    that is not a support (another artwork filling the canvas). Separates 'a support surrounds
    the work' from 'something surrounds the work'."""
    W, H = stage_size
    bg = _rgb(background).copy()
    # keep only the central 60 %: museum images of paintings often show their own frame or
    # mount, and the background must not itself be a support
    bw, bh = bg.size
    bg = bg.crop((round(bw * 0.2), round(bh * 0.2), round(bw * 0.8), round(bh * 0.8)))
    scale = max(W / bg.width, H / bg.height)
    bg = bg.resize((round(bg.width * scale) + 1, round(bg.height * scale) + 1), Image.LANCZOS)
    bg = bg.crop(((bg.width - W) // 2, (bg.height - H) // 2, (bg.width - W) // 2 + W,
                  (bg.height - H) // 2 + H))
    fg = area_matched(im, stage_size, area_fraction)
    out = bg.copy()
    arr_fg = np.asarray(fg)
    inside = (arr_fg != 128).any(2)
    ys, xs = np.where(inside)
    if len(xs):
        box = (xs.min(), ys.min(), xs.max() + 1, ys.max() + 1)
        out.paste(fg.crop(box), box[:2])
    return out


def blur_only(cell: float = 5.0) -> Callable:
    """Control for the 'colour only' screen variant, which is a blur at the scale of one
    cell: the same blur on the original, without any colour change (review I3)."""
    def apply(im: Image.Image, rng: random.Random) -> Image.Image:
        return _cap(_rgb(im)).filter(ImageFilter.GaussianBlur(cell * 0.9))
    return apply


LAYERS["blur_only"] = blur_only(5.0)
