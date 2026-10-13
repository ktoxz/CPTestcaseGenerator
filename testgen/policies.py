"""Pure refinement policies."""
import math

def dynamic_case_bounds(base: int, survivor_count: int,
                        tnr: float | None, target: float = 0.9, *,
                        uncovered_critical: int = 0,
                        rejected_count: int = 0,
                        stalled_rounds: int = 0) -> tuple[int, int]:
    """Return an accepted-case target range based on remaining test pressure."""
    if (base < 1 or survivor_count < 0 or not 0 < target <= 1
            or uncovered_critical < 0 or rejected_count < 0 or stalled_rounds < 0):
        raise ValueError("invalid dynamic case quota inputs")
    gap = 0.0 if tnr is None else max(
        0.0, target - max(0.0, min(1.0, tnr))
    )
    # Avoid ceil(2.0000000000000004) == 3 for values such as 0.9 - 0.7.
    gap_bonus = math.ceil(base * gap - 1e-12)
    pressure = (
        math.ceil(survivor_count / 2)
        + uncovered_critical
        + min(base, rejected_count)
        + 2 * stalled_rounds
    )
    minimum = min(base * 3, max(base, pressure))
    maximum = min(
        base * 3,
        max(minimum, base + survivor_count + uncovered_critical + gap_bonus
            + min(base, rejected_count) + 2 * stalled_rounds),
    )
    return max(1, minimum), max(1, maximum)



def split_mutant_pool(active_wrong, holdout_fraction):
    holdout_count = 0
    if len(active_wrong) >= 5 and holdout_fraction > 0:
        holdout_count = min(len(active_wrong) - 1,
                            max(1, round(len(active_wrong) * holdout_fraction)))
    return (active_wrong[:-holdout_count] if holdout_count else active_wrong,
            active_wrong[-holdout_count:] if holdout_count else [])


def stop_status(metrics, coverage, *, iteration, iterations, case_count,
                survivor_count, stalled_rounds, min_iterations, min_total_cases,
                critical_coverage_target, normal_coverage_target, stall_rounds_to_stop):
    from .coverage import coverage_meets_targets
    status = {
        "metric_threshold": (metrics["tpr_label_based"] is not None
                             and metrics["tnr_label_based"] is not None
                             and metrics["tpr_label_based"] >= 0.9
                             and metrics["tnr_label_based"] >= 0.9),
        "coverage_threshold": coverage_meets_targets(
            coverage, critical_coverage_target, normal_coverage_target),
        "minimum_rounds": iteration + 1 >= min(min_iterations, iterations),
        "minimum_cases": case_count >= min_total_cases,
        "progress_exhausted": not survivor_count or stalled_rounds >= stall_rounds_to_stop,
    }
    return {**status, "met": all(status.values())}
