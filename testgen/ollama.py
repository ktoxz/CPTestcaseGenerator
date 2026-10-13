"""Compatibility imports for the original public API."""
import urllib.request
from .infrastructure.llm.ollama import (
    OllamaClient, _escape_json_string_controls, _remove_json_trailing_commas,
    _json_candidates, _parse_json_locally,
)
from .generation.solutions import SolutionGenerationService as OllamaSolutionGenerator
from .generation.cases import CaseGenerationService as OllamaCaseGenerator
