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
