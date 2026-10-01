# Metric Integrity

A small Python example for keeping a metric's lineage attached to the number: the population it describes, the calculation that produced it, the evidence basis, and whether the result is safe to quote.

The failure this prevents is simple: correct arithmetic can still support the wrong business sentence. A measured number can use the wrong denominator, a modelled value can be formatted until it looks observed, and an attribution claim can be impossible because the data has no durable join.

![Metric lineage](docs/workflow.svg)

## One sample, four different claims

The demo uses **34 synthetic calls**: 14 express booking intent and 4 book. That produces two arithmetically valid rates, but only one answers the booking-intent success question.

```text
Booking rate vs calls expressing booking intent
  value: 28.6%
  population: calls expressing booking intent
  calculation: 4 / 14
  basis: measured
  quote: yes

Booking rate vs all calls
  value: 11.8%
  population: all calls
  calculation: 4 / 34
  basis: measured
  quote: no
  reason: denominator does not match the booking-intent success claim
```

The same run also keeps a **4,800** treatment-value calculation labelled `modelled`, while recovered revenue is `not available` because there is no durable attribution join. `unavailable` means the evidence needed for the claim does not exist; it is not a substitute for a low estimate.

## Where the behavior lives

| File | What to inspect |
|---|---|
| `src/metric_integrity/models.py` | `Figure`: value, population, calculation inputs, basis, and quote decision |
| `src/metric_integrity/rates.py` | named denominator populations and rate construction |
| `src/metric_integrity/valuation.py` | modelled value and explicit attribution refusal |
| `src/metric_integrity/report.py` | report composition and limitations |
| `src/metric_integrity/demo.py` | runnable lineage walkthrough |
| `tests/` | denominator, basis, quote-safety, attribution, and unavailable-state checks |

## Run it

```bash
python -m pytest
PYTHONPATH=src python -m metric_integrity.demo
python -m compileall -q src
```

CircleCI runs those checks plus proof-file existence checks from `.circleci/config.yml`.

## Evidence boundary

- The records are synthetic; these are not customer or revenue results.
- `measured` describes how a value was obtained. It does **not** automatically mean the value is safe to quote for every claim.
- `modelled` means an assumption participates in the calculation.
- `unavailable` means the required evidence is missing, such as a durable attribution join.

See [PROVENANCE.md](PROVENANCE.md) for the public/private boundary and [docs/invariants.md](docs/invariants.md) for the rules the tests protect.
