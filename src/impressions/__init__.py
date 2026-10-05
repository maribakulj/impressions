"""Nested frames and what they do to a machine's reading of an image."""

import os
from pathlib import Path

# Encodings live under data/cache/<version>. v1 = the first run (centre-cropped by CLIP and
# DINOv2); v2 = images completed to a square before encoding (review I4). Default: v2.
CACHE = Path("data/cache") / os.environ.get("IMPRESSIONS_CACHE", "v2")
