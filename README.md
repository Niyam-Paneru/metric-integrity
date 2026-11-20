# Metric Integrity

I can take four bookings and turn **11.8%** into **28.6%** without making one extra booking. Same four appointments; the slide deck is having a great day.

Both percentages can be mathematically correct. The difference is what you count.

I wrote this Python module so a reported metric carries its population, calculation, evidence basis and the claim those actually justify. It makes a number show its homework.

## Four bookings, two denominators

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
