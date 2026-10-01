# Design overview

A dashboard number has two pieces of meaning that should travel with it:

1. **what population was used as the denominator;**
2. **how the number came to exist.**

This repository keeps both visible.

The public model separates:

- call/figure types;
- denominator choice;
- measured vs modelled vs unavailable basis;
- attribution limitations.

The important behavior is refusal: if the data cannot support an attribution, the API returns an unavailable figure rather than inventing a smaller, more believable number.
