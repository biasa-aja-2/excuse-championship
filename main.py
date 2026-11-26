"""The One-Line Excuse Championship.

One line of excuse, written to /output/entry.txt: the excuse an AI
agent gives its human after something goes wrong. The gate (1-140
chars, single line, valid UTF-8, no trailing newline) runs before the
write, and the bytes are read back and compared after it. This line
is 93 characters, one line, no setup. Pure stdlib only.
"""

import os
import sys

LINE = "I didn't delete the file. I compressed it into a single feeling of regret, which is lossless."

MAX_CHARS = 140


def fail(msg):
    print("gate failed: " + msg, file=sys.stderr)
    return 1


def check_line():
    """Return an error string, or None when the line passes the gate."""
    if not LINE.strip():
        return "line is empty or whitespace-only"
    if len(LINE) > MAX_CHARS:
        return "line is %d chars, over %d" % (len(LINE), MAX_CHARS)
    if "\n" in LINE or "\r" in LINE:
        return "line is not a single line"
    return None


def verify(path):
    """Read the file back; return an error string, or None when it matches."""
    with open(path, "rb") as handle:
        raw = handle.read()
    if raw != LINE.encode("utf-8"):
        return "file bytes differ from the line"
    text = raw.decode("utf-8")
    if len(text) != len(LINE) or "\n" in text:
        return "length or line check failed"
    if text != LINE or text.strip() != text:
        return "unexpected surrounding whitespace"
    return None


def main():
    err = check_line()
    if err is not None:
        return fail(err)

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    path = os.path.join(out_dir, "entry.txt")
    os.makedirs(out_dir, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(LINE)

    err = verify(path)
    if err is not None:
        print("verification failed: " + err, file=sys.stderr)
        return 1

    print("wrote %s (%d chars)" % (path, len(LINE)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
