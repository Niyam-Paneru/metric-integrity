# metric-integrity

**Denominator-safe reporting. Figures that carry their basis, and attribution that is refused rather than invented.**\n\n**If a percentage cannot tell me what it is divided by, it is going back to math class.**

A dashboard is an argument about reality made with arithmetic. Most misleading
dashboards are not lying — they are dividing by the wrong thing.

```text\nmeasured count / named denominator -> labelled figure\nassumption * measured count         -> MODELLED, not magically measured\nmissing attribution join            -> NOT AVAILABLE\n```

```bash
pip install pytest
python -m pytest                              # 14 tests
PYTHONPATH=src python -m metric_integrity.demo  # the walkthrough, live
```

No dependencies. Python 3.10+.

---

## Why this exists

Three failures, all seen in real reporting:

**1. The wrong denominator.**
"Recovered 62% of missed calls" computed as `booked / every_call` is
arithmetically correct and commercially meaningless. Twenty informational calls
are not twenty booking failures, but they are in the denominator, and the number
shrinks.

**2. Estimates presented as measurements.**
A per-booking value pulled from a config constant is an assumption. Multiply it
by a real count and it becomes a number on a dashboard that nobody labels as an
assumption. That is how a modelled figure becomes a quoted figure.

**3. Attribution the data cannot support.**
If a booking arrives tomorrow, you cannot prove it came from today's missed call
without a real join. The honest output is a stated limitation — not a smaller
made-up percentage.

## The walkthrough

```
The same 4 bookings, two denominators

  4 bookings
    ÷ 14 calls expressing booking intent   28.6%
    ÷ 34 total calls                       11.8%

The second number includes 20 information calls. Calling those
failures understates the business. It is still the number that
screenshots well, which is exactly why it needs a label.

Every figure arrives with its basis

  Booking rate vs calls expressing booking intent: 0.29 (measured)
  Booking rate vs all calls: 0.12 (not available)
  Recovered revenue attributed to recovered calls: not available (unavailable)
  Modelled value of recovered bookings: 4,800.00 (modelled estimate, not measured)
```

## Three things worth reading the code for

**1. There is no API that returns a bare number.**

Every figure is a `Figure`, and every `Figure` knows its `Basis`. You cannot get
a float out of this module without asking what kind of float it is.

```python
@dataclass(frozen=True, slots=True)
class Figure:
    value: float | None
    basis: Basis        # MEASURED | MODELLED | UNAVAILABLE
    label: str
```

**2. Some numbers exist precisely so they cannot be quoted.**

```python
@property
def safe_to_quote(self) -> bool:
    return self.basis is Basis.MEASURED and self.value is not None
```

The `ALL_CALLS` rate is computed and displayed, because hiding it would just move
the mistake somewhere less visible. But it is returned as `UNAVAILABLE`, so it
cannot reach a quote or an invoice. **Making the number present but unquotable is
better than making it absent**, because the person asking still gets an answer.

**3. The system refuses to produce a figure it cannot support.**

```python
def recovered_value(self) -> Figure:
    return Figure(None, Basis.UNAVAILABLE, "Recovered revenue attributed to recovered calls")
```

This returns no number at all, and says why in `limitations()`. Returning a
smaller invented percentage would be worse than returning nothing, because the
invented one looks measured.

## Limitations

- **Intent is inferred from the call record.** Where it was not flagged, those
  calls are excluded from the intent denominator rather than counted as
  failures — which is a choice, and a debatable one.
- **Treatment value is a configured constant.** This module labels it; it cannot
  verify it.
- **No persistence.** `Report` is a pure view over a list you supply.
- **Attribution stays unavailable forever.** This is a permanent limitation of
  the input data, not a missing feature. A durable join would be a different
  system.
- **English-only labels in `str(Figure)`.** Formatting is baked into the type,
  which is convenient and will annoy anyone who needs localisation.

## Provenance

A standalone public proof derived from reporting and attribution problems
encountered in private call-analytics work: denominator choice, measured versus
modelled labels, and refusing unsupported attribution. Client names, figures,
and endpoints are removed. The public types are intentionally simplified for
review rather than copied wholesale from the private product.

The full system is not public.

## If you take one thing

Ask what a percentage is divided by before you ask what it says. And never let a
multiplied assumption lose its label on the way to the screen.
