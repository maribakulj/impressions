#!/usr/bin/env python3
"""E6 — encode the 171 real reproductions with the three models."""

import json

from impressions import CACHE
import numpy as np
from PIL import Image

from impressions.encoders import Encoder

rows = [json.loads(l) for l in open("data/real/manifest.jsonl")]
for m in ["clip", "siglip", "dinov2"]:
    enc = Encoder(m)
    vecs = enc.images(Image.open(f"data/real/images/{r['file']}") for r in rows)
    np.savez(f"{CACHE}/real-{m}.npz", files=np.array([r["file"] for r in rows]), vecs=vecs)
    print(m, vecs.shape)
