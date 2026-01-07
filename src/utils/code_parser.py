import re
from typing import Optional
import ast
import os

DEBUG = os.environ.get("CODE_PARSER_DEBUG", "").lower() in ("1", "true", "yes")


def _is_valid_python(code: str) -> bool:
    """
    Check if code is syntactically valid Python.

    Returns True if valid, False otherwise.
    """
    try:
        ast.parse(code)
        return True
    except SyntaxError as e:
        print(f"SyntaxError during validation: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error during validation: {e}")
        return False


def _clean_and_validate_code(code_snippet: str) -> Optional[str]:
    """
    Clean code and validate it's syntactically correct Python.

    Handles indentation normalization and validation.

    Returns cleaned code if valid, None otherwise.
    """

    if not code_snippet:
        return None

    lines = code_snippet.splitlines()
    non_empty_lines = [line for line in lines if line.strip()]

    if not non_empty_lines:
        return None

    min_indent = min(
        (len(line) - len(line.lstrip()) for line in non_empty_lines if line.lstrip()),
        default=0,
    )

    dedented = "\n".join(line[min_indent:] for line in lines)

    cleaned = dedented.strip()

    if _is_valid_python(cleaned):
        return cleaned
    return None


def extract_python_code(llm_output: str) -> Optional[str]:
    """
    Extract clean Python code from LLM output.

    Handles common patterns:
    - Code wrapped in ```python ... ``` blocks
    - Code wrapped in ``` ... ``` blocks
    - Raw code without markdown
    - Syntax validation

    Set CODE_PARSER_DEBUG=1 environment variable for verbose debugging.
    """
    if not llm_output:
        return None

    if DEBUG:
        print("\n" + "=" * 60)
        print("DEBUG: Raw LLM output:")
        print("-" * 60)
        print(llm_output)
        print("-" * 60)

    candidates = []

    # Pattern 1: ```python ... ```
    python_block = re.findall(r"```python\s*\n(.*?)```", llm_output, re.DOTALL)
    if DEBUG:
        print(f"DEBUG: Pattern 1 (```python) matches: {len(python_block)}")
    candidates.extend(python_block)

    # Pattern 2: ``` ... ``` (generic code block, newline required after ```)
    generic_block = re.findall(r"```\s*\n(.*?)```", llm_output, re.DOTALL)
    if DEBUG:
        print(f"DEBUG: Pattern 2 (``` with newline) matches: {len(generic_block)}")
    candidates.extend(generic_block)

    # Pattern 2b: ``` ... ``` (generic code block, no newline - code starts on same line)
    generic_block_inline = re.findall(r"```([^\n`].*?)```", llm_output, re.DOTALL)
    if DEBUG:
        print(f"DEBUG: Pattern 2b (``` inline) matches: {len(generic_block_inline)}")
    candidates.extend(generic_block_inline)

    # Pattern 3: No markdown, look for def/class as code start (allowing leading whitespace)
    # Find first function or class definition
    code_start = re.search(r"^\s*(def |class )", llm_output, re.MULTILINE)
    if code_start:
        if DEBUG:
            print(f"DEBUG: Pattern 3 (def/class) found at position {code_start.start()}")
        candidates.append(llm_output[code_start.start() :].strip())
    elif DEBUG:
        print("DEBUG: Pattern 3 (def/class) - no match")

    if DEBUG:
        print(f"DEBUG: Total candidates: {len(candidates)}")
        for i, c in enumerate(candidates):
            preview = c[:100].replace("\n", "\\n")
            print(f"DEBUG: Candidate {i}: {preview}...")

    for candidate in candidates:
        cleaned = _clean_and_validate_code(candidate)
        if cleaned:
            if DEBUG:
                print(f"DEBUG: Successfully extracted valid code ({len(cleaned)} chars)")
                print("=" * 60 + "\n")
            return cleaned

    print("Warning: No valid Python code found in LLM output.")
    if DEBUG:
        print("DEBUG: Attempting fallback validation on raw output...")
    cleaned = _clean_and_validate_code(llm_output)
    if cleaned:
        if DEBUG:
            print("DEBUG: Fallback succeeded")
            print("=" * 60 + "\n")
        return cleaned

    print("Could not validate any extracted code.")
    if DEBUG:
        print("=" * 60 + "\n")
    return None
