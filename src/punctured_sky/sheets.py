"""Contact sheets: a grid of thumbnails with a caption, to look before measuring."""

from __future__ import annotations

from PIL import Image, ImageDraw, ImageFont


def contact_sheet(items: list[tuple[Image.Image, str]], cols: int = 5, cell: int = 260,
                  caption_h: int = 34) -> Image.Image:
    rows = (len(items) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * cell, rows * (cell + caption_h)), "white")
    draw = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 13)
    except OSError:
        font = ImageFont.load_default()
    for i, (im, text) in enumerate(items):
        r, c = divmod(i, cols)
        thumb = im.convert("RGB").copy()
        thumb.thumbnail((cell - 8, cell - 8))
        x = c * cell + (cell - thumb.width) // 2
        y = r * (cell + caption_h) + (cell - thumb.height) // 2
        sheet.paste(thumb, (x, y))
        for k, line in enumerate(text.split("\n")[:2]):
            draw.text((c * cell + 4, r * (cell + caption_h) + cell + 2 + 15 * k), line[:38],
                      fill="black", font=font)
    return sheet
