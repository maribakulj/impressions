# punctured sky

**Nested frames and what they do to a machine's reading of an image.**

A gilt frame, a book page, a photographed book, a screen, a halftone print: images reach us
wrapped in supports that nest like Russian dolls. Part of frame theory gives the frame the
function of isolating and designating the work; computer vision, when it aims at recognition,
treats a change of support as a shift to overcome. This project tests what each wrapping does to
what models retrieve and say about an image, against controls that keep the work's area fixed.

*Status (8 October 2026): measures complete; article written (in French) and revised after three
adversarial reviews, the last by Codex. The plan, hypotheses and refutation criteria are in
[`PLAN.md`](PLAN.md); the dated log is in [`JOURNAL.md`](JOURNAL.md) (both in French).*

## Findings

Full account, in French: [`article/article.md`](article/article.md) — *Ce qui entoure l'œuvre :
supports emboîtés et lecture automatique des reproductions*. Reviews and what was done about
them: [`notes/relecture.md`](notes/relecture.md), [`notes/relecture-2.md`](notes/relecture-2.md),
[`notes/relecture-codex.md`](notes/relecture-codex.md) (Codex's reports kept verbatim in
[`notes/codex/`](notes/codex/)).

**For these machines and these tasks, the support plays no role of its own: it is part of the
scene. What decides is the work's salience in the image.**

1. **Museums already deliver nested images.** Of 300 museum images, only 48 show the work with
   nothing around it; prints and photographs come with their sheet, mount and inscriptions.
2. **A gilt frame changes these measures little** (retrieval in the top ten 99–100 %; the work
   stays the subject of the description 30/30).
3. **Salience, not the support.** Asked only "what does this image show?", the describing model
   (Claude Sonnet, read blind, judged blind by Claude Opus) makes the work the main subject:

   | situation (30 works, same area) | main subject |
   |---|---|
   | same degraded pixels, same place, on grey | 30/30 |
   | framed, on a gallery wall | 30/30 |
   | centred on another painting | 14/30 |
   | photographed book without any text (exact same geometry) | 2/30 |
   | photographed book | 0/30 |
   | web page on a photographed screen | 0/30 |
   | same degraded pixels, same place, on another painting | 0/30 |

   The work is not lost: it becomes a complement, and its subject is identified 98–100 % of the
   time when asked. Readable text has no measurable effect.
4. **Encoders say the same in their own way.** In a photographed book the work is retrieved worse
   than the same pixels on grey, but better than when centred on another painting (top ten:
   CLIP 12 / 5 / 2 %, SigLIP 46 / 18 / 13 %, DINOv2 29 / 19 / 2 %). Any surrounding dilutes it.
5. **On 131 real reproductions** of 22 famous works, the work stops being the main subject as
   layers accumulate (75 % at two layers, 6 % at four and more), but once visible people are
   accounted for, the layer effect is no longer established; people weigh. Encoders lose the work
   with each layer beyond its area, for all three models.
6. **The halftone screen** matters mainly through coarse dots (an expected texture effect).

Not done: the human study (ready in [`human_study/`](human_study/), 72 images, needs participants).

## What is here

- `src/punctured_sky/` — the layers (`layers.py`: gilt frame, passe-partout, gallery wall, book
  page, photographed book, browser page, photographed screen, halftone, rephotograph, and the
  matched-area controls), chains, encoders (CLIP ViT-B/32, SigLIP base, DINOv2 base, images
  completed to a square), blind reading and judging with Claude (`blind.py`).
- `scripts/` — one script per experiment (E1–E10c); `Makefile` runs them.
- `data/works.jsonl` — the 300 works (60 paintings, prints, drawings, sculptures, photographs)
  sampled from a museum pool built from Wikidata / Wikimedia Commons in the sibling project
  [caypollard](https://github.com/maribakulj/caypollard). Images are not redistributed here.
- `data/annotations/` — every Claude reading and judgment (cached; reruns make no new calls).
- `data/real/` — manifest and annotations of the 171 real reproductions (images not redistributed).
- `results/` — every number in the article; `article/figures/` — the figures.
- `figures/` — contact sheets of the layers, looked at before any measurement.

## Running

```sh
uv sync --extra dev
uv run pytest
make analyses figures   # every number and figure from the cached readings, no model call
```

Encodings need a local caypollard checkout (`~/caypollard`) for the images; new readings need the
`claude` CLI.

## Licence

Code: MIT. Figures and the human-study images reproduce museum images from Wikimedia Commons, under
the licences stated on their Commons pages (mostly public domain).
