# Metric Integrity

A small Python example for keeping a metric's lineage attached to the number: the population it describes, the calculation that produced it, the evidence basis, and whether the result is safe to quote.

A percentage can be mathematically correct and still answer the wrong question. Decimal places are not a permission slip.

```mermaid
flowchart LR
    C[Claim to report] --> E{Evidence path}
    E -->|Observed records| P[Choose named population]
    P --> R[Compute value + lineage]
    R --> M[basis = measured]
    M --> Q{Population fits the claim?}
    Q -->|Yes| Y[quotable = true]
    Q -->|No| N[quotable = false]
    E -->|Configured assumption| V[Measured booked count × assumption]
    V --> O[basis = modelled]
    O --> X[quotable = false]
    E -->|Attributed value| J{Durable attribution join?}
    J -->|No| U[basis = unavailable<br/>value = None]
    J -.->|Yes| A[Attribution evidence path<br/>not implemented in this public slice]
```

## One sample, four different claims

The demo uses **34 synthetic calls**: 14 express booking intent and 4 book. The same records can support different arithmetic without supporting the same sentence.

| Figure | Value | Population / calculation | Basis | Safe to quote for this claim? |
|---|---:|---|---|---|
| Booking rate vs calls expressing booking intent | 28.6% | calls expressing booking intent; 4 / 14 | `measured` | Yes |
| Booking rate vs all calls | 11.8% | all calls; 4 / 34 | `measured` | No — wrong denominator for the booking-intent success claim |
| Modelled value of booked calls | 4,800 | 4 booked calls × configured 1,200 assumption | `modelled` | No — an assumption participates in the value |
| Recovered revenue attributed to recovered calls | not available | no durable attribution join | `unavailable` | No — the evidence required for attribution does not exist |

`measured`, `modelled`, and `unavailable` describe the evidence basis. **Quotable is a separate decision.** A measured figure can still be unsafe to quote when its population does not support the intended claim.

## Where the behavior lives

| File | What to inspect |
|---|---|
| `src/metric_integrity/models.py` | `Figure`: value, population, calculation inputs, basis, and quote decision |
| `src/metric_integrity/rates.py` | named denominator populations and rate construction |
| `src/metric_integrity/valuation.py` | configured modelled booked-call value and explicit attribution refusal |
| `src/metric_integrity/report.py` | report composition and limitations |
| `tests/` | denominator, basis, quote-safety, attribution, unavailable-state, and finite-value checks |

## Evidence boundary

- The records are synthetic; these are not customer or revenue results.
- `measured` describes how a value was obtained. It does **not** automatically make the value safe to quote for every claim.
- `modelled` means a configured assumption participates in the calculation.
- `unavailable` means the required evidence is missing; it is not a low estimate in disguise.

Verification commands and expected checks: [docs/verification.md](docs/verification.md)

See [PROVENANCE.md](PROVENANCE.md), [docs/invariants.md](docs/invariants.md), and [docs/failure-modes.md](docs/failure-modes.md) for the public boundary and the rules the tests protect.
