# LAYOUT.txt — Grammar Reference (skill restatement, v1)

**Restatement for standalone use.** This file restates the normative
grammar of LAYOUT format **v1**. Normative source:
`../../specs/LANGUAGE.md` (this repo) — **if they disagree, the spec
wins.** Design rationale:
`../../discussions/layout-spec-format/layout-txt-format.md`.

**Shared-update rule:** a LAYOUT format change → update `grammar.md`, the
examples in `examples/`, and `scripts/check_layout.py` together; adjust
`SKILL.md`'s quick-reference only if a headline rule changed; log the
change in `../../log.md` (skills log) and bump the version pin.

## Grammar

### G1 — Text and trivia

UTF-8 plain text, parsed line by line. Blank lines and trailing
whitespace are ignored. Indentation counts leading spaces only; a tab
anywhere in leading whitespace is a parse error (whitespace-only lines
are blank and ignored). A leading BOM is ignored.

### G2 — Line kinds

After stripping indentation, each line is exactly one of:

| Kind | Starts with | Meaning |
|------|-------------|---------|
| NOTE | `#` | annotation for humans/agents; never a widget |
| WIDGET | `[` or `(` | a widget (leaf or container) |
| TEXT | anything else | a text widget: type `text` by convention, label = the trimmed line |

### G3 — Token grammar (shared by both shapes)

`TYPE[:VARIANT] ATTRS`

- **TYPE** — the first whitespace-delimited token; non-empty; must not
  begin with `:`. Case-sensitive; convention: lowercase kebab-case.
- **VARIANT** — the substring after the first `:` of the type token;
  absent if there is no colon.
- **ATTRS** — everything from the first whitespace after the type token
  up to the closing `)`, trimmed. Verbatim, opaque, never parsed, never
  verified; must not contain `)`.

### G4 — Leaf

`[LABEL](TYPE[:VARIANT] ATTRS)`

LABEL is everything up to the first `]` (any character except `]`; a
needed `]` goes into a note instead). After the `]`, optional whitespace,
then `(`. Empty labels are legal (`[](image cover.webp)`); convention
prefers the paren form `(image cover.webp)`.

### G5 — Container

`(TYPE[:VARIANT] ATTRS)`

With one or more indented widget children = a **group**. With none = a
**label-less leaf** (the "empty group" is exactly this). No depth limit;
single-child groups are legal.

### G6 — Hierarchy

A widget line's parent is the most recent preceding widget line (skipping
notes and blanks) with strictly smaller indentation. Children of a
multi-item line attach to the **last item** on that line. A node's
children are the following consecutive lines with strictly greater
indentation, until a line with indentation ≤ the parent's.

### G7 — Order

Within a parent, widgets occur in file order. Order is structure and is
verified.

### G8 — Rows and columns

Widgets on one physical line = a row, left-to-right. Widgets on separate
lines = stacked. Rows are a layout **hint** — never a verifier concern.
`(row)`, `(column)`, `(grid)` are ordinary container types by convention:
a `(row)` whose children sit on separate lines is still laid out
side-by-side by the implementing agent.

### G9 — Repetition

A token `xN` (lowercase `x`, digits, N ≥ 1) after any widget item repeats
that item N times, applying to the immediately preceding item only. On a
group's own line it repeats the whole subtree N times; children are
written once, indented once beneath that line.

- `x0` is a parse error (absence is said in a note).
- `x1` is a legal no-op.
- Repetition copies identical structure only; varying content is written
  out.

### G10 — Notes

A note attaches to the immediately following widget line (its first item
if a row); stacked notes attach together. Notes before the first widget
are screen-level meta. Note indentation is irrelevant. Note text is never
verified. `#` is special only as the first non-space character of a line.

### G11 — Invalid input

A WIDGET line that fails to parse (missing `]`, `]` not followed by `(`,
missing `)`, empty TYPE, TYPE starting with `:`, stray non-`xN` junk after
a completed widget) is a **parse error** for the whole file. TEXT and
NOTE lines cannot fail. Prose that starts with `(` parses as an
unknown-type leaf and is reported as INFO only (e.g. `(in progress)` →
type `in`).

### G12 — Screens and naming

Top-level lines are children of an implicit screen node. One file = one
screen. The filename is the screen name (`login.layout.txt` → "Login",
title-cased by convention). `LAYOUT.txt` is the canonical single-file
name. No headers, no imports, no include mechanism.

## Semantics

- **Widget** — an element the screen contains. **Label** = the
  human-visible text (what people verify against: "is there a Sign in
  button?"). **Type** = the kind (conventionally lowercase kebab-case).
  **Variant** = style or state (`button:primary`, `card:compact`).
  **Attrs** = opaque parameters passed to the implementer
  (`placeholder=…`, `data=…`, URLs).
- **Text widgets** — bare lines are headings, captions, and paragraphs.
  They are structure: presence, order, and label are verified.
- **Groups** — containment. Nesting = hierarchy; depth is unlimited.
- **Repetition** — identical copies. `xN` never hides differing content.
- **Notes** — implementer guidance. Positional attachment (line above the
  widget) gives them a target without IDs or labels.
- **States** — use `:variant` for states you want machine-checked
  (`button:primary`); an attr like `disabled` is a hint, not a check.
- **Exotic widgets** — any type works, always. `[Revenue](graph
  data=monthly)` is a `graph` widget with attrs `data=monthly`. The
  first-token rule means new widgets never require a language change.
- **Lenient for humans, strict for agents** — unmatched lines are notes
  for humans; malformed widget lines are errors for parsers. A typo'd
  marker (`[Save](buton)`) parses fine but shows up in a verifier's
  informational report ("unknown type `buton`").

## Recommended vocabulary

The format owns shapes, not vocabulary. These 15 types are the *minimal
universal core* — documented convention, never enforced. Agents default
to consistent mappings for them; a verifier may whisper typo suggestions
("`buton` — did you mean `button`?") as INFO. Everything else is
free-form.

| Group | Types |
|-------|-------|
| Atoms | `text`, `button`, `input`, `link`, `image`, `icon`, `divider`, `spacer` |
| Containers | `row`, `column`, `grid`, `card`, `form` |
| Form controls | `checkbox`, `select` |

Admission rule: *does every app, in any domain, have this widget?*
`avatar` fails (many apps have none); `divider` passes (every screen has
one, and it is a structural fact, not decoration). Candidates for future
inclusion: `textarea`, `radio`.

## File organization

| Case | Convention |
|------|-----------|
| Static website | one `LAYOUT.txt` |
| Multi-page app | `<page>.layout.txt`, flat |
| Crowded app directory | domain subfolders keep the pattern: `auth/login.layout.txt` |

Screen identity lives in the **file stem**, never the folder path —
folders are pure grouping and can be introduced or moved without touching
files or cross-references. There is no index file and no registry: the
filesystem is the index. Screen inventory for agents = glob
`LAYOUT.txt` / `*.layout.txt` (flat) or `**/*.layout.txt` (folders).
Cross-screen references use the target file stem by convention
(`[Settings](link settings)` → `settings.layout.txt`); they are
unvalidated in v1.

## Verification contract (summary)

Parse errors are ERRORs; structure (type, variant, label, order, counts)
is matched recursively against the agent-extracted app tree; unknowns,
extras, attrs, and notes are INFO; duplicates and unverifiable variants
are WARNINGs; pass iff no ERROR. Exit codes: `0` pass / `1` fail / `2`
unparseable. This skill's `scripts/check_layout.py` implements the parse
layer only (G11); full structural matching is a separate future tool.
