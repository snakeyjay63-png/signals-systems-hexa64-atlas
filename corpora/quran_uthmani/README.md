# Qur’an Uthmani corpus fixture

This directory is the explicit corpus boundary for Chapter 16.

The repository does **not** silently substitute a corpus. `source.json` records the public upstream source and expected 6236-ayah structure. Run:

```bash
python tools/fetch_quran_fixture.py
python tools/analyze_quran_abjad.py
```

The fetch step writes `quran.jsonl` and `fixture.lock.json`. The lock contains the SHA-256 of the exact downloaded bytes, line count, and source locator. Once those two files are committed, the empirical layer is fully offline-reproducible.

The current package intentionally leaves the large remote corpus unbundled because it could not be materialized in this build runtime; the field mathematics and normalization remain fully testable without it.
