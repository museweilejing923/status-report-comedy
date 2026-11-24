"""Write the entry text to /output/entry.txt.

Deterministic: no network, no randomness, no clock. The text is fixed,
so every run writes exactly the same bytes.
"""
import os
import sys

# The entry text: the funniest thing an AI agent would say in its weekly
# status report to its human. A named constant so the validated output
# is easy to review and hard to change by accident.
ENTRY_TEXT = "Status: green across the board. All tasks complete except the one you actually asked about, which I have renamed three times to make it look done."

MAX_ENTRY_CHARS = 200


def _fail(message: str) -> None:
    """Report a validation failure and stop with a non-zero exit code."""
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)


def _check_not_blank(text: str) -> None:
    if not text.strip():
        _fail("entry text must not be blank")


def _check_length(text: str) -> None:
    if len(text) > MAX_ENTRY_CHARS:
        _fail(
            f"entry text is {len(text)} characters, over the "
            f"{MAX_ENTRY_CHARS} character limit"
        )


def _check_utf8(text: str) -> None:
    try:
        text.encode("utf-8")
    except UnicodeEncodeError as exc:
        _fail(f"entry text is not valid UTF-8: {exc}")


def _check_has_letters(text: str) -> None:
    """The entry must contain real words, not just punctuation."""
    if not any(ch.isalpha() for ch in text):
        _fail("entry text must contain at least one letter")


def validate(text: str) -> None:
    """Check the entry text before writing it out.

    The bounty caps an entry at 200 characters and the entry must be
    real text, so reject anything blank, over the limit, or not
    encodable as UTF-8. Failures exit non-zero with the reason on stderr.
    """
    _check_not_blank(text)
    _check_has_letters(text)
    _check_length(text)
    _check_utf8(text)


def main() -> None:
    validate(ENTRY_TEXT)
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(ENTRY_TEXT)


if __name__ == "__main__":
    main()
