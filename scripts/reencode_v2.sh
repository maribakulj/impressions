#!/bin/sh
# Review I4: re-encode everything with images completed to a square (no centre crop).
set -e
cd "$(dirname "$0")/.."
for m in clip siglip dinov2; do uv run python scripts/embed_pool.py $m; done
uv run python scripts/e6_embed.py
uv run python scripts/e4b_embed_screens.py
uv run python scripts/e4_embed_stages.py
echo REENCODE_DONE
