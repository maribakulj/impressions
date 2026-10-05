# impressions

**Nested frames and what they do to a machine's reading of an image.**

A gilt frame, a book page, a photographed book, a screen, a halftone print: images reach us
wrapped in supports that nest like Russian dolls. This project tests whether each wrapping changes
what a computer-vision model takes the image to *be* — and at which layer the support starts to
outweigh the object. Computer vision usually treats a change of support as noise to be made
invariant ("domain shift"); the hypothesis here is that the frame carries part of the meaning.

The name comes from Raymond Roussel's *Nouvelles Impressions d'Afrique*, a poem built from
parentheses nested up to five deep.

*Status: results in, article being written and reviewed; driven by an autonomous research loop. The plan, hypotheses and
refutation criteria are in [`PLAN.md`](PLAN.md); the running log is in [`JOURNAL.md`](JOURNAL.md)
(both in French).*

## Findings so far

*(Full account, in French, in [`article/article.md`](article/article.md) and
[`JOURNAL.md`](JOURNAL.md).)*

1. **Museums already deliver nested images.** Of 300 museum images, only 48 show the work with
   nothing around it; prints and photographs come with their sheet, mount and inscriptions,
   paintings are cropped to the canvas. Object type is readable in the margins.
2. **The outermost frame decides; an inner gilt frame does nothing.** Retrieval and Claude's
   description are unchanged by a frame alone, on synthetic layers and on real close-up photos.
3. **As layers pile up, the support takes the place of the subject — and not because the work
   got small.** At six layers Claude describes the support in 27 of 30 cases; the same work
   alone at the same size, on grey: 0 of 30. On 171 real reproductions of 22 famous works, the
   same pattern holds at matched size, and Claude names the work but demotes it to a setting
   ("visitors crowd in a gallery in front of The Starry Night").
4. **The halftone screen works by impregnation, not envelopment.** Its dots (not its colour)
   make Claude lose the subject, and a coarse screen becomes the subject; DINOv2 reacts to the
   dots (texture), CLIP to the colour.
5. **The medium read follows the envelope** (on a wall → "a painting", in a book → "a print"),
   controlled for size. Expected; stated, not stressed.
6. On real images, for the embedding models, most of the loss is explained by the size of the
   work in the image; an effect of the layers themselves is not established (22 works).

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
