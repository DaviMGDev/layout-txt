---
name: layout-txt
description: >-
  Write LAYOUT.txt files — the v1 plain-text UI structure spec (wireframe
  level). Convert a design brief or an existing UI/HTML/DOM into a valid
  LAYOUT.txt file: screen/file naming, widget decomposition, hierarchy via
  indentation, rows, variants vs attrs, xN repeats, notes, and a final parse
  check. Includes grammar quick-reference, full grammar reference, worked
  examples, and a dependency-free parse-check script. Structure only — no
  visuals, no behavior, no vocabulary enforcement.
---

# LAYOUT.txt writer

Applies to LAYOUT format **v1** — normative source:
`../../specs/LANGUAGE.md`; if they disagree, the spec wins. If the format
changes, update this skill before further use.

## The format in five things

1. One file = one screen; the filename is the screen name.
2. Indentation (spaces only) = nesting; order = structure.
3. `[LABEL](TYPE ATTRS)` = labeled widget; `(TYPE ATTRS)` = unlabeled
   widget/container; every type works.
4. Plain lines are visible text; `#` lines are annotations; widgets on one
   line are a row.
5. No tabs, no markdown, no behavior, no styling — when in doubt, use a note.

## Grammar quick-reference

- **Indent:** spaces only; children strictly more than parents (2 per
  level by convention); a leading tab anywhere = whole file invalid.
- **Leaf:** `[Label](type:variant attr=…)` — label = exact visible text up
  to the first `]`; after `]` must come `(`; type = first token,
  non-empty, not `:`-prefixed; attrs = up to the first `)`, opaque, never
  parsed, no `)` inside; nothing after `)` except `xN`.
- **Unlabeled:** `(type attrs)` — the `[]`-bracket form is legal but
  unidiomatic; prefer parens.
- **Container:** `(type attrs)` with indented children = group; without
  children = a bare (label-less) leaf.
- **Nesting:** a widget's parent = the nearest previous widget line with
  fewer leading spaces; children = following lines with more spaces, until
  a line with ≤ the parent's.
- **Rows:** widgets on one physical line = a row (layout hint, never
  verified); separate lines = stacked.
- **Repeat:** `xN` right after an item repeats exactly that item; on a
  container line it repeats the whole indented subtree (children written
  once). Identical items only; N ≥ 1 (`x0` = parse error; varying content
  is written out).
- **Notes:** `#` directly above a widget attaches to it (stacked notes
  attach together); notes before the first widget = screen-level meta;
  never verified.
- **Text:** any other line — but a line starting with `#`, `(`, or `[`
  parses as a note/widget/error, not text. Rephrase or write
  `[Text](text)`.
- **Invalid widget line** (missing `]`/`(`/`)`, empty or `:`-prefixed
  type, junk after `)`, tab indent) fails the **whole file**. Run
  `scripts/check_layout.py` to be sure.

## Workflow: from brief or UI/HTML to LAYOUT.txt

**Step 0 — Read context.** From the design brief, extract the screen's
*visible content only*. If DESIGN.md exists, skim it for widget-naming
conventions — never copy visual specs. If the input is HTML/DOM, keep it
open for Steps 2–3.

**Step 1 — Decide the screen and file home.**

- Single screen / static site → `LAYOUT.txt`.
- Multi-page app → one file per screen: `<stem>.layout.txt`; add domain
  subfolders only when the file list gets crowded (`auth/login.layout.txt`).
- Screen identity = file stem, never folder (`login.layout.txt` → screen
  "Login", title-cased by convention). Never two screens in one file;
  never split one screen across files.

**Step 2 — Inventory the content.** Walk the brief/DOM top-to-bottom then
left-to-right; list every distinct visible item: texts (headings,
captions, paragraphs), controls, links, images/icons, dividers, structural
groups (nav, cards, forms, lists, grids). Drop purely presentational
wrappers. For inputs: the field *label* is the label; placeholder/name/
type are attrs. For images/icons: label = visible/alt text when
content-bearing; decorative icons → unlabeled `(icon …)`. Collect behavior
(events, nav, state) into a scratch list, **then delete it** — it has no
home in this file. (Link URLs are fine as attrs: passthrough data, not
behavior.)

**Step 3 — Map to widget types.** Use the core vocabulary when it fits
(see DOM mapping below; prose/headings → `text`). Anything real that
doesn't fit → exotic type, which *always* works:
`[Revenue](graph data=monthly)`. Never invent a type to express behavior.

**Step 4 — Order and hierarchy.** Write top-level widgets in visual order.
Indent children with spaces, strictly more than their parent, siblings
aligned. One physical line = one row (left-to-right); separate lines =
stacked.

**Step 5 — Variant vs attr vs note.** Would a verifier assert it? →
`:variant` (`button:primary`, `input:error`). Does the implementer need a
parameter? → attr (`placeholder=…`, `href=…`, `data=…`; `disabled` as attr
is a *hint*, `:disabled` is a check). Is it an explanation? → `# note`.

**Step 6 — Apply `xN` only to identical repeats.** `[x](button) x4`
repeats that exact item; `(card) x3` on its own line repeats the whole
subtree. Only when label + type + variant + attrs are truly identical.
Varying content is always written out. Never `x0`.

**Step 7 — Note the inexpressible.** Anything structure can't carry goes
into a `#` line directly above the widget it explains; before the first
widget = screen-level meta. Missing content is noted, never fabricated.

**Step 8 — Self-check.** Run the checklist below, then
`python3 scripts/check_layout.py <file>` until it exits 0.

## DOM → type mapping

| HTML / DOM | LAYOUT.txt |
|---|---|
| `h1`–`h6`, `p` | `text` — bare line |
| `button` | `button` |
| `a[href]` | `link href=…` |
| `input` | `input` (label = field label) |
| `select` | `select` |
| `textarea` | `textarea` (exotic) |
| `img` | `image` |
| svg / icon font | `icon` |
| `form` | `form` |
| `div.card`, `article` | `card` |
| repeated identical `li` | `row`/`column` + `xN` (identical only) |
| `table` | `grid` |
| `nav` | `row`/`column` |
| `hr` | `divider` |
| presentational-only divs | **drop** |

## Common mistakes to unlearn

| # | Markdown/HTML habit | What LAYOUT.txt sees | Why it's wrong | Correct response |
|---|---|---|---|---|
| 1 | `# Welcome` as a heading | a NOTE — widget never exists | screen silently loses its title text | `Welcome` (bare text line); `#` is for annotations only |
| 2 | `[Docs](https://docs.example.com)` as a link | a WIDGET with TYPE `https://docs.example.com` | URL became the type; parses fine, semantics destroyed | `[Docs](link https://docs.example.com)` — URL is an attr |
| 3 | Tab indentation | whole-file parse error (G1) | one tab kills the file | spaces only, consistent (2/level) |
| 4 | Code fences ```…``` | fence lines become text widgets | literal `` ``` `` artifacts in the screen | never include fences; LAYOUT.txt *is* the plain-text format |
| 5 | `**Submit**`, `_Email_` | literal `**`/`_` in the label | verifier compares exact visible text | plain exact text: `Submit`, `Email` |
| 6 | Every DOM `div` → a container | over-nesting, empty structure | wrapper noise pollutes the hierarchy | drop presentational wrappers; containers only for structural groups |
| 7 | `[A](button) [B](button) x2` | `x2` repeats *only the immediately preceding item* → A B B | xN binds to the wrong item, or hides differing content | put xN directly after its item; identical items only |
| 8 | `[](image cover.webp)` | legal but noisy and unidiomatic | convention prefers the paren form | `(image cover.webp)` |
| 9 | Prose starting with `(` — `(in progress)` | parses as an exotic widget (TYPE `in`) | intended text never becomes text | rephrase, or force text: `[In progress](text)` |
| 10 | Label containing `]` — `[Save] edits](button)` | parse error: label ends at first `]` | file invalid | put the literal in a note or rephrase the label |
| 11 | Attr containing `)` — `placeholder=(optional)` | parse error: widget closes at first `)`, rest = stray junk | file invalid | rephrase: `placeholder=optional` |
| 12 | Behavior as structure — `[Cart](button onclick=…)`, "if logged in…" | attrs/notes are unverified hints; this file is never the place for behavior | events/state/nav pretend to be structure | keep them out; checked states only via `:variant`; flow goes to notes/DESIGN.md |
| 13 | Two screens in one file (`# Screen 2` + widgets) | all top-level lines = one implicit screen | screen identity broken | one file per screen; the stem names it |

## Before you finish

- [ ] No tabs anywhere in leading whitespace.
- [ ] Every `#` line is an annotation; every `[`/`(` line is a widget;
      every other line is text and does not start with `#`, `(`, or `[`.
- [ ] Labels are exact visible text; no `]` inside a label; no `)` inside
      attrs; nothing after `)` except `xN`.
- [ ] Children strictly more indented than parents; siblings aligned; no
      emptied-wrapper nesting.
- [ ] One physical line per row; separate lines stack.
- [ ] Variants only for checkable states; attrs only as implementer
      params; no events/nav/conditionals anywhere.
- [ ] `xN` only on identical items, N ≥ 1, attached to the item it repeats.
- [ ] One screen per file; filename = `LAYOUT.txt` or `<screen>.layout.txt`.
- [ ] Every brief item appears exactly once (or is noted as absent);
      nothing invented.
- [ ] `python3 scripts/check_layout.py <file>` exits 0.

## Scope boundaries

1. **No visuals** — colors, spacing, sizes, typography, tokens belong to
   DESIGN.md. If the brief is visual-heavy, ignore it for structure (or
   note `# visual specs left to DESIGN.md`).
2. **No behavior** — events, navigation flows, state transitions,
   conditionals, auth logic. States appear only as `:variant`
   (machine-checked) or attr *hints*; never as structure.
3. **No vocabulary enforcement** — never reject or "correct" unknown
   types; exotic types always work. The core vocabulary is advisorial
   convention only.
4. **No structural verification (V2)** — never compare an implementation
   or DOM against a LAYOUT.txt file. `scripts/check_layout.py` is
   parse-only (G11). Structural matching is a separate future tool.
5. **No cross-file validation** — no link-target checks, no registry
   generation, no index files. The filesystem is the index; cross-screen
   references are by stem convention, unvalidated in v1.
6. **No fabrication** — if the brief lacks content, note it, don't invent
   it.
7. **No other formats** — this skill writes LAYOUT.txt only; it does not
   edit DESIGN.md, generate code, or produce visuals/behavior docs.

## References

- `references/grammar.md` — full grammar restatement (v1); the spec wins
  on conflict.
- `examples/login.layout.txt`, `examples/card-grid.layout.txt`,
  `examples/LAYOUT.txt` — valid v1 files (verbatim copies of the spec's
  worked examples).
- `scripts/check_layout.py` — parse-only check (G11). Not the V2
  verifier.
