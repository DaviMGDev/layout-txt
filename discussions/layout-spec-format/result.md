# User currently specs UI/UX with InterSpec (.is files) + DESIGN.md (design tokens), feels InterSpec is overkill for their workflow, and proposes replacing it with a much simpler text format — LAYOUT.md / STRUCTURE.md or even LAYOUT.txt — where widgets are marked inline with markdown-link-style syntax: [label](button), [placeholder](input). Wants opinion and suggestions; knows they need to define a simple, flexible format for interface structure. — closed
Date: 2026-08-08 · snapshots: 10

## Topic
User currently specs UI/UX with InterSpec (.is files) + DESIGN.md (design tokens), feels InterSpec is overkill for their workflow, and proposes replacing it with a much simpler text format — LAYOUT.md / STRUCTURE.md or even LAYOUT.txt — where widgets are marked inline with markdown-link-style syntax: [label](button), [placeholder](input). Wants opinion and suggestions; knows they need to define a simple, flexible format for interface structure.

## Timeline
**[2026-08-08 22:36]** (Snapshot 1, entry)
- idea: replace InterSpec at the structure layer with a much simpler text format — LAYOUT.md / STRUCTURE.md / LAYOUT.txt — widgets marked inline with markdown-link-style syntax ([label](button), [placeholder](input))
- arg: InterSpec's real power is behavioral (state, events, navigation, reactivity); structure-only specs pay for ~10% of its feature set
- Q1 (value judgment): filename/format home — LAYOUT.md vs STRUCTURE.md vs LAYOUT.txt — open
- Q2 (design tension): how to disambiguate [label](type) markers from real markdown links — [Save](button) vs [Docs](https://…) are visually identical — open
- Q3 (design tension): grammar scope — nesting (card > title/input/buttons), repetition (grid of 5 cards), variants/states (primary, disabled) in linear text — open
- Q4 (value judgment): does the format express behavior (events, nav, conditionals) or pure static structure — open
- Q5 (value judgment): primary consumer — human-only communication artifact vs agent-consumed (implementation/verification) — open
- insight: the inline widget marker is the easy part; nesting + repetition is the hard 10% where formats either die or bloat into mini-InterSpec
- insight: .txt variant escapes markdown-link collision but loses headings/lists/rendering; .md gives structure tools but collides with real links — a prefix convention (e.g. [Save](@button)) is a cheaper fix than fleeing markdown
- insight: precedent — Markdoc/MDX do "markdown + inline custom component markers" for content sites; nobody does it for app UI structure
- tension: "kind of flexible" is precisely the requirement that kills simplicity — needs an explicit scope decision

**[2026-08-08 22:39]** (Snapshot 2, message)
- A5: consumer = BOTH — humans read, agents implement & verify — the format needs deterministic structure, not just prose
- A4: scope = "whatever makes sense to be present in a prototype/wireframe" — widgets, arrangement, hierarchy, labels, variants/states, annotations; NOT events/navigation/data logic
- insight: the format defines NO vocabulary — widget types reference DESIGN.md's components ([Save](button:primary) names a token that already exists); verification falls out: unknown marker type = spec error, built DOM must match markers — a referencing layer, not a self-contained language
- insight: incompleteness as a feature — escape hatches ("if the format fights you, write a prose sentence") are OK because humans fill holes; the real anti-bloat mechanism
- insight: same-line = row, new-line = column is a natural ordering rule; markdown tables can express grids natively
- insight: containers are unavoidable — multi-widget repetition (grid of cards) requires named groups
- Q6 (design tension): container/nesting mechanism — fence blocks, indented trees, inline brackets, or none — open
- Q7 (unexplored): repetition syntax (x3 / list items) — open
- Q8 (unexplored): variant/state syntax ([label](type:variant) vs [label](type disabled)) — open
- Q18 (design tension): verification mechanics — how agents verify against the layout file; candidate: marker types must exist in DESIGN.md components; DOM must match presence/order/hierarchy — open
- Q19 (unexplored): per-screen files vs one file — open

**[2026-08-08 22:42]** (Snapshot 3, message)
- arg: user rejects the .md default — "we really need to use .md for specification formats? why not use txt for this one? I don't like using code blocks for this" — the .txt direction is preferred
- idea: indented trees (option B) tentatively preferred ("maybe I liked B?") — code fences (option A) rejected as container mechanism
- insight: the user's two objections (code fences; markdown link collision) BOTH evaporate in .txt — the preference is coherent, not random: a format that defines everything itself, inherits nothing
- insight: the extension decides what is inherited — .md = inherit markdown semantics + rendering, fight collisions and fence noise; .txt = define 100% of the grammar, gain monospace freedom (ASCII sketches become legal), lose rendering
- insight: lenient parsing — "anything that isn't a widget marker is a note" — removes the need for any comment syntax (#, //); Fountain precedent (unmatched lines = action/description); typos silently become notes (cost of leniency, but aligns with incompleteness-as-feature)
- arg: the .md argument is mostly ecosystem inertia + heading rendering; DESIGN.md/MKF/OKF are markdown because they're documents/token files, not structure specs
- Q9 (design tension): grammar density — strict (all prose must be marked) vs lenient (unmatched lines = notes) — open
- Q10 (unexplored): ASCII sketch blocks as allowed annotation — possible txt-only superpower — open
- Q11 (unexplored): type-first syntax (input: Email) vs label-first ([Email](input)) — open

**[2026-08-08 22:56]** (Snapshot 4, message)
- A1: file home locked — LAYOUT.txt (plain text, own grammar, no markdown semantics)
- idea: notes carry a minimal identifying mark (e.g. # prefix) — user's middle path between fully lenient and fully strict ("prose is supposed to be used to help, add at least something to identify each one"); notes also serve the implementer; marker char undecided
- Q12 (value judgment): note marker character — # vs ; vs // vs other — open
- Q13 (unexplored): notes attachment — position rule (note directly above a widget = refers to it)? — open
- Q14 (design tension): vocabulary validation — marker types validated against DESIGN.md components (unknown = warning/error) vs free-form convention — open
- Q15 (design tension): repetition placement — 3x (card) prefix vs (card) x3 suffix — open
- Q16 (unexplored): container variants ((card:compact)) — symmetry leaf=[] group=() — open
- Q17 (unexplored): real links as widget type ([Docs](link https://…)) — open
- insight: the two-shape grammar (leaf [label](type) / group (type)) may be sufficient for wireframe scope
- insight: strict-enough for agents, loose enough for humans — a single-char marker keeps the file parseable without ceremony

**[2026-08-08 22:59]** (Snapshot 5, message)
- A12: note marker = # (locked)
- A14: widget vocabulary = FREE-FORM convention, NOT validated against DESIGN.md (user overrode the validation recommendation) — verification becomes structure-only; vocabulary is a soft convention; layout-first workflow is a legitimate reason (sketches often lead the design system)
- A8: variant syntax = colon [x](type:variant) — space-form is incompatible with free-form vocabulary (ambiguous parsing), separate-bracket adds a third grammar shape
- idea: first-token parse rule — type = first token, optional :variant after the first colon, rest of the parens = opaque passthrough attributes ([Docs](link https://example.com) falls out with zero extra grammar)
- arg: space-separated variants would reintroduce a closed vocabulary through the back door (ambiguous parse: type "button primary" vs type "button" + variant) — incompatible with the free-form choice
- Q15 (design tension): repetition placement — 3x (card) vs (card) x3 — open
- Q19 (design tension): file organization — one LAYOUT.txt per screen/feature vs a single file — open
- Q16 (unexplored): container variants — (card:compact) via the same colon rule — likely yes, unconfirmed — open
- Q18 (design tension): verification mechanics detail — structure-only checks (presence, order, hierarchy, labels) + informational vocabulary report — direction set — open
- Q17 (unexplored): real links as widgets — works via the passthrough rule — open
- Q20 (unexplored): multi-screen — how multiple screens/features relate in files — open
- insight: the vocabulary decision constrains the syntax decision — free-form ⇒ colon variants
- insight: two shapes ([label](type), (type)) + first-token rule + # notes + indentation covers the wireframe scope; grammar now ~7 rules
- insight: verification = structural (what/where/how many); vocabulary = soft convention

**[2026-08-08 23:20]** (Snapshot 6, message)
- idea: convergence round via the thinker consultation — close ALL open and future questions, produce the final proposal, revisit the syntax question ([]() was just the first idea), search inspirations
- insight: inspirations researched — ASCIIwire (markdown-headings-as-hierarchy), markdown-ui (fenced type-first), Fountain (lenient parsing), Markdoc/MDX (inline component markers for content), ASCII box-drawing tools; label-first []() survived the comparison against all of them
- arg: syntax-family verdict — label-first [Label](type:variant attrs) wins on read-speed (label first = what people verify against: "is there a Sign in button?"), determinism for tiny parsers, and natural fit in plain .txt
- arg: type-first was the only serious challenger (nice left-aligned type column) but reads backwards for humans and needs colon-quoting rules; heading-based and fenced forms were pre-rejected (no-markdown/no-fence constraints); box-drawing is visual but not semantic; Fountain-lenient alone is too weak for verification
- A3: grammar locked — 12 rules: line kinds disjoint by first char (# = NOTE; [ or ( = WIDGET; else = TEXT text-widget, label = trimmed line); leaf [LABEL](TYPE[:VARIANT] ATTRS) with label = up to first ], type = first token, variant = after first colon, attrs = opaque passthrough (never parsed/verified, must not contain )); container (TYPE[:VARIANT] ATTRS) with indented children = group, without = label-less leaf; hierarchy by indentation (multi-item row children attach to the LAST item); rows: same line = row (layout hint only, never verified) — (row)/(column)/(grid) = convention types; xN repetition suffix; notes attach to following widget line; static text = text widgets verified by label; per-screen files
- A7: repetition = xN suffix after any item (repeats the immediately preceding item; on a group's own line, the whole subtree); x0 = parse error, x1 = legal no-op
- A6: containers locked — (type) line + indented children; no depth limit; empty group = label-less leaf
- A13: notes attach to the immediately following widget line; notes before the first widget = screen-level meta; note indent irrelevant; never verified
- A18: verifier locked — parse errors = file-level ERROR (stop); recursive structural subsequence match over the agent-extracted app tree (type, variant, label, order, counts); unknown types & unmatched app nodes = INFO; duplicates & unverifiable variants = WARNING; pass iff no ERROR; exit codes 0/1/2; a few hundred lines, no dependencies; attrs and notes never compared
- A19: files locked — one screen per file: <screen>.layout.txt; single-screen projects may use LAYOUT.txt; filename = screen name; no index/imports
- A20: cross-screen references by filename convention, unvalidated in v1
- A2: link collision closed — the markdown-link shape reappears only if a tool renders the file as markdown; never rename it .md
- A16: container variants via the same colon rule — variants/attrs symmetric for leaves and containers
- A17: 'link' is a convention type, target = opaque attr; no first-class treatment
- A11: label-first kept after the full family comparison
- A15: repetition placement answered — suffix, not prefix (counts attach backward; no new line-start kind)
- Q10 (unexplored): ASCII sketches — answered: .txt monospace freedom makes them legal; not a grammar feature
- decision: edge cases closed — ']' in labels forbidden (label = up to first ]), '(' in labels OK; ')' in attrs inexpressible (reword or note); tabs in indentation = parse error; trailing whitespace ignored; UTF-8 labels allowed; prose starting with '(' parses as unknown-type leaf → INFO; malformed widget lines = file parse errors
- tension: the verifier checks the agent-extracted app tree, not the app itself (accepted residual soft spot)
- insight: grammar complete at 12 rules; incompleteness-as-feature is the escape hatch; attrs and notes are deliberately never verified

**[2026-08-08 23:24]** (Snapshot 7, message)
- Q21 (design tension): catalog rigidity — should LAYOUT.txt have a catalog of builtin components, or is component usage loose/free? (user's example: [graph](graph data) — exotic widgets like graphs; the syntax would already work — the question is the rigidity of the vocabulary) — open
- Q22 (unexplored): where the recommended vocabulary lives (format spec doc section; verifier typo-whisper INFO) and whether it is global vs per-project — open
- arg: InterSpec's CATALOG.md is normative (rigid, must-know builtins, new components need language-level definitions) — that rigidity was part of the felt weight; a growing catalog is the bloat the format exists to escape
- arg: DESIGN.md precedent — "Recommended Token Names (Non-Normative)": guidance without validation; the same pattern applies to LAYOUT widget types
- insight: the format owns shapes, not vocabulary (thinker soft spot #1, accepted); catalog-as-convention stabilizes agent mappings and enables typo-suggestion INFO ("buton" → button?) without enforcement
- insight: boundary rule — grammar closed, vocabulary open, catalog = suggestion box
- insight: exotic widgets work via passthrough attrs ([Revenue](graph data=monthly) — type graph, attrs opaque); [graph](graph data) already parses in the current grammar — no language change needed
- idea: three-tier model — rigid grammar, loose vocabulary, non-normative recommended core; options: A minimal-universal-core vs B no-core-at-all vs C rich catalog ~25+

**[2026-08-08 23:28]** (Snapshot 8, message)
- A21: catalog = Option A — minimal universal core (15 types draft: atoms text/button/input/link/image/icon/divider/spacer; containers row/column/grid/card/form; controls checkbox/select), convention-only, doubles as the verifier's typo dictionary
- arg: rich catalog (~25+) rejected — bloat; no-core rejected — no anchor for agent mappings
- Q23 (design tension): multi-page app organization — multiple LAYOUT.txt in subfolders per page vs one single LAYOUT.txt for everything vs LAYOUT.<page>.txt prefix naming — user re-opened (convergence already closed per-screen files) — open
- Q24 (unexplored): shared blocks across pages (header/nav on every screen) — no import mechanism (rejected); convention = duplicate + note, or shared.layout.txt reference by note; per-file self-containment keeps verification per-page — open
- arg: filename order mirrors the label-first philosophy — screen name first ([label](type) = label first; login.layout.txt = screen first, kind after); the prefix form groups layouts in listings but buries the screen name
- arg: scale-based tiers — 1 screen → LAYOUT.txt; a few → flat *.layout.txt; many/feature-scale → folder per page with uniform LAYOUT.txt (folder = screen name); invariant: one file per screen, screen name recoverable, glob-able, no index file
- insight: the filesystem is the index — glob replaces any registry/index file
- insight: screen inventory for agents = glob *.layout.txt / **/LAYOUT.txt
- insight: duplication of shared blocks is acceptable at wireframe level — each file stays self-contained and independently verifiable; notes point to the source of truth; imports were explicitly rejected (ceremony)

**[2026-08-08 23:30]** (Snapshot 9, message)
- A23 (refined): user's axis — <page>.layout.txt for multi-page apps AND a single LAYOUT.txt for static websites; a better axis than scale: template-driven (static/content sites) vs screen-driven (apps); accepted with a distinctness refinement
- idea: distinctness rule — when a page within a template-driven site becomes genuinely distinct (e.g. a contact page with a form), split it into its own file; mixed usage is legal (LAYOUT.txt + contact.layout.txt side by side)
- insight: "static vs app" is really "template-driven vs screen-driven" — a static site's wireframe IS the template (content lives in the content layer); apps have genuinely distinct screens; the user's instinct validated
- insight: filename order mirrors the label-first philosophy — screen name leads; LAYOUT.<page>.txt prefix vs <page>.layout.txt suffix: equivalent globs, but the suffix keeps the human-searched name first
- arg: the one-file-one-screen invariant is relaxed to one-file-per-distinct-structure for template-driven sites, with the split-off rule preserving per-page verification where it matters
- Q25 (design tension): for template-driven sites with >1 template — one LAYOUT.txt with note-marked sections (# Template: home) vs one file per template (home.layout.txt) — open
- Q24 (unexplored): shared blocks across pages — duplicate + note convention — open

**[2026-08-08 23:35]** (Snapshot 10, message)
- A23: file organization finalized — (1) static websites → one single LAYOUT.txt; (2) multi-page apps → <page>.layout.txt flat; (3) crowded app directory → domain subfolders that KEEP the <page>.layout.txt pattern (auth/login.layout.txt, auth/signup.layout.txt). Screen name is always the file stem; folders are pure grouping, never rename the file; no index/registry; glob = inventory (**/*.layout.txt); cross-references by stem. (User simplified my three-tier + template concept away — "found it confusing")
- A25: template concept removed — static → one file, app → per-page; no note-marked template sections needed
- insight: screen identity lives in the file stem, never the folder path
- insight: simplification wins — the user's two-rule model replaced my three-tier + template idea; template-driven vs screen-driven collapsed into "static → one file; app → per-page" without losing anything (content-driven sites genuinely have one shell)
- Q24 (unexplored): shared-block duplication convention (duplicate + note) — deferred (tentative, not locked)
- Q26 (unexplored): exact composition of the 15-type core list — deferred (draft proposed, adjustable)
- next step: fold catalog + organization decisions into the final spec document

## Final state
### Facts & constraints
- LAYOUT.txt v1 locked: grammar (12 rules), structural verifier, free-form vocabulary, minimal universal core (15 types, draft composition), boundary rule — grammar closed, vocabulary open, catalog = suggestion box
- Final organization model (user's): static website → single LAYOUT.txt; multi-page app → <page>.layout.txt flat; crowded app dir → domain subfolders keeping <page>.layout.txt naming; screen name = file stem always; folders never rename files
- Consumer: humans read, agents implement & verify; scope: wireframe-level structure only, no behavior

### Priorities
- Simplicity / minimal grammar (anti-bloat) — simplification wins over concept richness
- No ceremony: filesystem is the index; glob = inventory
- Screen-name-first consistency in filenames (label-first philosophy)

### Decisions
- Format: LAYOUT.txt v1 — grammar, verifier, naming as locked in Snapshot 6 (LOCKED)
- Vocabulary: free-form + minimal universal core (15 types, draft composition, adjustable) (LOCKED)
- Boundary rule: grammar closed, vocabulary open, catalog = suggestion box (LOCKED)
- FILE ORGANIZATION (final, user's model): static website → single LAYOUT.txt; multi-page app → <page>.layout.txt flat; crowded app dir → domain subfolders keeping <page>.layout.txt naming (auth/login.layout.txt). Screen name = file stem always (folders never rename files). No index/registry; glob = inventory (**/*.layout.txt); cross-references by stem. (LOCKED)
- Shared-block duplication convention (duplicate + note) — TENTATIVE, not locked

### Questions
- Q1 (value judgment): filename/format home — answered: LAYOUT.txt
- Q2 (design tension): marker disambiguation from real markdown links — answered: moot — .txt has no markdown link semantics
- Q3 (design tension): grammar scope — nesting/repetition/variants in linear text — answered: 12-rule grammar (Snapshot 6)
- Q4 (value judgment): behavior in scope — answered: wireframe scope only, no behavior
- Q5 (value judgment): primary consumer — answered: both — humans read, agents implement & verify
- Q6 (design tension): container/nesting mechanism — answered: (type) line + indented children
- Q7 (unexplored): repetition syntax — answered: xN suffix
- Q8 (unexplored): variant/state syntax — answered: colon [x](type:variant)
- Q9 (design tension): grammar density — answered: middle path — # notes
- Q10 (unexplored): ASCII sketch blocks — answered: .txt monospace freedom makes them legal; not a grammar feature
- Q11 (unexplored): type-first vs label-first — answered: label-first
- Q12 (value judgment): note marker character — answered: #
- Q13 (unexplored): notes attachment — answered: notes attach to the following widget line
- Q14 (design tension): vocabulary validation vs free-form — answered: free-form convention
- Q15 (design tension): repetition placement — answered: suffix (xN after the item)
- Q16 (unexplored): container variants — answered: same colon rule, symmetric for leaves and containers
- Q17 (unexplored): real links as widget type — answered: passthrough attrs; 'link' is a convention type
- Q18 (design tension): verification mechanics — answered: structural verifier (subsequence match; INFO/WARNING/ERROR)
- Q19 (design tension): file organization — answered: per-screen <screen>.layout.txt; single-screen LAYOUT.txt (refined by Q23)
- Q20 (unexplored): multi-screen file relations — answered: cross-references by file stem, unvalidated v1
- Q21 (design tension): catalog rigidity — answered: minimal universal core (15 types), convention-only
- Q22 (unexplored): where the recommended vocabulary lives — answered: spec doc convention section; doubles as verifier typo dictionary
- Q23 (design tension): multi-page organization — answered: final model — static → single LAYOUT.txt; apps → <page>.layout.txt flat; crowded → domain subfolders keeping <page>.layout.txt naming
- Q24 (unexplored): shared-block duplication convention — deferred (tentative: duplicate + note)
- Q25 (design tension): >1 template handling — answered: template concept removed — static sites get a single LAYOUT.txt
- Q26 (unexplored): exact composition of the 15-type core list — deferred (draft proposed, adjustable)

### Rejected alternatives
- Code fences as containers; fully lenient parsing; vocabulary validated against DESIGN.md; space-separated variants; separate-bracket variants; type-first syntax; markdown-headings (ASCIIwire); box-drawing; fenced type-first (markdown-ui); Fountain-lenient alone; imports/index/registry; rich catalog ~25+; no-core-at-all
- LAYOUT.<page>.txt prefix naming (suffix keeps the human-searched name first)
- Template-driven three-tier model with note-marked template sections (user simplified it away)
- Subfolders renaming files (folders are pure grouping — rejected)

### Next steps
- Fold catalog + organization decisions into the final spec document — DONE after the discussion (specs/SPEC.md + specs/LANGUAGE.md in this repo)
- Validate the format on a real screen (e.g. login example implemented and verified end-to-end)
- Optional: package grammar + verifier as a small script or pi skill
- Optional later: cross-file validation (glob-based screen inventory, link target checks)
