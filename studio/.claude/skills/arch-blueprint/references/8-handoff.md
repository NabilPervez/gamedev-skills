# /arch-blueprint — Phase 8: Handoff

> Part of `/arch-blueprint`. `SKILL.md` names when to read this file; the settings it
> resolved and the rules under its later headings still apply here.

## Phase 8: Handoff

**Step 1 — Update session state**: Write a summary to `production/session-state/active.md` covering: artifact written, TD/LP sign-off verdicts, any blockers, required ADRs remaining, and next step.

**Step 2 — Output the handoff** using exactly this template (no freeform prose, no rephrasing of section titles):

---

## Architecture Complete

`docs/architecture/architecture.md` v[N] — [TD-ARCHITECTURE: APPROVE / CONCERNS (accepted) / REVISED after CONCERNS / REVISED after REJECT / NOT ASSESSED / skipped — [mode] mode]. [One sentence on what the architecture covers.]

---

## Run These ADRs Next

**1. `/arch-adr "[Title]"` → ADR-[XXXX]**
[One sentence: what it defines and what it unblocks.]

**2. `/arch-adr "[Title]"` → ADR-[XXXX]**
[One sentence.]

**3. `/arch-adr "[Title]"` → ADR-[XXXX]**
[One sentence.]

**Then:** `/review-architecture`, and `/arch-control-manifest` once it passes and those ADRs are Accepted — it turns them into the layer rules manifest.

List top 3 from Phase 6 in priority order. If fewer than 3 remain, list only what's outstanding.

---

## Gate-Check Readiness

> **Required before `/review-phase-gate pre-production`:**
> - [ ] Accept ADRs: [list Proposed ADR IDs that must be Accepted]
> - [ ] Write ADRs: [list ADR IDs that must still be written]
> - [ ] Run `/review-architecture` — writes the review report and the traceability index (`docs/architecture/requirements-traceability.md`) the gate reads
> - [ ] Run `/qa-test-setup` — scaffolds `tests/unit/`, `tests/integration/`, CI workflow, and an example test file
> - [ ] Run `/ux-spec` — creates `design/ux/interaction-patterns.md` and `design/accessibility-requirements.md`
>
> Run `/review-phase-gate pre-production` when all boxes are checked.

If nothing is blocking, write instead:
> No blockers — run `/review-phase-gate pre-production` now.

---

## Open Questions to Watch

| ID | Summary | Priority | Resolution Path |
|----|---------|----------|-----------------|
| QQ-XX | [short description] | High / Medium / Low | [ADR or system that resolves it] |

Omit this section entirely if there are no open QQs.

---

(End of handoff. Do not add trailing commentary after the closing rule.)

---
