# punctured sky

**Nested frames and what they do to a machine's reading of an image.**

A gilt frame, a book page, a photographed book, a screen, a halftone print: images reach us
wrapped in supports that nest like Russian dolls. This project tests whether each wrapping changes
what a computer-vision model takes the image to *be* — and at which layer the support starts to
outweigh the object. Computer vision usually treats a change of support as noise to be made
invariant ("domain shift"); the hypothesis here is that the frame carries part of the meaning.

*Status: revised after two adversarial reviews; final encoder measures running. Driven by an autonomous research loop. The plan, hypotheses and
refutation criteria are in [`PLAN.md`](PLAN.md); the running log is in [`JOURNAL.md`](JOURNAL.md)
(both in French).*

## Findings so far

*(Full account, in French, in [`article/article.md`](article/article.md) and
[`JOURNAL.md`](JOURNAL.md). Revised twice after adversarial reviews: [`notes/relecture.md`](notes/relecture.md),
[`notes/relecture-2.md`](notes/relecture-2.md).)*

**The machine has no parergon.** Neither the embedding models (CLIP, SigLIP, DINOv2) nor the
describing model (Claude, read blind and judged by another model) treat a frame or a support as a
frame — something that isolates and designates the work.

1. **Museums already deliver nested images.** Of 300 museum images, only 48 show the work with
   nothing around it; prints and photographs come with their sheet, mount and inscriptions.
2. **A gilt frame changes nothing**, for retrieval or description.
3. **What demotes the work is salience, not the support.** In a photographed book or on a screen,
   the describing model still identifies the work's subject, but stops making it the subject of
   its sentence (0/30). The very same degraded pixels, at the same place, on grey: 30/30; on
   another painting, with no support at all: 0/30. A book without text: 6/30.
4. **On 131 real reproductions** of 22 famous works, demotion grows with the number of layers at
   equal area (mostly in gallery photographs), while the work's subject is identified ~100 % of the time.
5. **Encoders lose the work with any surrounding**, support or not; on real images each layer
   costs retrieval beyond area for all three models once images are no longer centre-cropped.
6. **The halftone screen** matters mainly through coarse dots; expected texture effects.

## What is here

- `src/punctured_sky/layers.py` — composable, deterministic layers: gilt frame, passe-partout,
  gallery wall, book page, photographed book, browser page, monitor photographed in a room,
  CMY halftone print, casual rephotograph; and two controls (same reduction on flat grey;
  resampling + JPEG with no frame).
- `src/punctured_sky/encoders.py` — CLIP ViT-B/32, SigLIP base, DINOv2 base (image-only, the
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
