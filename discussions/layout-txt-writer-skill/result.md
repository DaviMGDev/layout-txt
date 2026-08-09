# layout-txt-writer-skill — closed
Date: 2026-08-09 · snapshots: 4

## Topic
Create a new skills/ directory in this repo containing a skill that helps agents write LAYOUT.txt files (the wireframe-level UI structure format just specified in specs/). Use the thinker subagent as helper to produce a full proposal; resolve all open questions raised during the discussion by myself; the user will only give opinion at the final proposal.

## Timeline
**[2026-08-09 00:05]** (Snapshot 1, entry)
idea: repo gains a top-level skills/ directory containing a skill that helps agents write LAYOUT.txt structure files
constraint: user will not answer questions during the process — all design questions must be resolved by me
constraint: thinker subagent (reasoning-only, no tools) must be consulted as helper for the full proposal
constraint: proposal must be complete when presented; user gives opinion only at the final proposal

**[2026-08-09 00:05]** (Snapshot 2, manual)
insight: pi auto-discovers project skills from .pi/skills/ and .agents/skills/ (committed, cross-harness standard); a top-level skills/ dir is NOT auto-loaded
decision: canonical skill lives in versioned skills/layout-txt/; loading via committed symlink .agents/skills/layout-txt -> ../../skills/layout-txt (fallback: .pi/settings.json skills array pointing at ../skills)
insight: agentskills.io standard — .agents/skills/ is the agent-agnostic shared location, so a committed symlink survives fresh clones

**[2026-08-09 00:11]** (Snapshot 3, message)
insight: thinker proposal (a4fbe95d) resolves all 9 questions: name layout-txt; hybrid grammar embedding (quick-ref inline + references/grammar.md + specs-wins precedence); structure SKILL.md+references+examples+scripts; include parse-only check_layout.py (G11, not V2); 9-step workflow; 13-row failure-mode table; MKF index.md+log.md; 7 non-goals; version pin + drift guards + validation steps
decision: include ALL THREE worked examples verbatim (login, card-grid, static-site shell) — thinker proposed 2; the LAYOUT.txt single-file form directly illustrates the Step-1 file-home decision, zero extra cost
decision: skill-to-specs relative path pinned as ../../specs/LANGUAGE.md (from skills/layout-txt/)
decision: check_layout.py tab rule interpreted — whitespace-only lines are blank (ignored); tab error applies to lines with content (G1 edge, documented in script header)
decision: single commit docs(skills): add layout-txt writer skill (repo convention; feat() defensible since it ships a script — noted)
decision: no .pi/settings.json created; symlink primary; fallback documented only
decision: design-rationale pointer added to references/grammar.md (discussions/layout-spec-format/layout-txt-format.md) for traceability

**[2026-08-09 00:12]** (Snapshot 4, close)
answer (all): user approved the full proposal as presented ("Approve as proposed") — no changes requested
decision: proposal accepted in full; implementation scope = exactly the file tree + commit in the proposal

## Final state
### Facts & constraints
- Repo: /home/davi/Projects/local/web — LAYOUT.txt v1 spec project (specs/SPEC.md + specs/LANGUAGE.md, status draft)
- Pi skill discovery: project .pi/skills/ and .agents/skills/ (trusted); top-level skills/ NOT auto-loaded; committed symlink is the loading mechanism; .agents/ not gitignored
- skill-creator validation: name lowercase/hyphens/≤64, description ≤1024
- User flow honored: thinker helper → full proposal → user opined at the end only
### Priorities
- Proposal completeness; genuinely useful writer skill; consistency with repo conventions (MKF nodes, single source of truth); anti-bloat
### Decisions
- Name: layout-txt (format-named, family-compatible with future layout-txt-verify); description carries "write"
- Grammar embedding: hybrid (b+) — compact quick-ref inline in SKILL.md; full restatement in references/grammar.md; precedence "specs/LANGUAGE.md wins"; version pin LAYOUT v1 in 3 places
- Structure: skills/index.md + skills/log.md (MKF compound node) + skills/layout-txt/{SKILL.md, references/grammar.md, examples/{login,card-grid,LAYOUT}.layout.txt, scripts/check_layout.py} + committed symlink .agents/skills/layout-txt → ../../skills/layout-txt
- Parse-check script: YES — python3 stdlib-only, G11 parse-only, exit 0/2/1 (matches SPEC.md V4 semantics); NOT the V2 verifier
- Workflow: 9 steps (0-8): read context → file home → inventory → type mapping → hierarchy/rows → variant-vs-attr-vs-note → xN only for identical → notes for inexpressible → self-check checklist + checker run
- Failure modes: 13-row markdown-habits-to-unlearn table (verified against G1-G12)
- Boundaries: 7 non-goals (no visuals, no behavior, no vocab enforcement, no V2, no cross-file validation, no fabrication, no other formats)
- Commit: single docs(skills): add layout-txt writer skill
- Validation: checker on examples → 0; negative fixtures → 2; skill-creator validate.py; symlink resolution check; verbatim example copies
- Overrules on thinker: 3 examples (incl. static-site LAYOUT.txt); pinned relative paths (../../specs/); tab rule on whitespace-only lines = blank; design-rationale pointer in grammar.md
- USER APPROVED THE FULL PROPOSAL AS PRESENTED — no changes
### Questions
- Q1 name/description — answered: layout-txt
- Q2 grammar embedding — answered: hybrid b+
- Q3 skill structure — answered: as in proposal
- Q4 parse-check script — answered: yes, G11-only
- Q5 workflow design — answered: 9 steps
- Q6 failure modes — answered: 13-row table
- Q7 skills/ conventions — answered: MKF index.md + log.md
- Q8 boundaries — answered: 7 non-goals
- Q9 extras — answered: version pin, drift guards, install docs, commit, validation
### Rejected alternatives
- skills/ under .pi/ only (hidden, unshareable)
- Minimal pointer-only skill (unportable standalone)
- Full grammar inline in SKILL.md only (second spec, drift)
- Including V2 structural verifier now (scope creep; parse/match separation)
- .pi/settings.json as primary loading (unverified path semantics)
### Next steps
- (post-discussion, user's call) materialize the approved file tree, copy examples verbatim from specs/LANGUAGE.md, write check_layout.py per spec, run validation steps, single commit docs(skills): add layout-txt writer skill
