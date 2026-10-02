# Decisions

## Keep evidence basis separate from quote permission

`measured` says the value came from observed records. `safe_to_quote` says the value supports the intended claim. The all-calls booking rate is therefore measured arithmetic but explicitly not quotable as the booking-intent success rate.

## Put denominator lineage on the figure

Rates carry their population, numerator, and denominator instead of relying on a label alone.

## Modelled values stay modelled

A configured per-booking assumption multiplied by a measured count remains a modelled estimate.

## Missing attribution is unavailable

Without a durable join from the earlier call to the later booking, recovered revenue has no numeric value. The missing evidence is named in `quote_reason`.
