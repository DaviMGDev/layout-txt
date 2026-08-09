---
type: spec
title: "LAYOUT.txt — Specification"
description: "A minimal plain-text format for specifying UI structure at wireframe level; humans read, agents implement and verify"
tags: [spec]
sections: [context, decisions, grammar, semantics, conformance, examples, versioning, glossary]
created: "2026-08-08"
updated: "2026-08-08"
---

# LAYOUT.txt — Specification

*This spec declares its own contract: every `##` section below must appear in
`sections:` in the frontmatter, and nothing may appear undeclared. The
normative grammar and semantics live in `LANGUAGE.md`; this document is the
why, the decisions, and the conformance contract.*

## Context

UI/UX work at specification level currently uses InterSpec (`.is`) for
structure and DESIGN.md for visuals. InterSpec is a full declarative UI
language — state, events, navigation, reactivity, viewport contracts. For
wireframe-level structure ("this screen has these things in this order")
most of that machinery is unused, and the cost is real: a programming
language's worth of grammar and conventions to learn, write, and maintain.

LAYOUT.txt is the replacement for that structure layer: a plain-text,
markdown-free format with a tiny closed grammar and an open vocabulary. It
describes widgets, hierarchy, order, labels, variants, and annotations —
nothing more. DESIGN.md keeps owning the visual layer; LAYOUT.txt references
its vocabulary by convention only, never by validation.

**Goals**

- A screen structure spec that takes minutes to write and seconds to read.
- Deterministic enough that AI agents implement from it and verify against it.
- Plain text with zero inherited semantics: no markdown, no code fences,
  no tooling required.
- Vocabulary that never constrains the author: any widget type is legal.
- Incompleteness as a feature: anything the grammar cannot express is
  written as a note.

**Stakeholders**

- The spec author (writes LAYOUT files quickly, reads them later).
- Implementing agents (build screens from LAYOUT files).
- Verifying agents (check implementations against LAYOUT files).
- The design system (DESIGN.md) — the conventional source of widget names.

**Design record:** the full discussion, alternatives considered, and the
reasoning chains behind every decision live in
`discussions/layout-spec-format/layout-txt-format.md`.

## Decisions

All decisions were made deliberately in discussion; the important ones:

| # | Decision | Why |
|---|----------|-----|
| D1 | **`.txt`, not `.md`** | The extension decides what you inherit. Markdown brings link collisions (`[Save](button)` vs `[docs](https://…)`), fence noise, and rendering semantics. Plain text defines 100% of its own grammar — and the `[]()` shape stops being ambiguous. |
| D2 | **Label-first syntax** `[Label](type:variant attrs)` | Winner of a six-family comparison (vs type-first, markdown-headings, box-drawing, fenced type-first, lenient-only). Labels are what humans verify against; the shape is deterministic to parse and natural in `.txt`. |
| D3 | **Two shapes, one parse rule** | `[Label](type:variant attrs)` leaves and `(type:variant attrs)` groups. First token = type, optional `:variant`, rest = opaque attrs. Exotic widgets (`[Revenue](graph data=monthly)`) need no language change. |
| D4 | **`#` notes, positionally attached** | A note directly above a widget refers to it. No IDs, no labels, no comment syntax beyond one character. |
| D5 | **Bare lines are text widgets** | Headings and captions are structure: presence, order, and label are verified. Line kinds are disjoint by first character (`#`, `[`/`(`, else). |
| D6 | **`xN` suffix repetition** | Count attaches backward to the written item; on a group line it repeats the whole subtree. `x0` is an error; `x1` is a no-op. |
| D7 | **Free-form vocabulary + minimal core** | Unknown types are INFO, never errors (layout leads, the design system catches up). A 15-type recommended core (see LANGUAGE.md) stabilizes agent mappings and enables typo whispers. |
| D8 | **Structural verification only** | The verifier checks presence, order, hierarchy, labels, counts. Layout is a hint; attrs and notes are never compared; visuals are DESIGN.md's deliverable. |
| D9 | **Filesystem is the index** | One file = one screen; `LAYOUT.txt` (static sites), `<page>.layout.txt` (apps), domain subfolders keep the pattern. No index file, no registry, no imports; the glob is the inventory. |
| D10 | **Incompleteness is a feature** | Escape hatches, not grammar growth, are the anti-bloat mechanism. `]` in labels, `)` in attrs, and anything else unexpressible → a note. |

## Grammar

The normative grammar (G1–G12: line kinds, token grammar, hierarchy, rows,
repetition, notes, error handling, file naming) is defined in
`LANGUAGE.md` (§Grammar). LAYOUT.txt has exactly five things to learn:
`[Label](type:variant attrs)`, `(type)` + indentation, `xN`, `#`, and
"same line = side-by-side".

## Semantics

The meaning of every construct — widgets, text widgets, groups, repetition,
positional notes, states via `:variant`, exotic widgets via attrs, lenient
for humans / strict for agents — is defined in `LANGUAGE.md` (§Semantics).

## Conformance

An implementation (the built UI) conforms to a LAYOUT file when it matches
it structurally. The verifier is a small, dependency-free checker (a few
hundred lines) over two inputs:

1. **The spec** — the LAYOUT file, parsed per LANGUAGE.md §Grammar.
2. **The app tree** — the implemented UI extracted as JSON nodes of the
   shape `{type, variant?, label?, children?}` (the agent extracts it from
   the framework of choice; the verifier does not parse frameworks).

**V1 — Parse.** Any G11 violation (malformed widget line) is an **ERROR**
with file and line; the run stops with exit code 2.

**V2 — Structural match.** Recursive match per parent, in file order, over a
moving cursor of app children:

- *match* = same TYPE; same VARIANT if the spec declares one (app node has
  no variant data → **WARNING** "variant unverifiable"; different variant →
  **ERROR**); same LABEL if the spec node has one (exact, trimmed). Text
  widgets match by label only.
- No match → **ERROR** "missing `type[:variant] label`" with hint "maybe
  out of order".
- Count absent → require ≥ 1 match; more than one → **WARNING** "duplicate
  match".
- Count N → require exactly N subtree matches, each checked recursively;
  k < N → **ERROR** "found k of N"; more than N → **WARNING**.

**V3 — Informational.** Never affects pass/fail: unknown widget types →
**INFO** (name, line, count); unmatched app nodes (extras) → **INFO**;
attrs and notes → never compared, echoed in an INFO dump for the
implementer. Typo whispers ("`buton` — did you mean `button`?") are INFO.

**V4 — Exit codes.** `0` pass (no ERROR), `1` fail, `2` unparseable.
Warnings and INFO never fail.

**Out of scope (deliberately):** layout correctness (rows/columns are
hints), attrs (opaque), vocabulary (unregistered), cross-file references
(unvalidated in v1), visual fidelity (DESIGN.md's domain).

## Examples

Canonical worked examples — a login screen, a card grid, and a static-site
shell — are in `LANGUAGE.md` (§Worked examples).

## Versioning

The format is at **v1**. Additive changes (new recommended vocabulary,
clarified rules) are logged in `log.md` without a version bump. Changes that
alter parsing or the meaning of existing constructs are breaking and require
a new version of the format: update `LANGUAGE.md`, record the change in
`log.md`, and bump the version stated here. The versioned contract is the
pair (SPEC.md, LANGUAGE.md) as of the `updated` dates.

## Glossary

| Term | Meaning |
|------|---------|
| Widget | An element a screen contains: leaf or container. |
| Leaf | `[Label](type:variant attrs)` — a widget with a label, a type, and optional variant/attrs. |
| Container / group | `(type:variant attrs)` with indented children; without children it is a label-less leaf. |
| Label | The human-visible text of a widget; what verification matches. |
| Type | The kind of widget (convention: lowercase kebab-case; free-form vocabulary). |
| Variant | Style or state suffix after the first `:` of the type token (`button:primary`). |
| Attrs | Opaque passthrough text inside parens after the type; never parsed or verified. |
| Note | A `#` line; implementer guidance attached to the following widget line. |
| Text widget | A bare line; type `text` by convention, label = the trimmed line. |
| Row | Widgets on one physical line; a layout hint, never verified. |
| Screen | The implicit root of one LAYOUT file; identified by the file stem. |
| Layout file | One screen's spec: `LAYOUT.txt` or `<screen>.layout.txt`. |
| Stem | The filename without extension or folder (`login` in `auth/login.layout.txt`); the screen's identity. |
