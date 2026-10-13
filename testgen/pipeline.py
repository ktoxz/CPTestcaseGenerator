"""Compatibility API for existing pipeline callers."""
from .application.run_pipeline import RunPipeline as Pipeline
from .problem import samples, requires_input_aware_checker
from .evaluation.metrics import metrics
from .policies import dynamic_case_bounds
from .suite import suite_lock, case_record, merge_certified_coverage
