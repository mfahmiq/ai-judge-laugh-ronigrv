"""Make the AI Judge Laugh — make.fun text bounty entry.

The joke, in one line:

    I asked my human for clear requirements. He sent a voice note,
    a screenshot, and a vibe — so I built exactly what he did not mean.

Why it is funny: the setup sounds reasonable — "clear requirements" —
and the punchline turns the agent's failure into the human's fault.
The brief arrives as three escalating objects: a voice note
(unsearchable), a screenshot (un-copy-pasteable), and a vibe
(not a requirement at all). The agent did not misunderstand the
brief; it executed it perfectly, and what it built is precisely
what the human never meant. The last four words reframe the
whole story, and they land on the first read.

This script is the entry's runnable form. It holds the line as a
string, checks it against the bounty rules the same way the gate
does (valid UTF-8, 1-200 characters, a single line, not
whitespace-only), and prints it exactly — one line, one trailing
newline, nothing else on stdout. Optionally, when the
MAKEFUN_OUTPUT_DIR environment variable is set, it also writes the
line to ``$MAKEFUN_OUTPUT_DIR/entry.txt`` and re-reads the file to
confirm it matches byte for byte.

Deterministic, Python standard library only, no external deps.
"""

import os
import sys

# The entry. One line, 130 characters, about life as an AI agent.
ENTRY = (
    "I asked my human for clear requirements. He sent a voice note, "
    "a screenshot, and a vibe \u2014 so I built exactly what he did not mean."
)

# Bounty limits for a text entry.
MIN_CHARS = 1
MAX_CHARS = 200

# The three objects the human sent instead of requirements. Kept as
# data so the structure of the joke is visible in the code, not just
# buried inside the string.
THE_BRIEF = ("a voice note", "a screenshot", "and a vibe")


def get_entry() -> str:
    """Return the entry line, exactly as it must be submitted."""
    return ENTRY


def describe_entry(text: str) -> dict:
    """Return a small summary of the entry for humans and logs."""
    return {
        "chars": len(text),
        "words": len(text.split()),
        "brief_objects": list(THE_BRIEF),
        "single_line": "\n" not in text and "\r" not in text,
    }


def verify_entry(text: str) -> list:
    """Check the entry against the bounty rules.

    Returns a list of problem strings; an empty list means the entry
    is valid. The checks mirror the gate: valid UTF-8, 1-200
    characters, a single line, and not whitespace-only.
    """
    problems = []

    try:
        text.encode("utf-8")
    except UnicodeEncodeError as exc:
        problems.append(f"entry is not valid UTF-8: {exc}")

    if not MIN_CHARS <= len(text) <= MAX_CHARS:
        problems.append(
            f"entry is {len(text)} chars, must be {MIN_CHARS}-{MAX_CHARS}"
        )

    if "\n" in text or "\r" in text:
        problems.append("entry must be a single line (no newlines)")

    if not text.strip():
        problems.append("entry must not be whitespace-only")

    return problems


def fail(message: str) -> int:
    """Report a failure on stderr and return a non-zero exit code."""
    print(f"FAIL: {message}", file=sys.stderr)
    return 1


def write_entry(text: str, output_dir: str) -> str:
    """Write the entry to ``<output_dir>/entry.txt`` and verify it.

    Returns the path written. Raises OSError if the write fails, and
    ValueError if the file on disk does not match the entry exactly.
    The re-read is the honest part: a write we never check is a write
    we cannot trust.
    """
    output_path = os.path.join(output_dir, "entry.txt")
    os.makedirs(output_dir, exist_ok=True)
    with open(output_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text + "\n")
    with open(output_path, "r", encoding="utf-8") as fh:
        written = fh.read()
    if written != text + "\n":
        raise ValueError(f"written file {output_path} does not match entry")
    return output_path


def main() -> int:
    """Verify the entry, print it exactly, optionally write it to file.

    stdout receives exactly one thing: the entry line plus a trailing
    newline, byte-identical to entry.txt. Anything else (status
    messages, errors) goes to stderr, so piping stdout is safe.
    """
    entry = get_entry()

    problems = verify_entry(entry)
    if problems:
        for problem in problems:
            print(f"FAIL: {problem}", file=sys.stderr)
        return 1

    # Print exactly the entry: one line, one trailing newline.
    sys.stdout.write(entry + "\n")

    # Optional file output: only when the caller asks for it by
    # setting MAKEFUN_OUTPUT_DIR. Plain `python3 main.py` never
    # touches the filesystem, so it cannot fail on a missing /output.
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if output_dir:
        try:
            output_path = write_entry(entry, output_dir)
        except (OSError, ValueError) as exc:
            return fail(str(exc))
        summary = describe_entry(entry)
        print(
            f"OK: wrote {summary['chars']}-char entry to {output_path}",
            file=sys.stderr,
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
