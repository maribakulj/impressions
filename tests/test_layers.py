import random

import numpy as np
from PIL import Image

from impressions.layers import LAYERS, MAX, apply_chain


def _image(w=500, h=380):
    rng = np.random.default_rng(0)
    return Image.fromarray(rng.integers(0, 255, (h, w, 3), dtype=np.uint8))


def test_every_layer_returns_bounded_rgb():
    for name, fn in LAYERS.items():
        out = fn(_image(), random.Random(1))
        assert out.mode == "RGB", name
        assert max(out.size) <= MAX, name


def test_layers_are_deterministic():
    for name, fn in LAYERS.items():
        a = np.asarray(fn(_image(), random.Random(3)))
        b = np.asarray(fn(_image(), random.Random(3)))
        assert np.array_equal(a, b), name


def test_layers_compose_in_any_order():
    stages = apply_chain(_image(), ["gilt_frame", "museum_wall", "book_page", "book_photo",
                                    "screen_photo", "rephotograph"], seed=5)
    assert len(stages) == 7
    assert all(max(s.size) <= MAX for s in stages)


def test_frame_surrounds_the_picture():
    im = Image.new("RGB", (400, 300), (0, 200, 0))
    out = np.asarray(LAYERS["gilt_frame"](im, random.Random(0))).astype(int)
    h, w, _ = out.shape
    centre = out[h // 2, w // 2]
    corner = out[2, 2]
    assert centre[1] > 150 and centre[0] < 80  # the picture is still in the middle
    assert corner[0] > corner[2]  # gold, not green, at the edge


def test_content_mask_follows_the_work():
    from impressions.layers import content_mask

    masks = content_mask((400, 300), ["gilt_frame", "museum_wall", "book_page"], seed=2)
    fractions = [m.mean() for m in masks]
    assert fractions[0] > 0.99  # the bare image is all work
    assert fractions[1] < fractions[0] and fractions[3] < fractions[2]
    assert fractions[3] > 0.0


def test_area_matched_has_the_stage_size_and_area():
    from impressions.layers import area_matched

    out = area_matched(_image(), (960, 720), 0.05)
    assert out.size == (960, 720)
    covered = (np.asarray(out).astype(int) - 128).any(2).mean()
    assert 0.03 < covered < 0.07
