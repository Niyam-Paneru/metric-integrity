# Verification

Exact maintainer-facing checks live here rather than in the reviewer-facing README.

## Local checks

```bash
python -m pytest
PYTHONPATH=src python -m metric_integrity.demo
python -m compileall -q src
```

Expected evidence:

- the pytest suite completes with no failures;
- the demo prints the measured booking-intent rate, the measured all-calls rate, the modelled booked-call value, and the unavailable attribution figure with their lineage;
- source compilation exits successfully.

## CI

CircleCI repeats source compilation, the pytest suite, and the demo, then checks that the public proof/supporting files are present.
