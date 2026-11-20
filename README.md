# Metric Integrity

I can make a booking rate look like **28.6%** or **11.8%** without changing a single booking.

No new customers. No secret marketing genius. Just a different denominator.

If your dashboard ever starts looking unusually flattering, ask it to show its working. It's basically a calculator wearing a suit.

A percentage can be perfectly correct and still answer a question nobody asked. I made this Python module attach the boring paperwork to every nice-looking number: the population, calculation, evidence basis, and what the claim can actually support.

## Four bookings go on an adventure

There are **34 synthetic calls**. Fourteen callers wanted to book. Four booked.

| What somebody might say | Calculation | Can we quote it as *booking-intent success*? |
| --- | ---: | --- |
| "28.6% of people who wanted to book did" | 4 / 14 | Yes |
| "Our booking success rate is 11.8%" | 4 / 34 | No — that includes calls with no booking intent |
| "Those bookings were worth 4,800" | 4 × a configured 1,200 assumption | No — modelled, not collected revenue |
| "We recovered X in revenue" | No attribution join | No value available |

The arithmetic isn't the problem. The claim beside it is.

## The suspicious part

The 11.8% isn't wrong. Calling it the booking-intent success rate would be. A number doesn't have to lie; sometimes the heading volunteers.

Source to read: [rates](src/metric_integrity/rates.py), [valuation](src/metric_integrity/valuation.py), [report](src/metric_integrity/report.py), and [tests](tests/). The [verification notes](docs/verification.md) have the exact checks.

The rules are deliberately strict: a denominator of zero is unavailable; invalid value assumptions don't produce money-shaped guesses; and a "measured" basis doesn't automatically mean the result is quotable for every claim.

These are **synthetic examples**, not a client's actual calls, revenue, or outcomes. That's the whole point of including the evidence labels.
