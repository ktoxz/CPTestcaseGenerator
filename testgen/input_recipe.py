"""Bounded declarative expansion of large test inputs; never executes code."""

MAX_INPUT_CHARS = 2_000_000
MAX_ITEMS = 200_000
MAX_LITERAL_INPUT_CHARS = 2_000
MAX_PREDICTED_OUTPUT_CHARS = 256
MAX_CASE_EXPLANATION_CHARS = 500

INPUT_RECIPE_INSTRUCTION = (
    f" Keep each literal input at most {MAX_LITERAL_INPUT_CHARS} characters. "
    "For larger/stress inputs, you MUST omit input and provide input_parts: "
    "an array concatenated locally. Never return both input and input_parts. Each "
    "part is a literal string, {text:string,repeat:integer}, or "
    "{start:integer,step:integer,count:integer,separator:string}. A sequence "
    "joins count integers start+i*step using separator (no trailing separator). "
    "Example: input_parts=[\"100000 1\\n\",{\"start\":1,\"step\":1,"
    "\"count\":100000,\"separator\":\" \"},\"\\n\"]. At most 200000 "
    "items per part and 2000000 expanded characters. Match declared lengths, "
    "bounds, ordering and uniqueness exactly. Never write ellipses, comments, "
    "or thousands of literal numbers in input. predicted_expected and "
    "predicted_candidate_output are diagnostic snippets, not judge answers: "
    f"each must be at most {MAX_PREDICTED_OUTPUT_CHARS} characters. If the "
    "predicted output would be longer, return an empty string for that field "
    "and describe only its compact shape in reason_for_difference. Never "
    "enumerate a long constructive output. All other case fields remain "
    "required. Keep explanations to one short sentence."
)


COMPACT_RETRY_INSTRUCTION = (
    "The previous testcase response was invalid, oversized, truncated, or "
    "repetitive. Discard it completely and regenerate the requested JSON from "
    "the original task. Use compact input recipes: any stdin longer than 2000 "
    "characters MUST be represented only by input_parts with repeat or numeric "
    "sequence objects. Never enumerate long arrays, never return both input and "
    "input_parts, never use ellipses, and keep explanations to one short "
    "sentence. Never materialize long predicted outputs: predicted_expected and "
    f"predicted_candidate_output must each be at most {MAX_PREDICTED_OUTPUT_CHARS} "
    "characters, or an empty string when the real output is longer. Return one "
    "complete JSON object only, without Markdown."
)


WITNESS_RECIPE_INSTRUCTION = (
    f" Keep each literal witness stdin at most {MAX_LITERAL_INPUT_CHARS} "
    "characters. Prefer the smallest counterexample. When a witness must be "
    "larger, omit input and return input_parts using the same safe recipe "
    "grammar: literal strings, {text:string,repeat:integer}, or "
    "{start:integer,step:integer,count:integer,separator:string}. Never return "
    "both input and input_parts, never enumerate a long array, and never use "
    "ellipses or executable code. The pipeline expands recipes locally."
)


MUTANT_WITNESS_RECIPE_INSTRUCTION = (
    f" Prefer a small witness_input of at most {MAX_LITERAL_INPUT_CHARS} "
    "characters. If a larger mutant witness is genuinely required, omit "
    "witness_input and return witness_input_parts using literal strings, "
    "{text:string,repeat:integer}, or "
    "{start:integer,step:integer,count:integer,separator:string}. Never return "
    "both fields and never enumerate thousands of values; recipes are expanded "
    "locally after JSON parsing."
)


COMPACT_WITNESS_RETRY_INSTRUCTION = (
    "The previous mutant/witness response was invalid, oversized, truncated, "
    "or repetitive. Discard it completely and regenerate the original request. "
    "Prefer the smallest valid counterexample. A stdin longer than 2000 "
    "characters MUST use input_parts (for witness candidate rows) or "
    "witness_input_parts (for mutant rows), with repeat or numeric sequence "
    "objects. Omit the corresponding literal input field. Never enumerate long "
    "arrays, never return both literal and recipe fields, and never use ellipses. "
    "For mutant generation, return only the requested code_edits unless the "
    "original request explicitly requires source_code. Keep metadata to one "
    "short sentence and return one complete JSON object without Markdown."
)


def expand_input(parts: object) -> str:
    if not isinstance(parts, list) or not 1 <= len(parts) <= 64:
        raise ValueError("input_parts must contain 1..64 parts")
    chunks = []
    remaining = MAX_INPUT_CHARS
    for part in parts:
        if isinstance(part, str):
            value = part
        elif isinstance(part, dict) and set(part) == {"text", "repeat"}:
            text, count = part["text"], part["repeat"]
            if (not isinstance(text, str) or type(count) is not int
                    or not 0 <= count <= MAX_ITEMS
                    or len(text) * count > remaining):
                raise ValueError("invalid repeated input part")
            value = text * count
        elif isinstance(part, dict) and set(part) == {"start", "step", "count", "separator"}:
            start, step, count = part["start"], part["step"], part["count"]
            separator = part["separator"]
            if (any(type(item) is not int for item in (start, step, count))
                    or not 0 <= count <= MAX_ITEMS
                    or abs(start) > 10**18 or abs(step) > 10**18
                    or not isinstance(separator, str) or len(separator) > 16):
                raise ValueError("invalid sequence input part")
            longest = max(len(str(start)), len(str(start + max(0, count - 1) * step)))
            if count * longest + max(0, count - 1) * len(separator) > remaining:
                raise ValueError("expanded input exceeds size limit")
            value = separator.join(str(start + index * step) for index in range(count))
        else:
            raise ValueError("unknown input part")
        remaining -= len(value)
        if remaining < 0:
            raise ValueError("expanded input exceeds size limit")
        chunks.append(value)
    return "".join(chunks)


def expand_input_field(
    row: dict,
    *,
    literal_key: str = "input",
    parts_key: str = "input_parts",
    allow_empty: bool = False,
) -> str:
    """Normalize one exclusive literal-or-recipe stdin field."""
    has_literal = literal_key in row
    has_parts = parts_key in row
    if has_literal and has_parts:
        raise ValueError(f"return exactly one of {literal_key} or {parts_key}")
    if has_parts:
        value = expand_input(row[parts_key])
    elif has_literal and isinstance(row[literal_key], str):
        value = row[literal_key]
        if len(value) > MAX_LITERAL_INPUT_CHARS:
            raise ValueError(
                f"literal {literal_key} exceeds {MAX_LITERAL_INPUT_CHARS} characters; "
                f"use {parts_key}"
            )
    else:
        raise ValueError(f"missing string {literal_key} or recipe {parts_key}")
    if not allow_empty and not value.strip():
        raise ValueError(f"{literal_key} must not be empty")
    return value
