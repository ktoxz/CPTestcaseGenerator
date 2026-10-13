"""Label-based metrics; compile/infrastructure failures are not logic kills."""
from ..domain import Solution, Result

def metrics(solutions: list[Solution], verdicts: dict[str, Result], positive: str,
            negative: str) -> dict:
    pos = [verdicts[s.id].verdict for s in solutions if s.label == positive]
    neg = [verdicts[s.id].verdict for s in solutions if s.label == negative]
    # CE/INFRA cannot be credited as detecting a logic bug.
    pden = sum(v not in {"CE", "INFRA"} for v in pos)
    nden = sum(v not in {"CE", "INFRA"} for v in neg)
    return {
        "positive_label": positive, "negative_label": negative,
        "positive_pass": pos.count("PASS"), "positive_evaluable": pden,
        "negative_killed_logic": sum(v in {"WA", "RE", "TLE"} for v in neg),
        "negative_evaluable": nden,
        "tpr_label_based": pos.count("PASS") / pden if pden else None,
        "tnr_label_based": sum(v in {"WA", "RE", "TLE"} for v in neg) / nden if nden else None,
        "ce_infra": {"positive": sum(v in {"CE", "INFRA"} for v in pos),
                     "negative": sum(v in {"CE", "INFRA"} for v in neg)},
        "warning": "Original and LLM labels are provisional until independently verified.",
    }


