"""Runnable walkthrough. `python -m metric_integrity.demo`"""

from __future__ import annotations

import sys

from metric_integrity import Call, CallOutcome, Denominator, Report

GREEN, DIM, BOLD, OFF = "\033[32m", "\033[2m", "\033[1m", "\033[0m"


def sample() -> list[Call]:
    calls: list[Call] = [Call(CallOutcome.BOOKED, True, 1200.0) for _ in range(4)]
    calls += [Call(CallOutcome.NOT_BOOKING_INTENT, True) for _ in range(2)]
    calls += [Call(CallOutcome.NO_ANSWER, True) for _ in range(8)]
    calls += [Call(CallOutcome.NOT_BOOKING_INTENT, False) for _ in range(20)]
    return calls


def main() -> int:
    report = Report(sample(), assumed_value_per_booking=1200.0)

    print(f"{BOLD}\nThe same 4 bookings, two denominators{OFF}")
    print(f"{DIM}   Both numbers are arithmetically correct. Only one describes{OFF}")
    print(f"{DIM}   the business.{OFF}\n")

    intent = report.booking_rate(Denominator.BOOKING_INTENT)
    everything = report.booking_rate(Denominator.ALL_CALLS)

    print(f"  {DIM}4 bookings{OFF}")
    print(f"    ÷ {report.booking_intent_calls} calls expressing booking intent   "
          f"{GREEN}{intent.value:.1%}{OFF}")
    print(f"    ÷ {report.total_calls} total calls                        "
          f"{DIM}{everything.value:.1%}{OFF}")
    print()
    print(f"  {DIM}The second number includes 20 information calls. Calling those{OFF}")
    print(f"  {DIM}failures understates the business. It is still the number that{OFF}")
    print(f"  {DIM}screenshots well, which is exactly why it needs a label.{OFF}\n")

    print(f"{BOLD}\nEvery figure arrives with its basis{OFF}\n")
    for line in report.summary():
        if line.startswith("  - ") or not line.strip():
            print(f"    {DIM}{line}{OFF}" if line.startswith("  - ") else "")
            continue
        if "modelled" in line:
            print(f"  {DIM}{line}{OFF}")
        elif "not available" in line:
            print(f"  {DIM}{line}{OFF}")
        else:
            print(f"  {line}")

    print(f"\n{BOLD}What the system refuses to produce{OFF}")
    print(f"{DIM}   A recovered-revenue figure, because no durable join exists{OFF}")
    print(f"{DIM}   between a booking and the call that prompted it. Returning a{OFF}")
    print(f"{DIM}   smaller invented percentage would be worse than nothing.{OFF}\n")

    print(f"{BOLD}   Every line above is produced by code in this repo.{OFF}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
