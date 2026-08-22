# Atlas data

This directory is generated from the master SVG by `tools/export_concepts.py`.

- `atlas.json` — complete dataset with all 83 concept records.
- `concepts.ndjson` — one JSON object per concept, suitable for streaming, embeddings, RAG and token-oriented pipelines.
- `token_corpus.md` — deterministic human/model-readable text projection of the atlas.
- `schema.json` — schema for a concept record.

Do not hand-edit generated files. Change the SVG/generator or exporter, then regenerate and validate.


## Corpus / abjad additions

- `abjad_field.json` — direct 28-letter classical mapping and normalization contract.
- `quran_abjad_hypothesis.json` — empirical metric definition and candidate fraction, separate from the theorem layer.
- `quran_abjad_measurement.json` — measured result when a locked fixture exists; otherwise explicit `fixture_missing`.

The large corpus itself lives behind the explicit boundary in `../corpora/quran_uthmani/`.
