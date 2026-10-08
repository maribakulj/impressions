# Reproduce the measures. Encodings need the caypollard checkout (~/caypollard) for images;
# Claude readings need the `claude` CLI and are cached in data/annotations/ (rerun = no new calls).
PY = uv run python
HEAVY = ~/outils-seg/lourd.sh

.PHONY: all works layers pool stages screens real measures claude blind analyses figures test study

# `make analyses figures` recomputes every number and figure from the cached readings and
# encodings, without any model call.
all: measures blind analyses figures

works:            ## E1 — the 300 works
	$(PY) scripts/select_works.py
annotate:         ## E3 — layers already present in the museum images (Claude)
	$(PY) scripts/annotate_existing_layers.py
pool:             ## the 18 405-image search gallery, three encoders
	for m in clip siglip dinov2; do $(HEAVY) $(PY) scripts/embed_pool.py $$m; done
stages:           ## E4 — every stage of every chain, with its same-area control
	$(HEAVY) $(PY) scripts/e4_embed_stages.py
screens:          ## E4b — halftone variants
	$(HEAVY) $(PY) scripts/e4b_embed_screens.py
real:             ## E6 — the real reproductions (download + encode)
	$(PY) scripts/fetch_real_corpus.py
	$(PY) scripts/e6_embed.py
claude:           ## E3 pilot, E5, E4b, E6 readings and verdicts (cached)
	$(PY) scripts/pilot.py
	$(PY) scripts/e5_readings.py
	$(PY) scripts/e4b_claude.py
	$(PY) scripts/e6_readings.py
measures:         ## every number in the article
	taskpolicy -b $(PY) scripts/e4_measure.py
	$(PY) scripts/e4b_analyse.py
	$(PY) scripts/e5_analyse.py
	$(PY) scripts/e5_zeroshot.py
	$(PY) scripts/e6_analyse.py
figures:
	$(PY) scripts/fig_verdicts.py
	$(PY) scripts/fig_retrieval.py
	$(PY) scripts/fig_real.py
test:
	uv run pytest -q
blind:            ## E10b/E10c — blind readings (opaque names), Opus judgments, analysis
	PYTHONPATH=src $(PY) scripts/blind_readings.py 2
	PYTHONPATH=src $(PY) scripts/blind_judge_artwork.py
	PYTHONPATH=src $(PY) scripts/blind_round2.py
	PYTHONPATH=src $(PY) scripts/blind_round2_notext.py
analyses:         ## E10b/E10c — every number from the blind readings, no model call
	PYTHONPATH=src $(PY) scripts/blind_analyse.py
	PYTHONPATH=src $(PY) scripts/blind_round2_analyse.py
study:            ## E7 — the human study package
	$(PY) scripts/e7_build_study.py
