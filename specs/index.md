---
type: index
title: "specs/ — Index"
description: "Node registry and reading order for the specs/ directory"
created: 2026-08-08
updated: 2026-08-08
---

# specs/ — Index

Project status: draft

## Nodes

| File | Title | Description |
|------|-------|-------------|
| [SPEC.md](SPEC.md) | LAYOUT.txt — Specification | the spec monolith: context, decisions, conformance contract, versioning, glossary |
| [LANGUAGE.md](LANGUAGE.md) | LAYOUT.txt — Language Reference | the normative grammar, semantics, recommended vocabulary, organization, examples |
| [log.md](log.md) | specs/ log | activity log of spec changes |

## Reading order

SPEC.md — read top to bottom; the frontmatter `sections:` is the contract.
Follow links to LANGUAGE.md for the normative grammar, semantics, and
worked examples. The design discussion record lives outside `specs/` in
`discussions/layout-spec-format/layout-txt-format.md`.
