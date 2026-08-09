#!/usr/bin/env python3
"""check_layout.py — parse-only checker for LAYOUT.txt files (format v1).

Implements the G11 syntactic validity rules of the LAYOUT.txt grammar.
This is NOT the structural verifier (V2 match against an app tree) — it
checks that a file parses, nothing more.

Exit codes (SPEC.md V4 semantics):
  0  all files valid
  2  any parse error (per G11, one malformed widget line fails the file)
  1  usage error or unreadable file

Deliberately NOT checked (convention-only or unverifiable, per the spec):
  - widget type vocabulary (any type is legal; unknown = INFO, never error)
  - variant values, attrs content (opaque), note text/placement
  - hierarchy/indentation consistency beyond the tab ban
  - xN subtree semantics (identical-structure rule is author judgment)
  - filename conventions, cross-file references, screen inventory

Interpretation notes:
  - A tab in the leading whitespace of a line WITH CONTENT is a parse
    error (G1). Whitespace-only lines are blank and ignored.
  - The first `)` closes a widget (attrs may not contain `)` by G3);
    anything after it must be empty or a single `xN` token (G9).
  - `xN` accepts `x` followed by digits with value >= 1; `x0`, `X2`, and
    other trailing tokens are parse errors (G9, G11).
  - TEXT and NOTE lines cannot fail (G11).

Normative source: specs/LANGUAGE.md (G1, G3, G4, G9, G11).
"""

import re
import sys

X_N = re.compile(r"^x[0-9]+$")


def parse_line(line):
    """Return an error message string for a line, or None if it parses.

    `line` is the full line with trailing whitespace stripped. Leading
    indentation is still present (checked for tabs; otherwise it is
    stripped for line-kind dispatch). A line may carry several widget
    items — a row (G8) — and xN may appear mid-line (G9).
    """
    # G1: tab anywhere in leading whitespace of a content line = error.
    leading = line[: len(line) - len(line.lstrip())]
    if "\t" in leading:
        return "tab in leading whitespace"

    rest = line.strip()
    if not rest:
        return None  # blank — ignored (G1)
    if rest[0] == "#":
        return None  # NOTE — cannot fail (G2, G11)
    if rest[0] not in "[(":
        return None  # TEXT — cannot fail (G2, G11)

    # One or more widget items on this line (rows, G8).
    while rest:
        if rest[0] not in "[(":
            return "stray content after widget"

        # G4: leaf form — [LABEL](...)
        if rest[0] == "[":
            end = rest.find("]")
            if end < 0:
                return "missing `]`"
            rest = rest[end + 1 :].lstrip()
            if not rest or rest[0] != "(":
                return "`]` not followed by `(`"

        # Shared tail: (TYPE[:VARIANT] ATTRS)  — G3, G5
        rest = rest[1:]  # drop the opening `(`
        close = rest.find(")")
        if close < 0:
            return "missing `)`"
        inner = rest[:close]
        rest = rest[close + 1 :]

        type_token = inner.split(None, 1)[0] if inner.strip() else ""
        if not type_token:
            return "empty TYPE"
        if type_token.startswith(":"):
            return "TYPE starts with `:`"
        # VARIANT = substring after the first `:` of the type token (G3);
        # no further checks by design.

        # G9: an optional xN token may follow the item (mid-line allowed).
        rest = rest.lstrip()
        if rest:
            parts = rest.split(None, 1)
            first = parts[0]
            if first[0] == "x" and X_N.match(first):
                if int(first[1:]) < 1:
                    return "`x0`"
                rest = parts[1].lstrip() if len(parts) > 1 else ""
    return None


def check_file(path):
    """Return (errors, fatal) — errors: list of "<path>:<line>: ..." strings.

    fatal is True when the file itself could not be read (exit 1); parse
    errors are non-fatal per-file but still fail the run (exit 2).
    """
    try:
        with open(path, encoding="utf-8") as f:
            text = f.read()
    except OSError as exc:
        return [f"{path}: cannot read: {exc.strerror or exc}"], True

    if text.startswith("\ufeff"):
        text = text[1:]  # G1: leading BOM ignored

    errors = []
    for lineno, raw in enumerate(text.splitlines(), 1):
        line = raw.rstrip()  # trailing whitespace ignored (G1)
        err = parse_line(line)
        if err:
            errors.append(f"{path}:{lineno}: parse error: {err}")
    return errors, False


def main(argv):
    if not argv:
        print(f"usage: {sys.argv[0]} <file.layout.txt> [...]", file=sys.stderr)
        return 1

    fatal = False
    all_ok = True
    for path in argv:
        errors, is_fatal = check_file(path)
        if errors:
            all_ok = False
            fatal = fatal or is_fatal
            for err in errors:
                print(err, file=sys.stderr)

    if fatal:
        return 1
    if not all_ok:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
