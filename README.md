# LAYOUT.txt

A minimal plain-text format for specifying UI structure at wireframe
level — **humans read it, AI agents implement and verify it**.

LAYOUT.txt describes widgets, hierarchy, order, labels, variants, and
annotations — nothing more. It deliberately expresses no behavior
(events, navigation, state — that was InterSpec's weight) and no visuals
(colors, spacing, typography — that is DESIGN.md's domain). Vocabulary is
free-form; the grammar is closed. Incompleteness is a feature: anything
the grammar cannot express is written as a `#` note.

**Status:** draft · format **v1**

## Quick tour

```text
# Login screen — LAYOUT v1

Welcome back
Please sign in to continue

(form)
  [Email](input placeholder=you@example.com)
  [Password](input secure)
  [Remember me](checkbox) [Forgot?](link forgot)
  [Sign in](button:primary full-width)
```

Five things to learn: `[Label](type:variant attrs)`, `(type)` +
indentation, `xN` repetition, `#` notes, and "same line = side-by-side".

## Repository map

| Path | What it is |
|------|------------|
| [specs/](specs/index.md) | the specification — `SPEC.md` (why + decisions + conformance contract) and `LANGUAGE.md` (normative grammar G1–G12, semantics, vocabulary, worked examples) |
| [examples/](examples/index.md) | the example catalog — 12 capability showcases + 15 realistic screens, every file a valid v1 file |
| [skills/](skills/index.md) | agent skills — the `layout-txt` writer skill (workflow, grammar reference, parse-check script) |
| [discussions/](discussions/layout-spec-format/layout-txt-format.md) | the design record — every decision, alternative, and the reasoning behind it |
| [AGENTS.md](AGENTS.md) | operating instructions for AI agents working in this repo |
| [.agents/skills/](.agents/skills/) | committed symlink that auto-loads the `layout-txt` skill into pi |

## Reading order

1. `examples/capabilities/` — one construct per file, smallest ideas first.
2. `examples/screens/` — realistic screens combining everything.
3. `specs/SPEC.md` — the why and the conformance contract.
4. `specs/LANGUAGE.md` — the normative grammar.
5. `skills/layout-txt/SKILL.md` — how to write LAYOUT.txt files as an agent.

## Validation

Every example in the catalog is checked against the format's parse rules
(G11):

```bash
python3 skills/layout-txt/scripts/check_layout.py $(find examples -name '*.layout.txt' -o -name 'LAYOUT.txt')
```

Exit codes: `0` all valid · `2` parse error · `1` unreadable/usage.
The script is dependency-free (Python 3 stdlib).

## License

[MIT](LICENSE) © 2026 Davi Macêdo Gomes
