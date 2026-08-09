# LAYOUT.txt spec project

> A minimal plain-text format for specifying UI structure at wireframe
> level — humans read it, AI agents implement and verify it. This repo
> holds the specification, the example catalog, and the writer skill.

## Validation

There is no build system — this is a documentation/spec repo. The one
executable artifact is the LAYOUT parse checker (Python 3, stdlib only):

- **Check all examples**: `python3 skills/layout-txt/scripts/check_layout.py $(find examples -name '*.layout.txt' -o -name 'LAYOUT.txt')`
- **Exit codes**: `0` all valid · `2` parse error (G11) · `1` unreadable/usage
- **Checker contract**: parse rules only (G1–G12); deliberately does NOT
  check vocabulary, variant values, attrs content, notes, hierarchy
  depth, filenames, or cross-file references. See the script header.

Any new `.layout.txt` file added to `examples/` MUST pass the checker
(exit 0) before commit — the catalog's invariant is "every file valid".

## Testing

No test suite. Sanity checks agents should run after changing the checker
or the examples:

- Checker on all examples → exit 0.
- Negative fixtures (leading tab, `[Save](button)!`, `)` inside attrs,
  `x0`, empty TYPE) → exit 2; empty and notes-only files → exit 0.
- Skill validity (name/description rules): `cd ~/.pi/agent/skills/skill-creator && uv run scripts/validate.py <skill-dir>`

## Conventions

- **MKF compound nodes**: `specs/`, `skills/`, `examples/` are each a
  folder with an `index.md` (registry + reading order) and a `log.md`
  (activity log), all with YAML frontmatter (`type`, `title`,
  `description`, `created`, `updated`).
- **spec-md style**: `specs/SPEC.md` declares its own contract — the
  frontmatter `sections:` must list every `##` section; nothing appears
  undeclared. `specs/LANGUAGE.md` is the normative grammar (G1–G12).
- **Normative source**: `specs/LANGUAGE.md` wins on any conflict with
  restatements (skills, README, examples).
- **Verbatim copies**: canonical worked examples are copied byte-for-byte
  from `specs/LANGUAGE.md` into `skills/layout-txt/examples/` and
  `examples/screens/`. Never edit a copy in place — fix the spec first,
  then re-copy.
- **Version pins**: the format is v1; anything restating it (skills,
  docs) pins "v1". A format change requires updating grammar
  restatements, examples, and the checker together, then logging it.
- **Naming**: lowercase kebab-case for files, skills, and widget types.
- **Indentation**: 2 spaces; tabs are a parse error in LAYOUT files.

## Architecture

- **Pattern**: document hierarchy (spec monolith + normative reference +
  registries), not software.
- **Key directories**:
  - `specs/` — the specification: `SPEC.md` (context, decisions D1–D10,
    conformance contract V1–V4, versioning), `LANGUAGE.md` (normative
    grammar, semantics, vocabulary, worked examples), `index.md`, `log.md`
  - `examples/` — example catalog: `capabilities/` (12 files, one
    construct each) + `screens/` (15 realistic screens incl. the 3
    canonical worked examples); all valid v1 files
  - `skills/` — the `layout-txt` writer skill: `SKILL.md` (workflow,
    quick-reference, mistakes table), `references/grammar.md` (full
    restatement), `examples/` (3 canonical), `scripts/check_layout.py`
  - `discussions/` — design records: `layout-spec-format/` (the format's
    design rationale) and per-topic snapshot records
  - `.agents/skills/` — committed symlink → `skills/layout-txt` so pi
    auto-loads the skill; never break it
- **Data flow (conceptual)**: author writes a `.layout.txt` file → agent
  implements → agent extracts the app tree as JSON
  (`{type, variant?, label?, children?}`) → a future structural verifier
  (V2, not yet implemented) matches them. Today only the parse layer
  exists.

## PR & Commit Guidelines

- **Commit style**: Conventional Commits — history uses `docs(specs):`,
  `docs(skills):`, `docs(design):`, `docs(discussions):`, `chore:`.
- **One commit per coherent change**; include the related design record
  or log updates in the same commit.
- No remote is configured — commits stay local.

## Notes for AI Agents

- **Specs win.** The skill and examples restate the grammar; on any
  disagreement, `specs/LANGUAGE.md` is authoritative. Change the spec
  first, then propagate.
- **Discussion snapshots are permanent** — never edit, delete, or
  renumber files under `discussions/*/snapshots/`. `result.md` is the
  compiled record; `legacy/` holds archived formats.
- **The `layout-txt` skill is the writing playbook**: when asked to write
  LAYOUT files, load `skills/layout-txt/SKILL.md` (it auto-loads through
  the `.agents/skills/layout-txt` symlink once the project is trusted).
- **Format boundaries**: LAYOUT.txt expresses structure only — no
  behavior (events/nav/state) and no visuals (DESIGN.md's domain).
  Vocabulary is free-form; unknown widget types are INFO, never errors.
- **Incompleteness is a feature**: anything the grammar cannot express
  goes into a `#` note, never into grammar growth.
- **Runtime state**: `.pi/` and `.pi-subagents/` are gitignored agent
  tooling state — never commit them; `.pi/plans/*.md` are durable plan
  files (see `plan` skill).
- **Status**: the spec is a draft at format v1; a format change is a
  breaking change requiring a version bump (see `specs/SPEC.md`
  §Versioning).
