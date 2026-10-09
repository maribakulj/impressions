#!/usr/bin/env python3
"""Social round (pilot) — the same five contents in five frames (none, thin modern black,
classical gilt, ebonized ripple, rococo giltwood) in four spaces (neutral grey, white gallery,
living room, kitchen): 100 images. Real frames and rooms come from Wikimedia Commons and the
Met (data/social/src/hi/sources.json); frames are fitted to each content by five-slice scaling
(corners and central ornaments kept, plain mouldings stretched), so no content is ever cropped.
Writes data/social/img/<content>__<frame>__<space>.jpg and data/social/items.json."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

SRC = Path("data/social/src/hi")
FR = Path("data/social/frames")
OUT = Path("data/social/img")
CAY = Path.home() / "caypollard"

CONTENTS = {
    "renoir": "Auguste Renoir, The Daughters of Catulle Mendès (1888), Met — painting",
    "mondrian": "Piet Mondrian, Composition (1921), Met — painting",
    "child": "a child's drawing of a yellow house, sun and rain",
    "beach": "an amateur photograph of a beach",
    "receipt": "a supermarket receipt",
}
FRAMES = ["none", "modern", "classic", "ebonized", "rococo"]
# five-slice: fraction of the frame's width/height around the centre kept unstretched
KEEP_MID = {"classic": (0.0, 0.0), "ebonized": (0.0, 0.0), "rococo": (0.26, 0.22)}
SPACES = ["grey", "gallery", "salon", "kitchen"]


def content(name: str) -> Image.Image:
    if name == "renoir":
        w = next(json.loads(l) for l in open("data/works.jsonl") if "Q728373" in l)
        return Image.open(CAY / w["image_path"]).convert("RGB")
    im = Image.open(SRC / f"{name}.jpg").convert("RGB")
    if name == "receipt":
        W, H = im.size
        im = im.crop((int(0.04 * W), int(0.16 * H), int(0.82 * W), int(0.93 * H)))
    return im


def axis_map(n_src: int, a: int, b: int, keep: float, n_dst: int) -> np.ndarray:
    """Source coordinate for each destination pixel along one axis: [0,a) and [b,n_src) kept,
    a central band of width keep*n_src kept, the two plain stretches between rescaled."""
    k = int(keep * n_src / 2)
    m0, m1 = n_src // 2 - k, n_src // 2 + k
    if k == 0:
        m0 = m1 = n_src // 2
    fixed = a + (n_src - b) + (m1 - m0)
    seg_src = [(a, max(a, m0)), (min(b, m1), b)]
    free = n_dst - fixed
    if free < 2:  # not enough room: fall back to uniform scaling
        return np.clip((np.arange(n_dst) * n_src / n_dst).astype(int), 0, n_src - 1)
    lens = [s1 - s0 for s0, s1 in seg_src]
    tot = max(1, sum(lens))
    dst = [round(free * l / tot) for l in lens]
    dst[1] = free - dst[0]
    parts = [np.arange(a)]
    parts.append(seg_src[0][0] + (np.arange(dst[0]) + 0.5) * lens[0] / max(1, dst[0]))
    parts.append(np.arange(m0, m1))
    parts.append(seg_src[1][0] + (np.arange(dst[1]) + 0.5) * lens[1] / max(1, dst[1]))
    parts.append(np.arange(b, n_src))
    return np.clip(np.concatenate(parts).astype(int), 0, n_src - 1)


def framed(im: Image.Image, frame: str, meta: dict) -> tuple[Image.Image, int]:
    """Content inside the frame, as RGBA (content never cropped), and the content's width in it."""
    if frame == "none":
        return im.convert("RGBA"), im.width
    if frame == "modern":
        t = max(6, int(0.022 * max(im.size)))
        out = Image.new("RGBA", (im.width + 2 * t, im.height + 2 * t), (22, 22, 24, 255))
        out.paste(im, (t, t))
        return out, im.width
    m = meta[f"frame_{frame}"]
    fr = np.asarray(Image.open(FR / m["file"]).convert("RGBA"))
    x0, y0, x1, y1 = m["opening"]
    ow, oh = x1 - x0, y1 - y0
    # target opening with the content's aspect and the same area as the frame's opening
    ar = im.width / im.height
    tw, th = int(round((ow * oh * ar) ** 0.5)), int(round((ow * oh / ar) ** 0.5))
    H, W = fr.shape[:2]
    kx, ky = KEEP_MID[frame]
    xs = axis_map(W, x0, x1, kx, tw + x0 + (W - x1))
    ys = axis_map(H, y0, y1, ky, th + y0 + (H - y1))
    out = Image.fromarray(fr[ys][:, xs])
    under = Image.new("RGBA", out.size, (0, 0, 0, 0))
    under.paste(im.resize((tw + 4, th + 4), Image.LANCZOS), (x0 - 2, y0 - 2))
    under.alpha_composite(out)
    return under, tw


def shadow_paste(bg: Image.Image, obj: Image.Image, cw: int, ar: float, cx: float, cy: float,
                 max_w: float, max_h: float) -> Image.Image:
    """The content (width cw in obj, aspect ar) gets the same size whatever the frame: it fits
    a box of max_w x max_h of the background; the frame extends around it."""
    W, H = bg.size
    s = min(max_w * W, max_h * H * ar) / cw
    obj = obj.resize((max(1, int(obj.width * s)), max(1, int(obj.height * s))), Image.LANCZOS)
    x, y = int(cx * W - obj.width / 2), int(cy * H - obj.height / 2)
    a = obj.split()[3]
    sh = Image.new("L", bg.size, 0)
    off = max(3, obj.height // 60)
    sh.paste(a, (x + off, y + 2 * off))
    sh = sh.filter(ImageFilter.GaussianBlur(max(2, obj.height // 45))).point(lambda v: int(v * 0.45))
    out = bg.convert("RGBA")
    out.alpha_composite(Image.merge("RGBA", (Image.new("L", bg.size, 0),) * 3 + (sh,)))
    out.alpha_composite(obj, (x, y))
    return out.convert("RGB")


def gallery() -> Image.Image:
    W, H = 1600, 1200
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    wall = 238 - 10 * ((xx - W / 2) / W) ** 2 * 4 - 8 * (yy / H)
    light = 6 * np.exp(-(((xx - W / 2) / (0.35 * W)) ** 2 + ((yy - 0.3 * H) / (0.35 * H)) ** 2))
    img = np.stack([wall + light, wall + light - 1, wall + light - 3], -1)
    floor = int(0.84 * H)
    img[floor:] = np.array([176, 170, 162]) - 18 * ((yy[floor:] - floor) / (H - floor))[..., None]
    img[floor - 4:floor] = [222, 222, 220]
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))


def place(obj: Image.Image, cw: int, ar: float, space: str) -> Image.Image:
    if space == "grey":
        bg = Image.new("RGB", (1600, 1200), (128, 128, 128))
        return shadow_paste(bg, obj, cw, ar, 0.5, 0.5, 0.40, 0.42)
    if space == "gallery":
        return shadow_paste(gallery(), obj, cw, ar, 0.5, 0.42, 0.26, 0.30)
    if space == "salon":
        bg = Image.open(SRC / "space_salon.jpg").convert("RGB")
        return shadow_paste(bg, obj, cw, ar, 0.43, 0.15, 0.20, 0.145)
    bg = Image.open(SRC / "space_kitchen.jpg").convert("RGB")
    bg = bg.crop((0, 0, bg.width, int(bg.height * 0.6)))
    return shadow_paste(bg, obj, cw, ar, 0.815, 0.42, 0.105, 0.23)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    meta = json.loads((FR / "frames.json").read_text())
    items = []
    for c in CONTENTS:
        im = content(c)
        im.thumbnail((1400, 1400))
        for f in FRAMES:
            obj, cw = framed(im, f, meta)
            for s in SPACES:
                name = f"{c}__{f}__{s}.jpg"
                out = place(obj, cw, im.width / im.height, s)
                out.thumbnail((1600, 1600))
                out.save(OUT / name, quality=90)
                items.append({"file": name, "content": c, "frame": f, "space": s})
    (Path("data/social") / "items.json").write_text(json.dumps(
        {"contents": CONTENTS, "frames": FRAMES, "spaces": SPACES, "items": items}, indent=1))
    print(len(items), "images")


if __name__ == "__main__":
    main()
