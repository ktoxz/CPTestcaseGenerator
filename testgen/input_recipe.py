"""Bounded declarative expansion of large test inputs; never executes code."""

MAX_INPUT_CHARS = 2_000_000
MAX_ITEMS = 200_000

INPUT_RECIPE_INSTRUCTION = (
    " Keep each literal input under 2000 characters. For larger/stress inputs, "
    "omit input and provide input_parts: an array concatenated locally. Each "
    "part is a literal string, {text:string,repeat:integer}, or "
    "{start:integer,step:integer,count:integer,separator:string}. A sequence "
    "joins count integers start+i*step using separator (no trailing separator). "
    "Example: input_parts=[\"100000 1\\n\",{\"start\":1,\"step\":1,"
    "\"count\":100000,\"separator\":\" \"},\"\\n\"]. At most 200000 "
    "items per part and 2000000 expanded characters. Match declared lengths, "
    "bounds, ordering and uniqueness exactly. Never write ellipses, comments, "
    "or thousands of literal numbers in input. All other case fields remain "
    "required. Keep explanations to one short sentence."
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
