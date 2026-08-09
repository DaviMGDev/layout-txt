---
type: index
title: "examples/ — Index"
description: "Catalog of LAYOUT.txt examples: capability showcases and realistic screens, all valid v1 files"
created: 2026-08-09
updated: 2026-08-09
---

# examples/ — Index

The LAYOUT.txt example catalog: every file is a **valid v1 file** — the
whole catalog passes `skills/layout-txt/scripts/check_layout.py` (exit 0).
Each file's first lines are screen-level meta notes (`#`) explaining what
it demonstrates; the notes are part of the format, so the catalog is
self-documenting.

**Normative grammar:** `../specs/LANGUAGE.md`. **Design rationale:**
`../discussions/layout-spec-format/layout-txt-format.md`. **Writer skill:**
`../skills/layout-txt/` (its `examples/` holds the three canonical
spec-worked examples; the same three are included here verbatim).

## Reading order

1. `capabilities/` — one construct per file, smallest ideas first. Read
   them in filename order: each builds on the previous.
2. `screens/` — realistic screens combining everything. Start with the
   three canonical examples (login, card-grid, static-site shell), then
   the rest.

## Capability showcases

Each file isolates one capability of the format. `#` notes teach the rule
being shown.

| File | Shows |
|------|-------|
| [line-kinds.layout.txt](capabilities/line-kinds.layout.txt) | the four line kinds: NOTE / WIDGET / TEXT / blank — disjoint by first character |
| [hierarchy.layout.txt](capabilities/hierarchy.layout.txt) | nesting via indentation: deep trees, single-child groups, no depth limit |
| [rows.layout.txt](capabilities/rows.layout.txt) | same line = row (side-by-side); separate lines = stacked; `(row)`/`(column)` by convention |
| [repetition.layout.txt](capabilities/repetition.layout.txt) | `xN`: on a leaf, on a group (whole subtree), mid-line, `x1` no-op |
| [variants-styles.layout.txt](capabilities/variants-styles.layout.txt) | `:variant` — styles and machine-checkable states |
| [attrs-passthrough.layout.txt](capabilities/attrs-passthrough.layout.txt) | opaque attrs: placeholders, URLs, data, exotic parameters |
| [notes-annotations.layout.txt](capabilities/notes-annotations.layout.txt) | `#` notes: positional attachment, stacking, screen-level meta |
| [text-widgets.layout.txt](capabilities/text-widgets.layout.txt) | bare lines as headings, captions, paragraphs — structure, verified by label |
| [exotic-vocabulary.layout.txt](capabilities/exotic-vocabulary.layout.txt) | free-form vocabulary: any type works, always |
| [forms-controls.layout.txt](capabilities/forms-controls.layout.txt) | `form`, `checkbox`, `select`, inputs, field labels as labels |
| [navigation-links.layout.txt](capabilities/navigation-links.layout.txt) | links, nav rows, cross-screen references by stem convention |
| [containers-leaves.layout.txt](capabilities/containers-leaves.layout.txt) | group vs label-less leaf — the same token, role decided by children |

## Screen examples

Realistic screens combining the capabilities. File stem = screen name
(G12); `static-site/LAYOUT.txt` also demonstrates the domain-subfolder
pattern (folders are pure grouping — screen identity stays in the stem).

| File | Screen |
|------|--------|
| [login.layout.txt](screens/login.layout.txt) | login form — the spec's canonical worked example (verbatim) |
| [card-grid.layout.txt](screens/card-grid.layout.txt) | browse catalog — repetition, nesting, label-less leaves (verbatim) |
| [static-site/LAYOUT.txt](screens/static-site/LAYOUT.txt) | company site shell — single-file form (verbatim) |
| [dashboard.layout.txt](screens/dashboard.layout.txt) | admin dashboard — stat cards, chart, activity feed |
| [settings.layout.txt](screens/settings.layout.txt) | settings — sections, toggles, selects, save bar |
| [checkout.layout.txt](screens/checkout.layout.txt) | checkout — steps, address, payment, order summary |
| [product.layout.txt](screens/product.layout.txt) | product page — gallery, options, reviews |
| [search-results.layout.txt](screens/search-results.layout.txt) | search — filters, result cards, pagination |
| [onboarding.layout.txt](screens/onboarding.layout.txt) | onboarding wizard — progress, fields, actions |
| [chat.layout.txt](screens/chat.layout.txt) | chat — conversation list, messages, composer |
| [profile.layout.txt](screens/profile.layout.txt) | user profile — header, stats, tabs |
| [email-client.layout.txt](screens/email-client.layout.txt) | mail — folders, message list, reading pane |
| [landing.layout.txt](screens/landing.layout.txt) | marketing landing — hero, features, testimonials, footer |
| [booking.layout.txt](screens/booking.layout.txt) | hotel booking — search, room cards, summary |
| [file-manager.layout.txt](screens/file-manager.layout.txt) | files — toolbar, breadcrumb, grid, details |

## Conventions

- One file = one screen (G12); `LAYOUT.txt` is the canonical single-file
  name — here reserved for the static-site shell.
- First line of every file is a screen-level meta note.
- Folders are pure grouping; the file stem is the screen's identity.
- Catalog files are deliberately **valid**; constructs that are parse
  errors (`x0`, tabs, `]` in labels, `)` in attrs) are described in
  notes, never written — see `../skills/layout-txt/SKILL.md` §Common
  mistakes for the failure modes.
