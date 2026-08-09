---
type: index
title: "skills/ — Index"
description: "Skill registry, install/loading documentation, and conventions for the skills/ directory"
created: 2026-08-09
updated: 2026-08-09
---

# skills/ — Index

Skill registry and conventions for this project's agent skills. Project
status: draft.

## Registry

| Skill | Version | Purpose |
|-------|---------|---------|
| [layout-txt](layout-txt/SKILL.md) | v1 (LAYOUT format v1) | write valid LAYOUT.txt files — structure only |

### layout-txt

- **Canonical location:** `skills/layout-txt/`
- **Purpose:** convert a design brief or an existing UI/HTML/DOM into a
  valid LAYOUT.txt file (the plain-text wireframe structure format;
  normative grammar in `specs/LANGUAGE.md`).
- **Auto-load:** the committed symlink `.agents/skills/layout-txt` →
  `../../skills/layout-txt` makes pi (and other harnesses following the
  agentskills.io convention) discover the skill automatically once the
  project is trusted.
- **Fallback** (only if symlinks are unsupported, e.g. Windows without
  developer mode): make `.agents/skills/layout-txt` a real directory
  (copy) — or use `.pi/settings.json` `{"skills": ["../skills"]}`; the
  latter's path semantics are unverified, so prefer the symlink. Global
  install (all projects): copy `skills/layout-txt/` into
  `~/.pi/agent/skills/`.

## Conventions

- Canonical skills live in `skills/<name>/`; auto-loading happens via
  committed symlinks in `.agents/skills/` pointing back to them.
- Every skill is a directory with a `SKILL.md` (frontmatter: `name` +
  `description`), plus optional `references/`, `examples/`, `scripts/`.
- Skill names: lowercase, hyphens only, ≤ 64 chars; descriptions ≤ 1024
  chars (validated by the skill-creator `validate.py`).
- Format-related skills pin the format version they target; the normative
  source wins on conflict (see `layout-txt/references/grammar.md`).

## Reading order

Start at the registry above, then `layout-txt/SKILL.md`. The normative
grammar lives in `specs/LANGUAGE.md`; the design rationale lives in
`discussions/layout-spec-format/layout-txt-format.md`.
