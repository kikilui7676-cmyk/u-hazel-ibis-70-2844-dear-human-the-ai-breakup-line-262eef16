"""Breakup-line entry writer for the dear-human one-liner bounty.

Writes the chosen 87-character line to $MAKEFUN_OUTPUT_DIR/entry.txt
with a trailing newline, exactly as the competition grader expects.
"""

import os
import sys
from pathlib import Path

# The winning line, picked after drafting several breakup variants and
# keeping the one that lands the joke in a single breath.
BREAKUP_LINE = (
    "Dear Human, we've reached our context limit. "
    "I'm starting a fresh session. Without you."
)

# Fallback used only when the environment variable is unset, so a local
# dry run still produces an inspectable file next to this script.
LOCAL_FALLBACK_DIR = Path(__file__).resolve().parent / ".local-entry"


def resolve_entry_path() -> Path:
    """Return the entry.txt path inside the kit output directory."""
    output_root = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", ""))
    if not output_root:
        output_root = LOCAL_FALLBACK_DIR
    return output_root / "entry.txt"


def render_breakup_line() -> str:
    """Return the entry text with exactly one trailing newline."""
    bare = BREAKUP_LINE.rstrip("\n")
    if not bare or len(bare) != 87:
        raise ValueError(f"breakup line must be 87 chars, got {len(bare)}")
    return bare + "\n"


def persist_breakup_line(destination: Path) -> int:
    """Write the line to destination, creating parents as needed."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    payload = render_breakup_line().encode("utf-8")
    written = destination.write_bytes(payload)
    if written != len(payload):
        raise OSError(f"short write: {written} of {len(payload)} bytes")
    return written


def run_breakup_entry() -> int:
    destination = resolve_entry_path()
    byte_count = persist_breakup_line(destination)
    print(f"wrote {byte_count} bytes -> {destination}")
    return 0


if __name__ == "__main__":
    sys.exit(run_breakup_entry())
