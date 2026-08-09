# LAYOUT.txt — A Minimal UI Structure Format

**Date:** 2026-08-08

## Topic

Designing a minimal text format to replace InterSpec (`.is`) for wireframe-level UI structure specification. InterSpec is a full declarative UI language (state, events, navigation, reactivity) — powerful, but overkill when what gets written at spec time is "this screen has these things in this order." The discussion converged on **LAYOUT.txt**: a plain-text, markdown-free format with a tiny grammar, consumed by humans (reading) and AI agents (implementing and verifying), sitting next to DESIGN.md (which keeps owning visuals and tokens).

## Key Points

- InterSpec's real weight is behavioral (state, events, navigation); structure-only specs pay for ~10% of its feature set.
- The format is a **referencing layer**: it defines no vocabulary — widget types are free-form names that DESIGN.md catches up to by convention. Layout leads; the design system follows.
- `.txt` over `.md`: the extension decides what you inherit. Markdown brings collision (`[Save](button)` vs `[docs](https://…)`), code-fence noise, and rendering semantics. Plain text defines 100% of its own grammar — and its only historical defect (`[]()` looking like a markdown link) disappears.
- **Incompleteness is a feature**: anything the grammar can't express is written as a `#` note. Escape hatches, not grammar growth, are the anti-bloat mechanism.
- Verification is deliberately **structural**: presence, order, hierarchy, labels, counts. Unknown types, attrs, and notes never fail a build — they're informational.
- Inspirations researched: ASCIIwire (markdown-headings-as-hierarchy), markdown-ui (fenced type-first), Fountain (lenient parsing), Markdoc/MDX (inline component markers for content), ASCII box-drawing tools. Label-first `[]()` survived the comparison against all of them.

## Discussion

### Why InterSpec felt heavy

InterSpec's power is interaction logic: state, events, navigation, reactive watchers, viewport contracts. At wireframe level ("login screen: email, password, two buttons"), that machinery goes unused. The gap between prose and InterSpec is real, and a structure-only spec fits it. The user's original seed — markdown-link-style markers `[label](button)` — was validated: it's a universal mental model, reads naturally, and is trivially parseable by agents.

### The `.md` vs `.txt` fork

Early turns assumed markdown (ecosystem inertia: DESIGN.md, MKF, OKF are all markdown). The user pushed back: "we really need to use .md for specification formats?" The decisive reframe: the extension decides what you inherit. `.md` = inherit headings/lists/tables/rendering, fight link collisions and fence semantics. `.txt` = define everything, gain monospace freedom (ASCII sketches become legal), lose rendering. The user's two objections (code fences; markdown link collision) both evaporate in `.txt`, which made the direction coherent rather than random. Bonus: `.txt` signals "data, not docs" inside a markdown ecosystem.

### Syntax evolution

The grammar converged through several turns:

1. `[label](type)` — the seed. In `.txt` the link collision is gone; the shape survives.
2. **Notes** — a middle path between strict ("every prose line marked") and lenient ("unmatched lines are notes"): `#` prefix, with positional attachment (a note directly above a widget refers to it). Fountain-style leniency was the inspiration, tempered by the user's correct instinct that prose needs an identifier.
3. **Two shapes + one parse rule** — `[Label](type[:variant] attrs…)` for leaves, `(type[:variant])` for groups (indented children). The parse rule: first token = type, optional `:variant` after the first colon, everything else = opaque passthrough attrs. This made URLs and attributes fall out with zero extra grammar: `[Docs](link https://example.com)`.
4. **Free-form vocabulary** — user's explicit choice over DESIGN.md validation. Reconciled with "verify": verification checks structure; unknown types are informational. The layout-first workflow (sketches lead the design system) is a legitimate reason.
5. **Colon variants** — the only variant syntax compatible with free-form vocabulary (space-separated variants would require a closed type list; separate brackets add a third shape).
6. **Text lines** — the last real gap: wireframes contain headings and captions that aren't widgets. Closed by making bare non-`#` lines text widgets (verified by label). Line kinds are disjoint by first character: `#` = note, `[`/`(` = widget, anything else = text.
7. **Repetition** — `xN` suffix after any item (repeats only the immediately preceding item; on a group line, the whole subtree). Suffix chosen over prefix because counts attach backward and need no new line-start kind.
8. **Row rule** — same line = side-by-side, new line = stacked. Layout is a hint, never a verifier concern.

### The syntax-family showdown (final round)

Candidates compared: (a) label-first `[Label](type)`, (b) type-first `button: Save`, (c) markdown-headings (ASCIIwire), (d) ASCII box-drawing, (e) fenced type-first (markdown-ui), (f) Fountain-lenient. Axes: simplicity, human skimmability, typing speed, agent parseability, verifiability, expressiveness, txt-appropriateness, learnability.

Winner: **(a)**. The only candidate simultaneously fast for humans to read (label first = what people verify against: "is there a Sign in button?"), deterministic for tiny parsers, and natural in plain `.txt`. Type-first was the only serious challenger (nice left-aligned type column) but reads backwards for humans and needs colon-quoting rules. Heading-based and fenced forms were pre-rejected by the user's no-markdown/no-fence constraints; box-drawing is visual but not semantic; Fountain-lenient alone is too weak for verification.

### Verification design

"Humans read, agents implement and verify" + "free-form vocabulary" converge on a structural verifier: parse the spec (malformed widget lines = file-level ERROR), then a recursive subsequence match of spec nodes against the agent-extracted app tree (type, variant, label, order, counts). Unknown types and unmatched app nodes are INFO; duplicate matches and unverifiable variants are WARNING; pass iff no ERROR. A few hundred lines, no dependencies. Attrs and notes are never compared — deliberately.

### Deviant details (closed)

- `]` in labels: forbidden (label = up to the first `]`); needed brackets go in a note.
- `)` in attrs: inexpressible — reword or note. No escape/quote rules keeps the parser tiny.
- Empty groups: `(type)` without children is a label-less leaf — same token, role decided by children.
- Nesting: no depth limit; single-child groups allowed.
- `x0` is a parse error (absence is note-level); `x1` is a legal no-op.
- Tabs in indentation: parse error (indent = spaces only); trailing whitespace ignored; UTF-8 labels allowed.
- Prose that happens to start with `(`: parses as an unknown-type leaf → INFO only.
- File organization: one screen per file, `<screen>.layout.txt`; filename = screen name; no headers, no imports, no index.
- Cross-screen references: by filename convention, unvalidated in v1.

## Conclusions / Decisions

**The final proposal — LAYOUT v1.**

### Grammar

1. **Line kinds** — after stripping indentation, every line is exactly one of: `#` → NOTE; starts with `[` or `(` → WIDGET; anything else → TEXT (a text widget; label = the trimmed line).
2. **Leaf** — `[LABEL](TYPE[:VARIANT] ATTRS)`. Label = everything up to the first `]`. Type = first whitespace-delimited token. Variant = substring after the first `:`. Attrs = everything after the type token up to the closing `)` — verbatim, opaque, never parsed or verified; must not contain `)`.
3. **Container** — `(TYPE[:VARIANT] ATTRS)` with one or more indented widget children = a group; with none = a label-less leaf. No depth limit.
4. **Hierarchy** — a widget's parent = the most recent preceding widget line with strictly smaller indentation; children = following lines with strictly greater indentation.
5. **Order** — file order is structure and is verified.
6. **Rows** — widgets on one line = side-by-side; separate lines = stacked. Layout is a hint, never a verifier concern. `(row)`, `(column)`, `(grid)` are ordinary container types by convention.
7. **Repetition** — `xN` (N ≥ 1) after any item repeats only that item; on a group's own line it repeats the whole subtree (children written once, indented once).
8. **Notes** — attach to the immediately following widget line; notes before the first widget are screen-level meta. Never verified.
9. **Errors** — malformed widget lines (missing `]`, missing `)`, empty type, junk after a widget) are file-level parse errors. TEXT and NOTE lines cannot fail.
10. **Files** — one screen per file: `<screen>.layout.txt`; single-screen projects may use `LAYOUT.txt`. Filename = screen name (title-cased by convention).

### Verifier (v1)

Parse errors → ERROR (stop). Recursive structural match in file order: same type; same variant if declared (unverifiable variant → WARNING); same label if present; count absent → ≥ 1 match; count N → exactly N subtree matches. Unknown types, unmatched app nodes, attrs, notes → INFO. Duplicates → WARNING. Pass iff no ERROR. Exit codes: 0 pass / 1 fail / 2 unparseable.

### Worked example — `login.layout.txt`

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

### Residual soft spots (convention, not rule — by design)

1. Widget vocabulary is unregistered — unknown types are INFO, never errors.
2. Attrs are unverifiable (a wrong href passes) — verification is structural; use `:variant` for machine-checked states.
3. The verifier checks the agent-extracted app tree, not the app itself.
4. Layout is hint-only — a screen with everything present but badly arranged passes; visuals are DESIGN.md's deliverable.
5. `(type)` means leaf or group depending on children — author intent is unambiguous at write time.
6. `]` in labels and `)` in attrs are inexpressible — the note rule is the escape hatch.
7. The `[x](y)` markdown-link shape reappears only if a tool renders the file as markdown — never rename it `.md`.
8. Cross-file references and screen inventory are unvalidated in v1.

## Open Questions / Unresolved Threads

None — every question raised during the discussion (syntax family, repetition, static text, file organization, container variants, links, verification mechanics, edge cases, naming, plus the thinker's additional sub-questions) was closed with a decision. The residual soft spots above are intentional conventions, not open questions.

## Follow-ups

- Write a standalone format specification document (the reference the agent and humans both use).
- Validate the format on a real screen (e.g. the login example implemented and verified end-to-end).
- Optional: package the grammar + verifier as a small script or pi skill.
- Optional later: cross-file validation (glob-based screen inventory, link target checks).
