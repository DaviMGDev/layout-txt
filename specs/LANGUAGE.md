---
type: language
title: "LAYOUT.txt — Language Reference"
description: "The normative grammar and semantics of LAYOUT.txt, the plain-text UI structure format"
created: 2026-08-08
updated: 2026-08-08
---

# LAYOUT.txt — Language Reference

The normative reference for LAYOUT.txt: a minimal plain-text format for
specifying UI structure at wireframe level. Humans read it; AI agents
implement from it and verify against it. DESIGN.md owns visuals and tokens;
LAYOUT.txt owns structure. Vocabulary is free-form; the grammar is closed.

## Quick reference

```
# note (line above a widget = attached to it)

bare line                 → text widget (heading, caption, paragraph)

[Label](type)             → leaf widget
[Label](type:variant)     → leaf with variant (e.g. button:primary)
[Label](type attr=v)      → leaf with opaque attrs (never parsed)
[Docs](link https://x)    → attrs carry anything: [Revenue](graph data=monthly)

(type)                    → group; children indented under it
(type:variant attrs)      → group with variant/attrs; no children = label-less leaf

same line = side-by-side  → row (layout hint, never verified)
new line   = stacked      → column (default)

[chip](tag) x5            → repeat the preceding item 5 times
(card) x3                 → repeat the whole subtree 3 times

login.layout.txt          → one file = one screen; stem = screen name
LAYOUT.txt                → single-file form (static sites, one-screen apps)
auth/login.layout.txt     → crowded dirs: subfolders keep the file pattern
```

## Scope

LAYOUT.txt specifies **structure**: widgets, hierarchy, order, labels,
variants, annotations. It deliberately does not express:

- **Behavior** — events, navigation, data logic, conditionals. (That was
  InterSpec's weight; this format is the wireframe, not the program.)
- **Visuals** — colors, spacing, typography. Those belong in DESIGN.md.
- **Vocabulary enforcement** — any widget type is legal; unknown types are
  informational, never errors.

Anything the grammar cannot express is written as a `#` note. Incompleteness
is a feature: the escape hatch is prose, not grammar growth.

## Grammar

### G1 — Text and trivia

UTF-8 plain text, parsed line by line. Blank lines and trailing whitespace
are ignored. Indentation counts leading spaces only; a tab anywhere in
leading whitespace is a parse error. A leading BOM is ignored.

### G2 — Line kinds

After stripping indentation, each line is exactly one of:

| Kind | Starts with | Meaning |
|------|-------------|---------|
| NOTE | `#` | annotation for humans/agents; never a widget |
| WIDGET | `[` or `(` | a widget (leaf or container) |
| TEXT | anything else | a text widget: type `text` by convention, label = the trimmed line |

### G3 — Token grammar (shared by both shapes)

`TYPE[:VARIANT] ATTRS`

- **TYPE** — the first whitespace-delimited token; non-empty; must not begin
  with `:`. Case-sensitive; convention: lowercase kebab-case.
- **VARIANT** — the substring after the first `:` of the type token; absent
  if there is no colon.
- **ATTRS** — everything from the first whitespace after the type token up
  to the closing `)`, trimmed. Verbatim, opaque, never parsed, never
  verified; must not contain `)`.

### G4 — Leaf

`[LABEL](TYPE[:VARIANT] ATTRS)`

LABEL is everything up to the first `]` (any character except `]`; a needed
`]` goes into a note instead). After the `]`, optional whitespace, then `(`.
Empty labels are legal (`[](image cover.webp)`); convention prefers the
paren form `(image cover.webp)`.

### G5 — Container

`(TYPE[:VARIANT] ATTRS)`

With one or more indented widget children = a **group**. With none = a
**label-less leaf** (the "empty group" is exactly this). No depth limit;
single-child groups are legal.

### G6 — Hierarchy

A widget line's parent is the most recent preceding widget line (skipping
notes and blanks) with strictly smaller indentation. Children of a
multi-item line attach to the **last item** on that line. A node's children
are the following consecutive lines with strictly greater indentation, until
a line with indentation ≤ the parent's.

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
group's own line it repeats the whole subtree N times; children are written
once, indented once beneath that line.

- `x0` is a parse error (absence is said in a note).
- `x1` is a legal no-op.
- Repetition copies identical structure only; varying content is written out.

### G10 — Notes

A note attaches to the immediately following widget line (its first item if
a row); stacked notes attach together. Notes before the first widget are
screen-level meta. Note indentation is irrelevant. Note text is never
verified. `#` is special only as the first non-space character of a line.

### G11 — Invalid input

A WIDGET line that fails to parse (missing `]`, `]` not followed by `(`,
missing `)`, empty TYPE, TYPE starting with `:`, stray non-`xN` junk after a
completed widget) is a **parse error** for the whole file. TEXT and NOTE
lines cannot fail. Prose that starts with `(` parses as an unknown-type leaf
and is reported as INFO only (e.g. `(in progress)` → type `in`).

### G12 — Screens and naming

Top-level lines are children of an implicit screen node. One file = one
screen. The filename is the screen name (`login.layout.txt` → "Login",
title-cased by convention). `LAYOUT.txt` is the canonical single-file name.
No headers, no imports, no include mechanism.

## Semantics

- **Widget** — an element the screen contains. **Label** = the
  human-visible text (what people verify against: "is there a Sign in
  button?"). **Type** = the kind (conventionally lowercase kebab-case).
  **Variant** = style or state (`button:primary`, `card:compact`).
  **Attrs** = opaque parameters passed to the implementer (`placeholder=…`,
  `data=…`, URLs).
- **Text widgets** — bare lines are headings, captions, and paragraphs.
  They are structure: presence, order, and label are verified.
- **Groups** — containment. Nesting = hierarchy; depth is unlimited.
- **Repetition** — identical copies. `xN` never hides differing content.
- **Notes** — implementer guidance. Positional attachment (line above the
  widget) gives them a target without IDs or labels.
- **States** — use `:variant` for states you want machine-checked
  (`button:primary`); an attr like `disabled` is a hint, not a check.
- **Exotic widgets** — any type works, always. `[Revenue](graph data=monthly)`
  is a `graph` widget with attrs `data=monthly`. The first-token rule means
  new widgets never require a language change.
- **Lenient for humans, strict for agents** — unmatched lines are notes for
  humans; malformed widget lines are errors for parsers. A typo'd marker
  (`[Save](buton)`) parses fine but shows up in the verifier's
  informational report ("unknown type `buton`").

## Recommended vocabulary

The format owns shapes, not vocabulary. These 15 types are the *minimal
universal core* — documented convention, never enforced. Agents default to
consistent mappings for them; the verifier may whisper typo suggestions
("`buton` — did you mean `button`?") as INFO. Everything else is free-form.

| Group | Types |
|-------|-------|
| Atoms | `text`, `button`, `input`, `link`, `image`, `icon`, `divider`, `spacer` |
| Containers | `row`, `column`, `grid`, `card`, `form` |
| Form controls | `checkbox`, `select` |

Rule of thumb for admission: *does every app, in any domain, have this
widget?* `avatar` fails (many apps have none); `divider` passes (every
screen has one, and it is a structural fact, not decoration). Candidates
for future inclusion: `textarea`, `radio`.

## File organization

| Case | Convention |
|------|-----------|
| Static website | one `LAYOUT.txt` |
| Multi-page app | `<page>.layout.txt`, flat |
| Crowded app directory | domain subfolders keep the pattern: `auth/login.layout.txt` |

Screen identity lives in the **file stem**, never the folder path — folders
are pure grouping and can be introduced or moved without touching files or
cross-references. There is no index file and no registry: the filesystem is
the index. Screen inventory for agents = glob `LAYOUT.txt` / `*.layout.txt`
(flat) or `**/*.layout.txt` (folders). Cross-screen references use the
target file stem by convention (`[Settings](link settings)` →
`settings.layout.txt`); they are unvalidated in v1.

## Verification contract

See SPEC.md §Conformance. In short: parse errors are ERRORs; structure
(type, variant, label, order, counts) is matched recursively against the
agent-extracted app tree; unknowns, extras, attrs, and notes are INFO;
duplicates and unverifiable variants are WARNINGs; pass iff no ERROR.

## Worked examples

### `login.layout.txt` — screen with group, variants, attrs, rows, repetition

```
# Login screen — LAYOUT v1
# Meta: loading/error states are out of scope; annotate here when they matter.

Welcome back
Please sign in to continue

(form)
  [Email](input placeholder=you@example.com)
  [Password](input secure)
  # the divider separates the fields from the actions
  (divider)
  [Remember me](checkbox) [Forgot?](link forgot)
  [Sign in](button:primary full-width)
  [Create account](button:secondary) [Use demo](button:ghost)
# footer links are deliberately outside the form
(divider)
(link-row) x2
  [Docs](link https://example.com) [Help (FAQ)](link faq)
```

### `card-grid.layout.txt` — repetition, label-less leaves, deep nesting

```
# Card grid — LAYOUT v1
# Meta: column count is a hint for DESIGN.md; cards are listed in reading order.

Browse catalog
# primary feed — 6 identical compact cards
(grid cols=3)
  (card:compact) x6
    [](image cover.webp)
    [Title](text) [Price](text:emphasis)
    [Detail](text two-line clamp)
    (divider)
    [★](icon) x5 [Add](button:primary small)
  (spacer) x1
(divider)
(footer)
  [Privacy](link privacy) [Terms](link terms)
```

### `LAYOUT.txt` — static site shell (single file)

```
# Company site — LAYOUT v1
# All pages share this shell; per-page content lives in the content layer.

(header)
  [Logo](image logo.svg) [Home](link) [About](link) [Contact](link)
(hero)
  [Headline](text)
  [Subhead](text)
  [Get started](button:primary) [Learn more](button:ghost)
(sections)
  (card) x3
    [Title](text)
    [Body](text)
(footer)
  [Privacy](link privacy) [Terms](link terms)
```
