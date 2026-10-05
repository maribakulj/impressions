# impressions

**Nested frames and what they do to a machine's reading of an image.**

A gilt frame, a book page, a photographed book, a screen, a halftone print: images reach us
wrapped in supports that nest like Russian dolls. This project tests whether each wrapping changes
what a computer-vision model takes the image to *be* — and at which layer the support starts to
outweigh the object. Computer vision usually treats a change of support as noise to be made
invariant ("domain shift"); the hypothesis here is that the frame carries part of the meaning.

The name comes from Raymond Roussel's *Nouvelles Impressions d'Afrique*, a poem built from
parentheses nested up to five deep.

*Status: work in progress, driven by an autonomous research loop. The plan, hypotheses and
refutation criteria are in [`PLAN.md`](PLAN.md); the running log is in [`JOURNAL.md`](JOURNAL.md)
(both in French).*

## What is here

- `src/impressions/layers.py` — composable, deterministic layers: gilt frame, passe-partout,
  gallery wall, book page, photographed book, browser page, monitor photographed in a room,
  CMY halftone print, casual rephotograph; and two controls (same reduction on flat grey;
  resampling + JPEG with no frame).
- `src/impressions/encoders.py` — CLIP ViT-B/32, SigLIP base, DINOv2 base (image-only, the
  control for caption-trained models).
- `data/works.jsonl` — 300 works (60 paintings, prints, drawings, sculptures, photographs) sampled
  from a museum pool built from Wikidata / Wikimedia Commons in the sibling project
  [caypollard](https://github.com/maribakulj/caypollard). Images are not redistributed here.
- `figures/` — contact sheets of the layers, looked at before any measurement.

## Running

```sh
uv sync --extra dev
uv run pytest
uv run python scripts/sheet_layers.py gilt_frame book_photo
```

The image paths resolve against a local caypollard checkout (`~/caypollard`).

## Licence

Code: MIT. Figures reproduce museum images from Wikimedia Commons, under the licences stated on
their Commons pages (mostly public domain).
