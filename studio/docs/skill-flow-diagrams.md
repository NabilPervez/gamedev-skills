# Skill Flow Diagrams

Visual maps of how skills chain together across the 7 development phases.
These show what runs before and after each skill, and what artifacts flow between them.

---

## Default Path: Rigor Minimal (Four Steps to Code)

`modes.rigor: minimal` is the default. The one-page brief is the design record and
its build order is the plan, so there is no epic planning, sprint or phase gate to run.
Every skill below still runs at any tier; rigor changes what is required, not what
is allowed. `/studio-next-step` follows this route at `minimal`.

```
MINIMAL PATH (modes.rigor: minimal — the default; no /review-phase-gate, stage stays Concept)
  /studio-setup-engine ───────────────────────────────────────────────► project.yaml + CLAUDE.md
  /concept-brainstorm ─────────────────────────────────────────────────► design/game-brief.md (one page)
        │                                                          (replaces concept doc, systems index, GDDs)
        ▼
  /plan-stories ─────────────────────────────────────────────► production/epics/[slug]/story-*.md
        │                                                          (brief's build order is the plan —
        │                                                           no /plan-epics, no /plan-sprint)
        ▼ (one story at a time, in build order)
  /build-story [story] ──────────────────────────────────────────► routes to correct programmer agent
  /build-story-done [story] ─────────────────────────────────────────► story closed + next story named
        │
        └── back to /build-story until every story is Complete, then:
              play the build · /plan-stories for more · /studio-settings to raise rigor
```

The overview below is the `standard`/`full` pipeline.

---

## Full Pipeline Overview (Zero to Ship)

```
PHASE 1: CONCEPT
  /studio-start ──────────────────────────────────────────────────────► routes to A/B/C/D
  /concept-brainstorm ──────────────────────────────────────────────────► design/gdd/game-concept.md
  /studio-setup-engine ────────────────────────────────────────────────► project.yaml + CLAUDE.md
  /concept-prototype [core-mechanic] ───────────────────────────────────► prototypes/[name]-concept/REPORT.md
        │ PROCEED                                                  (validate idea BEFORE writing GDDs)
        ▼
  /review-design-doc [game-concept.md] ────────────────────────────► concept validated
  /art-bible ──────────────────────────────────────────────────► design/art/art-bible.md
  /design-map-systems ────────────────────────────────────────────────► design/gdd/systems-index.md
  /review-phase-gate ─────────────────────────────────────────────────► PASS → advance to systems-design
        │
        ▼
PHASE 2: SYSTEMS DESIGN
  /design-map-systems next ───────────────────────────────────────────► picks the next system to design
        │
        ▼ (for each system, in dependency order)
  /design-system-gdd [name] ──────────────────────────────────────► design/gdd/[system].md
  /review-design-doc [system].md ─────────────────────────────────► per-GDD review comments
        │
        ▼ (after all MVP GDDs done)
  /review-gdd-suite ────────────────────────────────────────────► design/gdd/gdd-cross-review-[date].md
  /review-phase-gate ─────────────────────────────────────────────────► PASS → advance to technical-setup
        │
        ▼
PHASE 3: TECHNICAL SETUP
  /arch-blueprint ────────────────────────────────────────► docs/architecture/architecture.md
  /arch-adr (×N) ─────────────────────────────────► docs/architecture/[adr-nnn].md
  /review-architecture ────────────────────────────────────────► review report + docs/architecture/tr-registry.yaml
  /arch-control-manifest ────────────────────────────────────► docs/architecture/control-manifest.md
  /qa-test-setup ─────────────────────────────────────────────────► test framework + CI/CD pipeline
  /qa-test-helpers ───────────────────────────────────────────────► tests/helpers/ (engine-specific library)
  /ux-spec accessibility ─────────────────────────────────────► design/accessibility-requirements.md
  /ux-spec patterns ──────────────────────────────────────────► design/ux/interaction-patterns.md
  /review-phase-gate ─────────────────────────────────────────────────► PASS → advance to pre-production
        │
        ▼
PHASE 4: PRE-PRODUCTION
  [UX — before epics, so specs exist when stories are written]
  /ux-spec [screen/hud] ──────────────────────────────────────► design/ux/*.md
  /review-ux ──────────────────────────────────────────────────► UX specs approved (HARD gate for /team-ui)

  [Vertical slice — before epics, validate full game loop]
  /build-vertical-slice ─────────────────────────────────────────────► prototypes/[name]-vertical-slice/REPORT.md
  /qa-playtest-report ────────────────────────────────────────────► production/qa/playtests/

  [Stories + sprint plan — only after vertical slice PROCEEDS]
  /plan-epics [layer] ───────────────────────────────────────► production/epics/*/EPIC.md
  /plan-stories [epic-slug] ─────────────────────────────────► production/epics/*/story-*.md
  /plan-sprint new ────────────────────────────────────────────► production/sprints/sprint-001.md
  /review-phase-gate ─────────────────────────────────────────────────► PASS → advance to production
        │
        ▼
PHASE 5: PRODUCTION (repeating sprint loop)
  /plan-sprint-status ──────────────────────────────────────────────► sprint snapshot
  /plan-story-readiness [story] ────────────────────────────────────► story validated READY
        │
        ▼ (pick up and implement)
  /build-story [story] ──────────────────────────────────────────► routes to correct programmer agent
        │
        ▼ (during implementation, as needed)
  /review-code ────────────────────────────────────────────────► code review report
  /review-scope ────────────────────────────────────────────────► scope creep detected / clear
  /review-content ──────────────────────────────────────────────► GDD content gaps identified
  /qa-bug-report ─────────────────────────────────────────────────► production/qa/bugs/BUG-NNNN.md
  /qa-bug-triage ─────────────────────────────────────────────────► bugs re-prioritized + assigned

  [Team skills for feature areas — spawn when working a full feature]
  /team-combat / /team-narrative / /team-ui / /team-level / /team-audio

  [QA cycle per sprint]
  /qa-test-plan ────────────────────────────────────────────────────► production/qa/qa-plan-[sprint-slug]-[date].md
  /qa-smoke ────────────────────────────────────────────────► smoke test gate (PASS/FAIL)
  /qa-regression ───────────────────────────────────────────► coverage gaps + missing regression tests
  /qa-evidence-review ───────────────────────────────────────► evidence quality report
  /qa-flaky-tests ─────────────────────────────────────────────► flaky test report
        │
        ▼
  /build-story-done [story] ─────────────────────────────────────────► story closed + next surfaced
  /plan-sprint [next] ─────────────────────────────────────────► next sprint
        │
        ▼ (after Production milestone)
  /prod-milestone-review ───────────────────────────────────────────► milestone report
  /review-phase-gate ─────────────────────────────────────────────────► PASS → advance to polish
        │
        ▼
PHASE 6: POLISH
  /qa-perf-profile ───────────────────────────────────────────────► perf report + fixes
  /review-balance ──────────────────────────────────────────────► balance report + fixes
  /art-asset-audit ────────────────────────────────────────────────► asset compliance report
  /review-tech-debt ──────────────────────────────────────────────────► docs/tech-debt-register.md
  /qa-soak ──────────────────────────────────────────────────► soak test protocol + results
  /team-polish ────────────────────────────────────────────────► polish sprint orchestrated
  /team-qa ────────────────────────────────────────────────────► full QA cycle sign-off
  /review-security ─────────────────────────────────────────────► production/security/security-audit-[date]-[scope].md
  /prod-localize qa ────────────────────────────────────────────────► production/localization/loc-qa-[locale]-[date].md
  /release-checklist ──────────────────────────────────────────► production/releases/release-checklist-[version].md
  /release-changelog ──────────────────────────────────────────────────► docs/CHANGELOG.md
  /release-patch-notes ────────────────────────────────────────────────► docs/patch-notes/[version].md (draft)
  /review-phase-gate ─────────────────────────────────────────────────► PASS → advance to release
        │
        ▼
PHASE 7: RELEASE
  /release-launch-checklist ───────────────────────────────────────────► launch readiness report
  /team-release ───────────────────────────────────────────────► release pipeline orchestrated
        │
        ▼ (post-launch, ongoing)
  /release-hotfix ─────────────────────────────────────────────────────► emergency fix with audit trail
  /team-live-ops ──────────────────────────────────────────────► live-ops content plan
```

---

## Skill Chain: /design-system-gdd in Detail

How a single GDD gets authored, reviewed, and handed to architecture:

```
systems-index.md (input)
game-concept.md (input)
upstream GDDs (input, if any)
        │
        ▼
/design-system-gdd [name]
        │
        ├── Pre-check: feasibility table + engine risk flags
        │
        ├── Section cycle × 8:
        │     question → options → decision → draft → approval → WRITE
        │     [each section written to file immediately after approval]
        │
        └── Output: design/gdd/[system].md (complete, all 8 sections)
                │
                ▼
        /review-design-doc design/gdd/[system].md
                │
                ├── APPROVED → mark DONE in systems-index, proceed to next system
                ├── NEEDS REVISION → agent shows specific issues, re-enter section cycle
                └── MAJOR REVISION → significant redesign needed before next system
                        │
                        ▼ (after all MVP GDDs + cross-review)
                /review-gdd-suite
                        │
                        └── Output: gdd-cross-review-[date].md
```

---

## Skill Chain: UX / UI Pipeline in Detail

Screen and HUD specs are authored in Phase 4 (Pre-Production), before epics are
written, so that story acceptance criteria can reference specific UX artifacts.
Accessibility and interaction-pattern specs are authored earlier, in Phase 3
(Technical Setup), since at `full` the Technical Setup → Pre-Production gate
requires them (at `standard` they are recommended; at `minimal` they drop).

```
design/gdd/*.md (UI/UX requirements extracted)
design/player-journey.md (emotional arc, if authored)
        │
        ▼
/ux-spec hud              → design/ux/hud.md
/ux-spec screen [name]    → design/ux/screens/[name].md
/ux-spec patterns         → design/ux/interaction-patterns.md
        │
        ▼
/review-ux design/ux/
        │
        ├── APPROVED → UX specs ready, proceed to /plan-epics
        ├── NEEDS REVISION → blocking issues listed → fix → re-run review
        └── MAJOR REVISION → fundamental UX problems → redesign before epics
                │
                ▼ (after APPROVED — in Phase 5 when implementing UI features)
        /team-ui
                │
                ├── Phase 1: /ux-spec (if any specs still missing) + /review-ux
                ├── Phase 2: visual design (art-director)
                ├── Phase 3: layout implementation (ui-programmer)
                ├── Phase 4: accessibility audit (accessibility-specialist)
                └── Phase 5: final review

Note: /ux-spec accessibility and /ux-spec patterns belong in Phase 3
      (Technical Setup); /ux-spec screen/hud and /review-ux belong in Phase 4
      (Pre-Production). /team-ui belongs in Phase 5 (Production) when a UI
      feature is being built.
```

---

## Skill Chain: Dev Story Flow in Detail

How a story moves from backlog to closed:

```
/plan-story-readiness [story]
        │
        ├── READY → Status: ready-for-dev → pick up for implementation
        ├── NEEDS WORK → agent shows specific gaps → resolve → re-run readiness
        └── BLOCKED → ADR still Proposed, or upstream story incomplete
                │
                ▼ (after READY)
        /build-story [story]
                │
                ├── Reads: story file, linked GDD requirement, ADR decisions, control manifest
                ├── Routes to: gameplay-programmer / engine-programmer / ui-programmer / etc.
                │
                └── Implementation begins
                        │
                        ▼ (optional, during/after implementation)
                /review-code          → architectural review of changeset
                /review-scope          → verify no scope creep vs. original story criteria
                /qa-evidence-review → validate test files and manual evidence quality
                        │
                        ▼
                /build-story-done [story]
                        │
                        ├── COMPLETE → Status: Complete, sprint-status.yaml updated, next story surfaced
                        ├── COMPLETE WITH NOTES → complete but some criteria deferred (logged)
                        └── BLOCKED → acceptance criteria cannot be verified → investigate blocker
```

---

## Skill Chain: Story Lifecycle (Backlog to Closed)

How a story gets from backlog to closed (summary view):

```
/plan-epics [layer]
        │
        └── Output: production/epics/[slug]/EPIC.md
                │
                ▼
        /plan-stories [epic-slug]
                │
                └── Output: production/epics/[slug]/story-NNN-[slug].md
                            (Status: Ready or Blocked if ADR is Proposed)
                │
                ▼
        /plan-story-readiness [story]
                │
                ├── READY → /build-story → implement → /build-story-done
                ├── NEEDS WORK → resolve gaps → re-run
                └── BLOCKED → fix upstream dependency first
```

---

## Skill Chain: QA Pipeline in Detail

```
[Phase 3 — one-time infrastructure setup]
/qa-test-setup ────────────────────────────────────────────────────► test framework scaffolded + CI/CD wired
/qa-test-helpers ──────────────────────────────────────────────────► tests/helpers/ (GDUnit4, NUnit, etc.)

[Phase 5 — per-sprint QA cycle]
/qa-test-plan [sprint or feature]
        │
        ├── Reads: story files, GDDs, acceptance criteria
        ├── Classifies each story by test type:
        │     Logic → automated unit test (BLOCKING by default)
        │     Integration → integration test or documented playtest (BLOCKING by default)
        │     Visual/Feel → retained screenshot + lead sign-off (BLOCKING by default)
        │     UI → retained screenshot of each screen (BLOCKING by default)
        │     Config/Data → smoke check (ADVISORY by default)
        │     (gate levels are overridable per type via testing.strict in project.yaml)
        └── Output: production/qa/qa-plan-[sprint-slug]-[date].md
                │
                ▼
        /qa-smoke
                │
                ├── PASS → QA hand-off cleared
                └── FAIL → block sprint close → fix critical paths first
                        │
                        ▼
                /qa-regression
                        │
                        └── Coverage gaps + list of fixed bugs without regression tests
                                │
                                ▼
                        /qa-evidence-review
                                │
                                └── Validates evidence quality, not just existence
                                        │
                                        ▼ (if CI run history available)
                        /qa-flaky-tests
                                │
                                └── Flaky test report + fix recommendations

[Phase 6 — extended stability testing]
/qa-soak ─────────────────────────────────────────────────────► soak test protocol + observed results
/team-qa ───────────────────────────────────────────────────────► full QA cycle sign-off for release gate

[Ongoing — bug management]
/qa-bug-report ────────────────────────────────────────────────────► production/qa/bugs/BUG-NNNN.md
/qa-bug-triage ────────────────────────────────────────────────────► open bugs re-prioritized + assigned

[Meta — harness validation]
/meta-skill-test [lint|spec|catalog] ────────────────────────────────► skill file structural + behavioral check
```

---

## Brownfield Onboarding Flow

For projects with existing work (use `/studio-start` option D or run directly):

```
/studio-detect-stage    → stage detection report
        │
        ▼
/studio-adopt-project
        │
        ├── Phase 1: detect what exists
        ├── Phase 2: FORMAT audit (not just existence)
        ├── Phase 3: classify gaps (BLOCKING / HIGH / MEDIUM / LOW)
        ├── Phase 4: ordered migration plan
        ├── Phase 5: write docs/adoption-plan-[date].md
        └── Phase 6: fix most urgent gap inline (optional)
                │
                ▼
        /design-system-gdd retrofit [path]    → fills missing GDD sections
        /arch-adr retrofit [path] → fills missing ADR sections
        /review-phase-gate                       → where are you in the pipeline?
```

---

## How to Read These Diagrams

| Symbol | Meaning |
|--------|---------|
| `──►` | Produces this artifact |
| `│ ▼` | Flows into next step |
| `├──` | Branch (multiple possible outcomes) |
| `×N` | Runs N times (once per system, story, etc.) |
| `(input)` | Read by the skill but not produced here |
| `[optional]` | Not required for the gate to pass |
| `WRITE` (caps) | File written to disk immediately |

---

## Common Entry Points

| Where you are | Run this |
|---------------|---------|
| Brand new, no idea | `/studio-start` → `/concept-brainstorm` |
| Have a concept, no engine | `/studio-setup-engine` |
| Have concept + engine | `/design-map-systems` |
| Mid-systems design | `/design-system-gdd [next system]` or `/design-map-systems next` |
| All GDDs done | `/review-gdd-suite` → `/review-phase-gate` |
| In technical setup | `/arch-blueprint` → `/arch-adr` |
| Starting UX design | `/ux-spec screen [name]` or `/ux-spec hud` |
| Scaffolding tests | `/qa-test-setup` → `/qa-test-helpers` |
| Have stories, ready to code | `/plan-story-readiness [story]` → `/build-story [story]` |
| Story done | `/build-story-done [story]` |
| Running QA for a sprint | `/qa-test-plan` → `/qa-smoke` → `/qa-regression` |
| Bug backlog needs sorting | `/qa-bug-triage` |
| Extended stability testing | `/qa-soak` |
| Not sure | `/studio-next-step` |
| Existing project | `/studio-adopt-project` |
