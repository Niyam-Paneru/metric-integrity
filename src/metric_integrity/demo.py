"""Runnable metric-lineage walkthrough. `python -m metric_integrity.demo`"""

from __future__ import annotations

import sys

from metric_integrity import Call, CallOutcome, Denominator, Figure, Report


def sample() -> list[Call]:
    calls: list[Call] = [Call(CallOutcome.BOOKED, True, 1200.0) for _ in range(4)]
    calls += [Call(CallOutcome.NOT_BOOKING_INTENT, True) for _ in range(2)]
    calls += [Call(CallOutcome.NO_ANSWER, True) for _ in range(8)]
    calls += [Call(CallOutcome.NOT_BOOKING_INTENT, False) for _ in range(20)]
    return calls


def print_figure(figure: Figure) -> None:
    print(figure.label)
    print(f"  value: {figure.formatted_value()}")
    for line in figure.lineage_lines():
        print(f"  {line}")
    print()


def main() -> int:
    report = Report(sample(), assumed_value_per_booking=1200.0)

    print("Metric lineage demo")
    print(f"records: {report.total_calls} calls")
    print()

    print_figure(report.booking_rate(Denominator.BOOKING_INTENT))
    print_figure(report.booking_rate(Denominator.ALL_CALLS))
    print_figure(report.modelled_value())
    print_figure(report.recovered_value())
    return 0


if __name__ == "__main__":
    sys.exit(main())
