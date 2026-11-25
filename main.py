#!/usr/bin/env python3
"""The GPS Swears It Was a Shortcut — make.fun entry.

Writes the GPS's one-line excuse for sending the driver down the
wrong road to <MAKEFUN_OUTPUT_DIR>/entry.txt (default /output).
Gate: UTF-8 text of 1 to 200 characters, not only whitespace,
a single line of plain text, no setup, no dialogue tags.
"""

import os
import sys
import unicodedata

# The GPS's excuse, in its own voice: smug, defensive, blaming the
# map — and, with a straight face, the driver who followed it.
LINE = (
    "Per my map, this lake is a shortcut. You chose to drive into it "
    "\u2014 I merely suggested it with the full confidence of a professional."
)

MAX_CHARS = 200


def validate(line: str) -> bytes:
    """Check the line against the competition gate and return its bytes."""
    if not line or len(line) > MAX_CHARS:
        raise ValueError(f"line must be 1-{MAX_CHARS} chars, got {len(line)}")
    if not line.strip():
        raise ValueError("line must not be only whitespace")
    if line != line.strip():
        raise ValueError("line must not have leading or trailing whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("line must be a single line")
    bad = [ch for ch in line if unicodedata.category(ch).startswith("C")]
    if bad:
        raise ValueError(f"line must not contain control characters: {bad!r}")
    if "  " in line:
        raise ValueError("line must not contain doubled spaces")
    data = line.encode("utf-8")
    if data.decode("utf-8") != line:
        raise ValueError("line must round-trip cleanly as UTF-8")
    return data


def main() -> int:
    data = validate(LINE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "wb") as fh:
        fh.write(data)  # exactly the line: no trailing newline
    with open(path, "rb") as fh:
        if fh.read() != data:
            raise RuntimeError("verification failed: entry.txt bytes differ")
    print(f"wrote {path} ({len(LINE)} chars, {len(data)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
