# Metric Integrity

A small Python example for keeping a metric's lineage attached to the number: the population it describes, the calculation that produced it, the evidence basis, and whether the result is safe to quote.

**Decimal places are not a permission slip.**

This is a public sample of reporting rules from my private voice/booking analytics work. Synthetic records make the evidence easy to inspect. I can extend these rules into the surrounding reports, dashboards, and integrations for other workflows.

## Measured rates: check the denominator before quoting

```mermaid
flowchart TB
    P["<b>Choose named population</b>"] --> D{"Denominator nonzero?"}
    D -- No --> U["<b>Unavailable</b><br/>value = None, not quotable"]
    D -- Yes --> R["<b>Compute rate + lineage</b><br/>basis = measured"]
    R --> Q{"Population fits<br/>the booking-intent claim?"}
    Q -- Yes --> Y["<b>Quotable</b><br/>booking-intent population"]
    Q -- No --> N["<b>Not quotable for that claim</b><br/>all-call population"]
    classDef input fill:#e8e6df,stroke:#55534a,color:#20201d,stroke-width:2px;
    classDef pass fill:#d2e5d8,stroke:#38734d,color:#183923,stroke-width:2px;
    classDef stop fill:#f4dadd,stroke:#b14253,color:#611c29,stroke-width:2px;
    class P,D,R,Q input;
    class Y pass;
    class U,N stop;
```

## Value estimates: expose the assumption or missing evidence

```mermaid
flowchart TB
    V["<b>Value request</b>"] --> K{"Which value?"}
    K -- Modelled bookings --> A{"Positive finite<br/>per-booking assumption?"}
    A -- Yes --> M["<b>Modelled value</b><br/>booked count × assumption<br/>not quotable"]
    A -- No --> U["<b>Unavailable</b><br/>value = None, not quotable"]
    K -- Attributed recovered revenue --> J["<b>No durable attribution join</b><br/>in this sample"]
    J --> U
    classDef input fill:#e8e6df,stroke:#55534a,color:#20201d,stroke-width:2px;
    classDef stop fill:#f4dadd,stroke:#b14253,color:#611c29,stroke-width:2px;
    class V,K,A input;
    class M,U,J stop;
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
