# Failure modes

## Correct arithmetic, wrong population

`booked / all_calls` is measurable arithmetic, but it does not answer the booking-intent success question. Response: carry the population and calculation on the figure and mark that claim `do not quote`.

## Unsupported denominator defaults to a quotable claim

An invalid denominator argument previously fell through to the booking-intent branch, presenting the result as a measured, quotable success rate. Response: accept only the two declared `Denominator` enum members and reject all other values before computing the rate.

## Modelled value presented as measured

An assumption is multiplied by a real count and loses its label. Response: keep `basis=modelled` attached to the figure and block quoting it as measured.

## Missing attribution join

The system cannot prove which later booking came from which earlier call. Response: return `basis=unavailable`, no numeric value, and the reason `missing durable attribution join`.

## Zero denominator

A rate would divide by an empty population. Response: return unavailable rather than a misleading zero.

## Detached context

A number is copied without its population, calculation, or evidence basis. Response: the runnable demo exposes the lineage next to the value, and tests assert those fields directly.
