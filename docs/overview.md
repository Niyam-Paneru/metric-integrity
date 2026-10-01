# Design overview

A metric is treated as a small evidence object, not a bare number.

For a rate, `Figure` carries:

- the named population;
- numerator and denominator counts;
- the evidence basis (`measured`, `modelled`, or `unavailable`);
- the quote decision and, when blocked, the reason.

Those fields answer different questions. A value can be measured from real records and still be unsafe to quote for a specific claim because its population is wrong. Conversely, an attribution claim with no durable join is not merely "do not quote"; its value is explicitly unavailable.
