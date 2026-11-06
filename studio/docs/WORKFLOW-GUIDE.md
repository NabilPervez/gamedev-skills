# Claude Code Game Studios -- Complete Workflow Guide

> **How to go from zero to a shipped game using the Agent Architecture.**
>
> This guide walks you through every phase of game development using the
> 49-agent system, 74 slash commands, and 15 automated hooks. It assumes you
> have Claude Code installed and are working from the project root.
>
> The pipeline has 7 phases. At `rigor: standard` and `full`, each phase has
> a formal gate (`/review-phase-gate`) that must pass before you advance. At
> `rigor: minimal` -- the default -- nothing requires a gate; see
> [The Default Path](#the-default-path-rigor-minimal). The authoritative
> phase sequence is defined in `.claude/docs/workflow-catalog.yaml` and read
> by `/studio-next-step`.

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [The Default Path: Rigor Minimal](#the-default-path-rigor-minimal)
3. [Phase 1: Concept](#phase-1-concept)
4. [Phase 2: Systems Design](#phase-2-systems-design)
5. [Phase 3: Technical Setup](#phase-3-technical-setup)
6. [Phase 4: Pre-Production](#phase-4-pre-production)
7. [Phase 5: Production](#phase-5-production)
8. [Phase 6: Polish](#phase-6-polish)
9. [Phase 7: Release](#phase-7-release)
10. [Cross-Cutting Concerns](#cross-cutting-concerns)
11. [Appendix A: Agent Quick-Reference](#appendix-a-agent-quick-reference)
12. [Appendix B: Slash Command Quick-Reference](#appendix-b-slash-command-quick-reference)
13. [Appendix C: Common Workflows](#appendix-c-common-workflows)

---

## Quick Start

### What You Need

Before you start, make sure you have:

- **Claude Code** installed and working
- **Git** with Git Bash (Windows) or standard terminal (Mac/Linux)
- **jq** (optional but recommended -- hooks fall back to `grep` if missing)
- **Python 3** (required -- every skill and hook reads `project.yaml` through it; without it every setting silently falls back to its default)

### Step 1: Clone and Open

```bash
git clone <repo-url> my-game
cd my-game
```

### Step 2: Run /studio-start

If this is your first session:

```
/studio-start
```

This guided onboarding asks where you are and routes you to the right phase:

- **Path A** -- No idea yet: routes to `/concept-brainstorm`
- **Path B** -- Vague idea: routes to `/concept-brainstorm` with seed
- **Path C** -- Clear concept: routes to `/concept-brainstorm` to write it down, or
  straight to `/studio-setup-engine`
- **Path D** -- Existing work: routes to `/studio-setup-engine` when no engine is set
  and there is no more than a concept; otherwise to `/studio-detect-stage`,
  then `/studio-adopt-project` for brownfield migration

### Step 3: Verify Hooks Are Working

Start a new Claude Code session. You should see output from the
`session-start.sh` hook:

```
=== Claude Code Game Studios -- Session Context ===
Branch: main
Recent commits:
  abc1234 Initial commit
===================================
```

If you see this, hooks are working. If not, check `.claude/settings.json` to
make sure the hook paths are correct for your OS.

### Step 4: Ask for Help Anytime

At any point, run:

```
/studio-next-step
```

This reads your current phase from `project.stage` in `project.yaml` (falling
back to `production/stage.txt`) -- at `rigor: minimal`, where the stage never
moves, it follows the minimal route instead -- checks which artifacts exist, and tells you
exactly what to do next. It distinguishes between REQUIRED next steps and
OPTIONAL opportunities.

### Step 5: Create Your Directory Structure

Directories are created as needed. The system expects this layout:

```
src/                  # Game source code (Godot; Unity: Assets/, Unreal: Source/<Module>/)
  core/               # Engine/framework code
  gameplay/           # Gameplay systems
  ai/                 # AI systems
  networking/         # Multiplayer code
  ui/                 # UI code
  tools/              # Dev tools
assets/               # Game assets
  art/                # Sprites, models, textures
  audio/              # Music, SFX
  vfx/                # Particle effects
  shaders/            # Shader files
  data/               # JSON config/balance data
design/               # Design documents
  gdd/                # Game design documents
  narrative/          # Story, lore, dialogue
  levels/             # Level design documents
  balance/            # Balance spreadsheets and data
  ux/                 # UX specifications
docs/                 # Technical documentation
  architecture/       # Architecture Decision Records
  api/                # API documentation
  postmortems/        # Post-mortems
tests/                # Test suites
prototypes/           # Throwaway prototypes
production/           # Sprint plans, milestones, releases
  sprints/
  milestones/
  releases/
  epics/              # Epic and story files (from /plan-epics + /plan-stories)
  playtests/          # Playtest reports
  session-state/      # Ephemeral session state (gitignored)
  session-logs/       # Session audit trail (gitignored)
```

> **Tip:** You do not need all of these on day one. Create directories as you
> reach the phase that needs them. The important thing is to follow this
> structure when you do create them, because the **rules system** enforces
> standards based on file paths. Code in `src/gameplay/` gets gameplay rules,
> code in `src/ai/` gets AI rules, and so on — and the same for C# and C++ in
> Unity and Unreal `Gameplay/` and `AI/` folders.

---

## The Default Path: Rigor Minimal

`modes.rigor` defaults to `minimal` (`/studio-start` infers the tier from your description and shows it
before saving; `/studio-settings` changes it any time). At `minimal` the path to code is four steps:

1. `/studio-setup-engine` -- configure the engine
2. `/concept-brainstorm` -- writes the one-page `design/game-brief.md`, which replaces
   the full concept doc, the systems decomposition and the per-system GDDs
3. `/plan-stories` -- turns the brief's MVP list and build order into stories
   under `production/epics/<slug>/`. No `/plan-epics`, no `/plan-sprint`: the
   brief's build order is the plan
4. `/build-story` then `/build-story-done`, story by story. `/build-story-done` names the
   next story, and `/studio-next-step` knows this route

Nothing on this path runs `/review-phase-gate`, so `project.stage` stays at Concept --
that is expected. Every skill still runs at any tier; rigor changes what is
required, not what is allowed.

The trade: there are no GDDs to catch design problems before they reach code.
Raise rigor with `/studio-settings` when the game outgrows a one-page brief -- several
systems that affect each other, a design someone else implements, a team, or a
firm release date. Existing files stay where they are, and `/studio-next-step` shows what
the new tier requires next.

The rest of this guide describes the `standard`/`full` pipeline.

---

## Phase 1: Concept

### What Happens in This Phase

You go from "no idea" or "vague idea" to a structured game concept document
with defined pillars and a player journey. This is where you figure out
**what** you are making and **why**.

### Phase 1 Pipeline

```
/concept-brainstorm  -->  game-concept.md  -->  /review-design-doc  -->  /studio-setup-engine
     |                                        |                    |
     v                                        v                    v
  10 concepts     Concept doc with       Validation          Engine pinned in
  MDA analysis    pillars, MDA,          of concept          project.yaml
  Player motiv.   core loop, USP         document
                                                                   |
                                                                   v
                                                             /concept-prototype
                                                       (concept prototype — 1 day max)
                                                        PROCEED ↓     PIVOT → /concept-brainstorm
                                                                   |
                                                                   v (PROCEED)
                                                             /design-map-systems
                                                                   |
                                                                   v
                                                            systems-index.md
                                                            (all systems, deps,
                                                             priority tiers)
```

### Step 1.1: Brainstorm With /concept-brainstorm

This is your starting point. Run the brainstorm skill:

```
/concept-brainstorm
```

Or with a genre hint:

```
/concept-brainstorm roguelike deckbuilder
```

**What happens:** The brainstorm skill guides you through a collaborative 6-phase
ideation process using professional studio techniques:

1. Asks about your interests, themes, and constraints
2. Generates 10 concept seeds with MDA (Mechanics, Dynamics, Aesthetics) analysis
3. You pick 2-3 favorites for deep analysis
4. Performs player motivation mapping and audience targeting
5. You choose the winning concept
6. Formalizes it into `design/gdd/game-concept.md`

The concept document includes:

- Elevator pitch (one sentence)
- Core fantasy (what the player imagines themselves doing)
- MDA breakdown
- Target audience (Bartle types, demographics)
- Core loop diagram
- Unique selling proposition
- Comparable titles and differentiation
- Game pillars (3-5 non-negotiable design values)
- Anti-pillars (things the game intentionally avoids)

### Step 1.2: Review the Concept (Optional but Recommended)

```
/review-design-doc design/gdd/game-concept.md
```

Validates structure and completeness before you proceed.

### Step 1.3: Choose Your Engine

```
/studio-setup-engine
```

Or with a specific engine:

```
/studio-setup-engine godot 4.7
```

**What /studio-setup-engine does:**

- Writes engine, language, specialists, naming conventions, and performance
  budgets to `project.yaml` (the source of truth) and mirrors them to
  `.claude/docs/technical-preferences.md` (the human-readable legacy fallback)
- Detects knowledge gaps (engine version newer than LLM training data) and
  advises cross-referencing `docs/engine-reference/`
- Creates version-pinned reference docs in `docs/engine-reference/`

**Why this matters:** Once you set the engine, the system knows which
engine-specialist agents to use. If you pick Godot, agents like
`godot-specialist`, `godot-gdscript-specialist`, and `godot-shader-specialist`
become your go-to experts.

### Step 1.4: Decompose Your Concept Into Systems

Before writing individual GDDs, enumerate all the systems your game needs:

```
/design-map-systems
```

This creates `design/gdd/systems-index.md` -- a master tracking document that:

- Lists every system your game needs (combat, movement, UI, etc.)
- Maps dependencies between systems
- Assigns priority tiers (MVP, Vertical Slice, Alpha, Full Vision)
- Determines design order (Foundation > Core > Feature > Presentation > Polish)

This step is **required** before proceeding to Phase 2. Research from 155 game
postmortems confirms that skipping systems enumeration costs 5-10x more in
production.

### Step 1.5: Art Bible

```
/art-bible
```

Authors `design/art/art-bible.md`, the visual identity every asset follows.
Run it once the concept is approved; `/art-bible` suggests doing it before
`/design-map-systems` (Step 1.4). Sections 1–4 are needed before `/review-phase-gate pre-production`, and all
9 before `/review-phase-gate production`. At `standard` it is required only when the
game has visual-asset stories; at `minimal` it is optional.

### Phase 1 Gate

```
/review-phase-gate systems-design
```

**Requirements to pass:**

- `design/gdd/game-concept.md` with content, the game pillars, and a Visual
  Identity Anchor section (at `minimal`: `design/game-brief.md` with content)
- Recommended: a concept prototype whose REPORT.md says PROCEED

This is the `full` list. `standard` and `minimal` drop items; the gate's own
file, `.claude/skills/review-phase-gate/references/gate-systems-design.md`, has the full
checklist and what each tier drops.

**Verdict:** PASS / CONCERNS / NOT ASSESSED / FAIL. PASS advances the stage.
On CONCERNS it advances only if you explicitly accept the risks, which are
recorded; a FAIL never advances it. NOT ASSESSED means something required could
not be checked.

---

## Phase 2: Systems Design

### What Happens in This Phase

You create all the design documents that define how your game works. Nothing
gets coded yet -- this is pure design. Each system identified in the systems
index gets its own GDD, authored section by section, reviewed individually,
and then all GDDs are cross-checked for consistency.

### Phase 2 Pipeline

```
/design-map-systems next  -->  /design-system-gdd  -->  /review-design-doc
       |                     |                     |
       v                     v                     v
  Picks next system    Section-by-section     Validates 8
  from systems-index   GDD authoring          required sections
                       (incremental writes)   APPROVED/NEEDS REVISION
       |
       |  (repeat for each MVP system)
       v
/review-gdd-suite
       |
       v
  Cross-GDD consistency + design theory review
  PASS / CONCERNS / NOT ASSESSED / FAIL
```

### Step 2.1: Author System GDDs

Design each system in dependency order using the guided workflow:

```
/design-map-systems next
```

This picks the highest-priority undesigned system and hands off to
`/design-system-gdd`, which guides you through creating its GDD section by section.

You can also design a specific system directly:

```
/design-system-gdd combat-system
```

**What /design-system-gdd does:**

1. Reads your game concept, systems index, and any upstream/downstream GDDs
2. Runs a Technical Feasibility Pre-Check (domain mapping + feasibility brief)
3. Walks you through each of the 8 required GDD sections one at a time
4. Each section follows: Context > Questions > Options > Decision > Draft > Approval > Write
5. Each section is written to file immediately after approval (survives crashes)
6. Flags conflicts with existing approved GDDs
7. Routes to specialist agents per category (systems-designer for math,
   economy-designer for economy, narrative-director for story systems)

**The 8 required GDD sections:**

| # | Section | What Goes Here |
|---|---------|---------------|
| 1 | **Overview** | One-paragraph summary of the system |
| 2 | **Player Fantasy** | What the player imagines/feels when using this system |
| 3 | **Detailed Rules** | Unambiguous mechanical rules |
| 4 | **Formulas** | Every calculation, with variable definitions and ranges |
| 5 | **Edge Cases** | What happens in weird situations? Explicitly resolved. |
| 6 | **Dependencies** | What other systems this connects to (bidirectional) |
| 7 | **Tuning Knobs** | Which values designers can safely change, with safe ranges |
| 8 | **Acceptance Criteria** | How do you test that this works? Specific, measurable. |

Plus a **Game Feel** section: feel reference, input responsiveness (ms/frames),
animation feel targets (startup/active/recovery), impact moments, weight profile.

### Step 2.2: Review Each GDD

Before the next system starts, validate the current one:

```
/review-design-doc design/gdd/combat-system.md
```

Checks the sections your `modes.workflow` tier requires (all 8 at `full`, 5 at
`standard`) for completeness, formula clarity, edge case resolution,
bidirectional dependencies, and testable acceptance criteria.

**Verdict:** APPROVED / NEEDS REVISION / MAJOR REVISION NEEDED / NOT ASSESSED.
Only APPROVED GDDs should proceed.

### Step 2.3: Small Changes Without Full GDDs

For tuning changes, small additions, or tweaks that do not warrant a full GDD:

```
/design-quick-spec "add 10% damage bonus for flanking attacks"
```

This creates a lightweight spec in `design/quick-specs/` instead of a full
8-section GDD. Use it for tuning, number changes, and small additions.

### Step 2.4: Cross-GDD Consistency Review

After all MVP system GDDs are approved individually:

```
/review-gdd-suite
```

This reads ALL GDDs simultaneously and runs two analysis phases:

**Phase 1 -- Cross-GDD Consistency:**
- Dependency bidirectionality (A references B, does B reference A?)
- Rule contradictions between systems
- Stale references to renamed or removed systems
- Ownership conflicts (two systems claiming the same responsibility)
- Formula range compatibility (does System A's output fit System B's input?)
- Acceptance criteria cross-check

**Phase 2 -- Design Theory (Game Design Holism):**
- Competing progression loops (do two systems fight for the same reward space?)
- Cognitive load (more than 4 active systems at once?)
- Dominant strategies (one approach that makes all others irrelevant)
- Economic loop analysis (sources and sinks balanced?)
- Difficulty curve consistency across systems
- Pillar alignment and anti-pillar violations
- Player fantasy coherence

**Output:** `design/gdd/gdd-cross-review-[date].md` with a verdict.

### Step 2.5: Narrative Design (If Applicable)

If your game has story, lore, or dialogue, this is when you build it:

1. **World-building** -- Use `world-builder` to define factions, history,
   geography, and rules of your world
2. **Story structure** -- Use `narrative-director` to design story arcs,
   character arcs, and narrative beats
3. **Character sheets** -- Use the `narrative-character-sheet.md` template

### Phase 2 Gate

```
/review-phase-gate technical-setup
```

**Requirements to pass:**

- `design/gdd/systems-index.md` listing at least the MVP systems, with their
  dependencies mapped
- A GDD for every MVP system, each passing `/review-design-doc` (no MAJOR REVISION
  NEEDED)
- A cross-GDD review report from `/review-gdd-suite` whose verdict is not FAIL —
  and not NOT ASSESSED, which means the GDDs could not be compared

This is the `full` list. `standard` and `minimal` drop items; the gate's own
file, `.claude/skills/review-phase-gate/references/gate-technical-setup.md`, has the full
checklist and what each tier drops.

---

## Phase 3: Technical Setup

### What Happens in This Phase

You make key technical decisions, document them as Architecture Decision Records
(ADRs), validate them through review, and produce a control manifest that
gives programmers flat, actionable rules. You also establish UX foundations.

### Phase 3 Pipeline

```
/arch-blueprint  -->  /arch-adr (x N)  -->  /review-architecture
        |                          |                                   |
        v                          v                                   v
  Master architecture       Per-decision ADRs              Validates completeness,
  document covering         in docs/architecture/          dependency ordering,
  all systems               adr-*.md                       engine compatibility
                                                                      |
                                                                      v
                                                         /arch-control-manifest
                                                                      |
                                                                      v
                                                         Flat programmer rules
                                                         docs/architecture/
                                                         control-manifest.md
        Also in this phase:
        -------------------
        /ux-spec  -->  /review-ux
        Accessibility requirements doc  (/ux-spec accessibility)
        Interaction pattern library     (/ux-spec patterns)
        /qa-test-setup  -->  test framework + CI workflow
```

### Step 3.1: Master Architecture Document

```
/arch-blueprint
```

Creates the overarching architecture document in `docs/architecture/architecture.md`
covering system boundaries, data flow, and integration points.

### Step 3.2: Architecture Decision Records (ADRs)

For each significant technical decision:

```
/arch-adr "State Machine vs Behavior Tree for NPC AI"
```

**What happens:** The skill guides you through creating an ADR with:
- Context and decision drivers
- All options with pros/cons and engine compatibility
- Chosen option with rationale
- Consequences (positive, negative, risks)
- Dependencies (Depends On, Enables, Blocks, Ordering Note)
- GDD Requirements Addressed (linked by TR-ID)

ADRs go through a lifecycle: Proposed > Accepted > Superseded/Deprecated.

**Minimum 3 Foundation-layer ADRs are required** before the gate check.

**Retrofitting existing ADRs:** If you already have ADRs from a brownfield
project:

```
/arch-adr retrofit docs/architecture/adr-005.md
```

This detects which template sections are missing and adds only those, never
overwriting existing content.

### Step 3.3: Architecture Review

```
/review-architecture
```

Validates all ADRs together:
- Topological sort of ADR dependencies (detects cycles)
- Engine compatibility verification
- GDD Revision Flags (flags GDD sections that need updates based on ADR choices)
- TR-ID registry maintenance (`docs/architecture/tr-registry.yaml`)

### Step 3.4: Control Manifest

```
/arch-control-manifest
```

Takes all Accepted ADRs and produces a flat programmer rules sheet:

```
docs/architecture/control-manifest.md
```

This contains Required patterns, Forbidden patterns, and Guardrails organized
by code layer. Stories created later embed the manifest version date so
staleness can be detected.

### Step 3.5: Accessibility Requirements

Create `design/accessibility-requirements.md` using the template. Commit to a
tier (Basic / Standard / Comprehensive / Exemplary) and fill the 4-axis feature
matrix (visual, motor, cognitive, auditory).

This document is required in Phase 3 because UX specs (written in Phase 4)
reference this tier — it is a design prerequisite, not a UX deliverable.
`/ux-spec accessibility` authors it; `/ux-spec patterns` starts the
interaction pattern library (`design/ux/interaction-patterns.md`), which the same
gate checks.

### Step 3.6: Test Framework

```
/qa-test-setup
```

Scaffolds the engine's test root, `.github/workflows/tests.yml` and one example
test; the Pre-Production gate checks for them. `/qa-test-helpers` can follow once
there are systems to test.

### Phase 3 Gate

```
/review-phase-gate pre-production
```

**Requirements to pass:**

- The engine configured, `project.yaml` populated (engine, naming, performance)
  and the engine reference docs present
- Art bible Sections 1–4 (`design/art/art-bible.md`)
- `docs/architecture/architecture.md`, at least 3 ADRs covering Foundation-layer
  systems, an `/review-architecture` report and
  `docs/architecture/requirements-traceability.md`
- The test framework in the engine's test root, `.github/workflows/tests.yml`
  and one example test (`/qa-test-setup`)
- `design/accessibility-requirements.md` and `design/ux/interaction-patterns.md`
  (`/ux-spec accessibility`, `/ux-spec patterns`)

This is the `full` list. `standard` and `minimal` drop items; the gate's own
file, `.claude/skills/review-phase-gate/references/gate-pre-production.md`, has the full
checklist and what each tier drops.

---

## Phase 4: Pre-Production

### What Happens in This Phase

You create UX specs for key screens, prototype risky mechanics, turn design
documents into implementable stories, plan your first sprint, and build a
Vertical Slice that proves the core loop is fun.

### Phase 4 Pipeline

```
/ux-spec  -->  /build-vertical-slice  -->  /plan-epics  -->  /plan-stories  -->  /plan-sprint
    |                   |                   |                   |                       |
    v                   v                   v                   v                       v
  UX specs       Production-quality   Epic files in       Story files in          First sprint with
  design/ux/     end-to-end build     production/         production/             prioritized stories
                 in prototypes/       epics/*/EPIC.md     epics/*/story-*.md      production/sprints/
                 PROCEED/PIVOT/KILL   (one per module)    (one per behaviour)     sprint-*.md
    |                                                          |
    v                                                          v
 /review-ux                                             /plan-story-readiness
 (validates specs                                       (validates each story
  before epics)                                          before pickup)
                                                               |
                                                               v
                                                           /build-story
                                                         (implements the story,
                                                          routes to right agent)
```

### Step 4.1: UX Specs for Key Screens

Before writing epics, create UX specs so that story authors know what screens
exist and what player interactions they must support.

**UX Specs:**

```
/ux-spec main-menu
/ux-spec core-gameplay-hud
```

Three modes: screen/flow, HUD, and interaction patterns. Output goes to
`design/ux/`. Each spec includes: player need, layout zones, states,
interaction map, data requirements, events fired, accessibility, localization.

Reads your `accessibility-requirements.md` (written in Phase 3) and your
input method config from `project.yaml` (the `platform.*` block, falling back
to `technical-preferences.md`) to drive accessibility and input coverage
checks — no need to re-specify them per screen.

> **Tip:** `/design-system-gdd` emits a 📌 UX Flag for every system with UI
> requirements. Use those flags as a checklist for which screens need specs.

**Interaction Pattern Library:**

```
/ux-spec patterns
```

Started in Phase 3 (the Pre-Production gate checks it); extend it here as the
key screens add patterns. `design/ux/interaction-patterns.md` holds 16 standard
controls plus game-specific patterns (inventory slot, ability icon, HUD bar,
dialogue box, etc.) with animation and sound standards.

**UX Review:**

```
/review-ux all
```

Validates UX specs for GDD alignment and accessibility tier compliance.
Produces APPROVED / NEEDS REVISION / MAJOR REVISION NEEDED verdict.

### Step 4.2: Build the Vertical Slice

The vertical slice is the production-quality proof that you can build the full
game loop end-to-end before committing to full Production.

```
/build-vertical-slice
```

**What it proves:** Does a player, starting from nothing, experience the core
fantasy within a few minutes, without developer guidance?

**What it builds:** A near-production-quality playable build covering at least
one complete [start → challenge → resolution] cycle. Uses real architecture
layers, real naming conventions, no hardcoded values — but not final art or
audio. This is not a throwaway like the concept prototype; it demonstrates
production pipeline feasibility.

**Note on concept prototyping:** If you ran `/concept-prototype` in Phase 1 (Concept),
you already validated the core idea is fun. The vertical slice now validates
you can build it properly. They answer different questions. If you skipped the
concept prototype, now is a reasonable time to run one first before investing
in the full slice.

**Verdict:** The vertical slice produces a PROCEED / PIVOT / KILL verdict, or
NOT ASSESSED while nobody has played it through.
- **PROCEED** → move to Step 4.3 (epics and stories)
- **PIVOT** → revise affected GDDs with `/design-system-gdd [mechanic]`, then re-run `/build-vertical-slice`
- **KILL** → return to `/concept-brainstorm` with what you learned

### Step 4.3: Create Epics and Stories From Design Artifacts

```
/plan-epics layer: foundation
/plan-stories [epic-slug]   # repeat for each epic
/plan-epics layer: core
/plan-stories [epic-slug]   # repeat for each core epic
```

`/plan-epics` reads your GDDs, ADRs, and architecture to define epic scope —
one epic per architectural module. Then `/plan-stories` breaks each epic into
implementable story files in `production/epics/[slug]/`. Each story embeds:
- GDD requirement references (TR-IDs, not quoted text -- stays fresh)
- ADR references (only from Accepted ADRs; Proposed ADRs cause `Status: Blocked`)
- Control manifest version date (for staleness detection)
- Engine-specific implementation notes
- Acceptance criteria from the GDD

Once stories exist, run `/build-story [story-path]` to implement one — it routes
automatically to the correct programmer agent.

### Step 4.4: Validate Stories Before Pickup

```
/plan-story-readiness production/epics/combat/story-combat-damage-calc.md
```

Checks: Design completeness, Architecture coverage, Scope clarity, Definition
of Done. Verdict: READY / NEEDS WORK / BLOCKED / NOT ASSESSED.

### Step 4.5: Effort Estimation

```
/plan-estimate production/epics/combat/story-combat-damage-calc.md
```

Provides effort estimates with risk assessment.

### Step 4.6: Plan Your First Sprint

```
/plan-sprint new
```

**What happens:** The `producer` agent collaborates on sprint planning:
- Asks for sprint goal and available time
- Breaks the goal into Must Have / Should Have / Nice to Have tasks
- Identifies risks and blockers
- Creates `production/sprints/sprint-001.md`
- Populates `production/sprint-status.yaml` (machine-readable story tracking)

### Step 4.7: Vertical Slice (recommended)

Before advancing to Production, build and playtest a Vertical Slice:

- One complete end-to-end core loop, playable from start to finish
- Representative quality (not placeholder everything)
- Played unguided in at least 1 documented session (3+ recommended)
- Playtest report written (`/qa-playtest-report`)

`/review-phase-gate production` treats it as recommended, not blocking: a skipped
slice is CONCERNS, a slice nobody has played is NOT ASSESSED, and a built slice
that is broken or not fun is a FAIL. At `workflow: minimal` the slice items
drop: the gate asks instead whether the current build's core loop is fun and
runs end to end.

### Phase 4 Gate

```
/review-phase-gate production
```

**Requirements to pass:**

- A first sprint plan in `production/sprints/`, and Foundation and Core epics
  with their stories under `production/epics/`
- The complete art bible (all 9 sections) with its AD-ART-BIBLE sign-off
  recorded
- Every MVP GDD complete, the master architecture document, Foundation and Core
  ADRs `Accepted`, and the control manifest
- UX specs for the key screens (main menu, HUD, pause menu) that passed
  `/review-ux`
- Recommended, not blocking: a Vertical Slice built and played in at least one
  documented session. Skipped → CONCERNS; built but broken or not fun → FAIL;
  built but not yet played → NOT ASSESSED

This is the `full` list. `standard` and `minimal` drop items; the gate's own
file, `.claude/skills/review-phase-gate/references/gate-production.md`, has the full
checklist and what each tier drops.

---

## Phase 5: Production

### What Happens in This Phase

This is the core production loop. You work in sprints (typically 1-2 weeks),
implementing features story by story, tracking progress, and closing stories
through a structured completion review. This phase repeats until your game
is content-complete.

### Phase 5 Pipeline (Per Sprint)

```
/plan-sprint new  -->  /plan-story-readiness  -->  implement  -->  /build-story-done
       |                     |                    |                |
       v                     v                    v                v
  Sprint created       Story validated      Code written     8-phase review:
  sprint-status.yaml   READY verdict        Tests pass       verify criteria,
  populated                                                  check deviations,
                                                             update story status
       |
       |  (repeat per story until sprint complete)
       v
  /plan-sprint-status  (quick 30-line snapshot anytime)
  /review-scope    (if scope is growing)
  /prod-retro  (at sprint end)
```

### Step 5.1: The Story Lifecycle

The production phase centers on the **story lifecycle**:

```
/plan-story-readiness  -->  implement  -->  /build-story-done  -->  next story
```

**1. Story Readiness:** Before picking up a story, validate it:

```
/plan-story-readiness production/epics/combat/story-combat-damage-calc.md
```

This checks design completeness, architecture coverage, ADR status (blocks
if ADR is still Proposed), control manifest version (warns if stale), and
scope clarity. Verdict: READY / NEEDS WORK / BLOCKED / NOT ASSESSED.

**2. Implementation:** Work with the appropriate agents:

- `gameplay-programmer` for gameplay systems
- `engine-programmer` for core engine work
- `ai-programmer` for AI behavior
- `network-programmer` for multiplayer
- `ui-programmer` for UI code
- `tools-programmer` for dev tools

All agents follow the collaborative protocol: they read the design doc, ask
clarifying questions, present architectural options, get your approval, then
implement.

**3. Story Completion:** When a story is done:

```
/build-story-done production/epics/combat/story-combat-damage-calc.md
```

This runs an 8-phase completion review:
1. Find and read the story file
2. Load referenced GDD, ADRs, and control manifest
3. Verify acceptance criteria (auto-checkable, manual, deferred)
4. Check for GDD/ADR deviations (BLOCKING / ADVISORY / OUT OF SCOPE)
5. Prompt for code review
6. Generate completion report (COMPLETE / COMPLETE WITH NOTES / BLOCKED)
7. Update story `Status: Complete` with completion notes
8. Surface the next ready story

Tech debt discovered during review is logged to `docs/tech-debt-register.md`.

### Step 5.2: Sprint Tracking

Check progress anytime:

```
/plan-sprint-status
```

Quick 30-line snapshot reading from `production/sprint-status.yaml`.

If scope is growing:

```
/review-scope production/sprints/sprint-003.md
```

This compares current scope against the original plan and flags scope increase,
recommends cuts.

### Step 5.3: Content Tracking

```
/review-content
```

Compares GDD-specified content against what has been implemented. Catches
content gaps early.

### Step 5.4: Design Change Propagation

When a GDD changes after stories have been created:

```
/design-propagate-change design/gdd/combat-system.md
```

Git-diffs the GDD, finds affected ADRs, generates an impact report, and
walks you through Superseded/update/keep decisions.

### Step 5.5: Multi-System Features (Team Orchestration)

For features spanning multiple domains, use team skills:

```
/team-combat "healing ability with HoT and cleanse"
/team-narrative "Act 2 story content"
/team-ui "inventory screen redesign"
/team-level "forest dungeon level"
/team-audio "combat audio pass"
```

Each team skill coordinates a 6-phase collaborative workflow:
1. **Design** -- game-designer asks questions, presents options
2. **Architecture** -- lead-programmer proposes code structure
3. **Parallel Implementation** -- specialists work simultaneously
4. **Integration** -- gameplay-programmer wires everything together
5. **Validation** -- qa-tester runs against acceptance criteria
6. **Report** -- coordinator summarizes status

The orchestration is automated, but **decision points stay with you**.

### Step 5.6: Sprint Review and Next Sprint

At the end of a sprint:

```
/prod-retro
```

Analyzes planned vs. completed, velocity, blockers, and actionable improvements.

Then plan the next sprint:

```
/plan-sprint new
```

### Step 5.7: Milestone Reviews

At milestone checkpoints:

```
/prod-milestone-review "alpha"
```

Produces feature completeness, quality metrics, risk assessment, and go/no-go
recommendation.

### Phase 5 Gate

```
/review-phase-gate polish
```

**Requirements to pass:**

- Every core GDD mechanic implemented, and the main gameplay path playable end
  to end
- Tests in the engine's test root covering the Logic and Integration stories,
  and passing
- A smoke-check report in `production/qa/` with PASS or PASS WITH WARNINGS
- A `/team-qa` sign-off (APPROVED or APPROVED WITH CONDITIONS)
- At least 3 documented playtest sessions (new player, mid-game, difficulty
  curve) and the fun hypothesis validated or revised
- No open S1 Critical bugs, and performance within budget

This is the `full` list. `standard` and `minimal` drop items; the gate's own
file, `.claude/skills/review-phase-gate/references/gate-polish.md`, has the full
checklist and what each tier drops.

---

## Phase 6: Polish

### What Happens in This Phase

Your game is feature-complete. Now you make it good. This phase focuses on
performance, balance, accessibility, audio, visual polish, and playtesting.

### Phase 6 Pipeline

```
/qa-perf-profile  -->  /review-balance  -->  /art-asset-audit  -->  /qa-playtest-report (x3)
       |                  |                    |                    |
       v                  v                    v                    v
  Profile CPU/GPU    Analyze formulas     Verify naming,      Cover: new player,
  memory, optimize   and data for         formats, sizes      mid-game, difficulty
  bottlenecks        broken progressions                      curve

  /review-tech-debt  -->  /team-polish
       |                |
       v                v
  Track and        Coordinated pass:
  prioritize       performance + art +
  debt items       audio + UX + QA

  /review-security  -->  /prod-localize qa  -->  /release-checklist  -->  /release-changelog
                        (per language)                           + /release-patch-notes
  Release readiness: the Polish -> Release gate checks all four.
```

### Step 6.1: Performance Profiling

```
/qa-perf-profile
```

Guides you through structured performance profiling:
- Establish targets (FPS, memory, platform)
- Identify bottlenecks ranked by impact
- Generate actionable optimization tasks with code locations and expected gains

### Step 6.2: Balance Analysis

```
/review-balance assets/data/combat_damage.json
```

Analyzes balance data for statistical outliers, broken progression curves,
degenerate strategies, and economy imbalances.

### Step 6.3: Asset Audit

```
/art-asset-audit
```

Verifies naming conventions, file format standards, and size budgets across
all assets.

### Step 6.4: Playtesting (Required: 3 Sessions)

```
/qa-playtest-report
```

Generates structured playtest reports. Three sessions are required, covering:
- New player experience
- Mid-game systems
- Difficulty curve

### Step 6.5: Technical Debt Assessment

```
/review-tech-debt
```

Scans for TODO/FIXME/HACK comments, code duplication, overly complex functions,
missing tests, and outdated dependencies. Each item categorized and prioritized.

### Step 6.6: Coordinated Polish Pass

```
/team-polish "combat system"
```

Coordinates 4 specialists in parallel:
1. Performance optimization (performance-analyst lists the optimisations; a
   programmer in the active set implements them — at `team.size: individual`,
   where none is active, the list is handed to `/build-story`)
2. Visual polish (technical-artist)
3. Audio polish (sound-designer)
4. Feel/juice (gameplay-programmer + technical-artist)

You set priorities; the team executes with your approval at each step.

### Step 6.7: Localization and Accessibility

```
/prod-localize scan
```

Scans for hardcoded strings, concatenation that breaks translation, text that
does not account for expansion, and missing locale files.

Accessibility is audited against the tier committed in Phase 3's accessibility
requirements document.

### Step 6.8: Security Audit

```
/review-security
```

Required for the release gate at `standard` and `full`: the newest report must
have no open CRITICAL or HIGH finding. A report whose recommendation is NOT
ASSESSED leaves the gate's security item NOT ASSESSED.

### Step 6.9: Localization QA

```
/prod-localize qa
```

Run it for every language you ship. At `full` the release gate needs a PASS (or
PASS WITH CONDITIONS) for each; a locale nobody has checked is NOT ASSESSED.

### Step 6.10: Release Checklist

```
/release-checklist all
```

The argument is the platform scope (`pc`, `console`, `mobile` or `all`), not a
version.

Generates a comprehensive pre-release checklist covering:
- Build verification (all platforms compile and run)
- Certification requirements (platform-specific)
- Store metadata (descriptions, screenshots, trailers)
- Legal compliance (EULA, privacy policy, ratings)
- Save game compatibility
- Analytics verification

### Step 6.11: Changelog and Patch Notes

```
/release-patch-notes v1.0.0
```

Generates player-friendly patch notes from git history and sprint data.
Translates developer language into player language.

```
/release-changelog v1.0.0
```

Generates an internal changelog (more technical, for the team).

The release gate needs the changelog or the patch notes drafted, so write them
now; `/team-release` publishes them once the release is a GO.

### Phase 6 Gate

```
/review-phase-gate release
```

**Requirements to pass:**

- Every milestone feature implemented and the content complete
- A QA test plan and a QA sign-off, and every Must Have story's test evidence
  (UI: retained screenshots; Visual/Feel: screenshots plus lead sign-off)
- Smoke check PASS on the release candidate, and the test suite passing
- `/review-balance` run, the release checklist completed, and the changelog or
  patch notes drafted
- No open S1–S3 bugs, the newest `/review-security` with no open CRITICAL or
  HIGH finding, and a `/prod-localize qa` pass for every locale you ship

This is the `full` list. `standard` and `minimal` drop items; the gate's own
file, `.claude/skills/review-phase-gate/references/gate-release.md`, has the full
checklist and what each tier drops.

---

## Phase 7: Release

### What Happens in This Phase

Your game is polished, tested, and ready. Now you ship it.

### Phase 7 Pipeline

```
/release-launch-checklist  -->  /team-release
        |                      |
        v                      v
  Full cross-department    Coordinate:
  validation (Go/No-Go     build, QA sign-off,
  per department)          deployment, launch

  The release checklist, security audit and patch notes are done in Polish,
  before /review-phase-gate release.   Also: /release-hotfix, /release-day-one-patch
```

### Step 7.1: Launch Readiness (Full Validation)

```
/release-launch-checklist
```

Complete cross-department validation:

| Department | What Is Checked |
|-----------|---------------|
| **Engineering** | Build stability, crash rates, memory leaks, load times |
| **Design** | Feature completeness, tutorial flow, difficulty curve |
| **Art** | Asset quality, missing textures, LOD levels |
| **Audio** | Missing sounds, mixing levels, spatial audio |
| **QA** | Open bug count by severity, regression suite pass rate |
| **Narrative** | Dialogue completeness, lore consistency, typos |
| **Localization** | All strings translated, no truncation, locale testing |
| **Accessibility** | Compliance checklist, assistive feature testing |
| **Store** | Metadata complete, screenshots approved, pricing set |
| **Marketing** | Press kit ready, launch trailer, social media scheduled |
| **Community** | Patch notes draft, FAQ prepared, support channels ready |
| **Infrastructure** | Servers scaled, CDN configured, monitoring active |
| **Legal** | EULA finalized, privacy policy, COPPA/GDPR compliance |

What no file can settle — the EULA, pricing, the on-call schedule — is asked
once per section: yes, no, not yet or N/A. A "no" or "not yet" is a failed item.
The overall status is READY, CONDITIONAL (only items with a workaround or an
accepted risk remain), NOT ASSESSED (something is still unconfirmed) or NOT
READY (a blocking item failed).

### Step 7.2: Coordinate the Release

```
/team-release
```

Coordinates release-manager, QA, and DevOps through:
1. Pre-release validation
2. Build management
3. Final QA sign-off
4. Deployment preparation
5. Go/No-Go decision

### Step 7.3: Ship

The `validate-push` hook will warn you when pushing to `main` or a `release/*` branch.
This is intentional -- release pushes should be deliberate:

```bash
git tag v1.0.0
git push origin main --tags
```

### Step 7.4: Post-Launch

**Hotfix workflow** for critical production bugs:

```
/release-hotfix "Players losing save data when inventory exceeds 99 items"
```

Bypasses normal sprint processes with a full audit trail:
1. Creates a hotfix branch
2. Implements the fix
3. Ensures the fix is backported to `main` (the trunk)
4. Documents the incident

**Post-mortem** after launch stabilizes:

```
Ask Claude to create a post-mortem using the template at
.claude/docs/templates/post-mortem.md
```

---

## Cross-Cutting Concerns

These topics apply across all phases.

### Director Review Modes

Director gates are specialist agents that review your work at key workflow steps.
**By default none run.** `modes.review_mode` follows `modes.rigor`, and the
default rigor, `rigor: minimal`, gives `solo`.

| Mode | What runs | The default under | Best for |
|------|-----------|-------------------|----------|
| `full` | All director gates at every step | `rigor: full` | Studio-scale projects, learning the system |
| `lean` | Directors only at phase transitions (`/review-phase-gate`) | `rigor: standard` | Experienced devs |
| `solo` | No director reviews | `rigor: minimal` | Solo projects, game jams, prototypes |

**Change it** with `/studio-settings modes.review_mode=lean` (written to `project.yaml`;
an explicit value wins over rigor), or `/studio-settings --local modes.review_mode=full`
for your machine only. `/studio-start` does not set it.

**Override for a single run** without changing your setting:

```
/concept-brainstorm space horror --review full
/arch-adr --review solo
```

The `--review` flag works on all gate-using skills. The first of these that is
set wins: the flag, `project.local.yaml`, `project.yaml`, a legacy
`production/review-mode.txt`, then the rigor default. A `review-mode.txt` left
from an older version still overrides rigor — delete it if the mode surprises you.

Full gate definitions and check pattern: `.claude/docs/director-gates.md`

---

### The Collaboration Protocol

This system is **user-driven collaborative**, not autonomous.

**Pattern:** Question > Options > Decision > Draft > Approval

Every agent interaction follows this pattern:
1. Agent asks clarifying questions
2. Agent presents 2-4 options with trade-offs and reasoning
3. You decide
4. Agent drafts based on your decision
5. You review and refine
6. Agent asks "May I write this to [filepath]?" before writing

See `docs/COLLABORATIVE-DESIGN-PRINCIPLE.md` for the full protocol with
examples.

### The AskUserQuestion Tool

Agents use the `AskUserQuestion` tool for structured option presentation.
The pattern is Explain then Capture: full analysis in conversation text first,
then a clean UI picker for the decision. Use it for design choices,
architecture decisions, and strategic questions. Do not use it for open-ended
discovery questions or simple yes/no confirmations.

### Agent Coordination (3-Tier Hierarchy)

```
Tier 1 (Directors):    creative-director, technical-director, producer
                                          |
Tier 2 (Leads):        game-designer, lead-programmer, art-director,
                       audio-director, narrative-director, qa-lead,
                       release-manager, localization-lead
                                          |
Tier 3 (Specialists):  gameplay-programmer, engine-programmer,
                       ai-programmer, network-programmer, ui-programmer,
                       tools-programmer, systems-designer, level-designer,
                       economy-designer, world-builder, writer,
                       technical-artist, sound-designer, ux-designer,
                       qa-tester, performance-analyst, devops-engineer,
                       analytics-engineer, accessibility-specialist,
                       live-ops-designer, prototyper, security-engineer,
                       community-manager, godot-specialist,
                       godot-gdscript-specialist, godot-shader-specialist,
                       godot-csharp-specialist, godot-gdextension-specialist,
                       unity-specialist, unity-dots-specialist,
                       unity-shader-specialist, unity-addressables-specialist,
                       unity-ui-specialist, unreal-specialist,
                       unreal-blueprint-specialist, unreal-gas-specialist,
                       unreal-replication-specialist, unreal-umg-specialist
```

**Coordination rules:**
- Vertical delegation: Directors > Leads > Specialists. Never skip tiers for
  complex decisions.
- Horizontal consultation: Agents at the same tier may consult each other but
  must not make binding decisions outside their domain.
- Conflict resolution: Design conflicts go to `creative-director`. Technical
  conflicts go to `technical-director`. Scope conflicts go to `producer`.
- No unilateral cross-domain changes.

### Automated Hooks (Safety Net)

The system has 15 hooks that run automatically:

| Hook | Trigger | What It Does |
|------|---------|-------------|
| `session-start.sh` | Session start | Shows branch, recent commits, detects active.md for recovery |
| `detect-gaps.sh` | Session start | Detects fresh projects (no engine, no concept) and suggests `/studio-start` |
| `pre-compact.sh` | Before compaction | Logs the compaction (its output does not reach Claude) |
| `notify.sh` | Permission prompt, or idle about a minute | Shows Windows toast notification via PowerShell |
| `validate-commit.sh` | Before commit | Checks design doc sections, valid JSON, hardcoded values, TODO format |
| `validate-push.sh` | Before push, tag, merge or deploy | Warns on pushes to main, master or release/*, and on `git tag`, `git merge`, `gh release`, `butler push` and `steamcmd +run_app_build` |
| `validate-read.sh` | Before a file read | Refuses a whole-file read of a design doc over 40 KB and answers with its headings |
| `validate-write.sh` | Before a file write | Warns when a write would break a rule the skills state (never blocks) |
| `validate-registry.sh` | Before an entity or TR-ID registry write | Warns when an entry would be deleted or renumbered, or a status is not in the header's list |
| `validate-assets.sh` | After a file write | Checks data-file JSON, and asset naming in Godot's `assets/` |
| `validate-skill-change.sh` | Skill file written | Advises running `/meta-skill-test` after `.claude/skills/` changes |
| `log-agent.sh` | Agent start | Logs agent invocations for audit trail |
| `log-agent-stop.sh` | Agent stop | Completes agent audit trail (start + stop) |
| `validate-agent-artifact.sh` | Agent stop | Warns when a subagent stops without writing the file its brief named |
| `session-stop.sh` | **Every response ends** | Session logging and the subagent spawn tally, in the background. Despite the name it fires once per response, not once per session. |

### Context Resilience

**Session state file:** `production/session-state/active.md` is a living
checkpoint. Update it after each significant milestone. After any disruption
(compaction, crash, `/clear`), read this file first.

**Incremental writing:** When creating multi-section documents, write each
section to file immediately after approval. This means completed sections
survive crashes and context compactions. Previous discussion about written
sections can be safely compacted.

**Automatic recovery:** The `session-start.sh` hook detects and previews
`active.md` automatically, and runs again after every compaction, so the
checkpoint comes back when the conversation is summarised.

**Sprint status tracking:** `production/sprint-status.yaml` is the
machine-readable story tracker. Written by `/plan-sprint` (init) and
`/build-story-done` (status updates). Read by `/plan-sprint-status`, `/studio-next-step`, and
`/build-story-done` (next story). Eliminates fragile markdown scanning.

### Brownfield Adoption

For existing projects that already have some artifacts:

```
/studio-adopt-project
```

Or targeted:

```
/studio-adopt-project gdds
/studio-adopt-project adrs
/studio-adopt-project stories
/studio-adopt-project infra
```

This audits existing artifacts for **format** (not existence), classifies gaps
as BLOCKING/HIGH/MEDIUM/LOW, builds an ordered migration plan, and writes
`docs/adoption-plan-[date].md`. Core principle: MIGRATION not REPLACEMENT --
it never regenerates existing work, only fills gaps.

Individual skills also support retrofit mode:

```
/design-system-gdd retrofit design/gdd/combat-system.md
/arch-adr retrofit docs/architecture/adr-005.md
```

These detect which sections are present vs. missing and fill only the gaps.

### Gate System

Phase gates are formal checkpoints. Run `/review-phase-gate` with the phase you are
entering:

```
/review-phase-gate systems-design       # Concept -> Systems Design
/review-phase-gate technical-setup      # Systems Design -> Technical Setup
/review-phase-gate pre-production       # Technical Setup -> Pre-Production
/review-phase-gate production           # Pre-Production -> Production
/review-phase-gate polish               # Production -> Polish
/review-phase-gate release              # Polish -> Release
```

**Verdicts:**
- **PASS** -- all requirements met, advance to next phase
- **CONCERNS** -- risks found; the stage advances only if you explicitly accept
  them, and the accepted risks are recorded
- **NOT ASSESSED** -- something required could not be checked; the report names
  it, so supply it and re-run
- **FAIL** -- requirements not met, blocks advancement with specific remediation

When a gate passes — or you accept a CONCERNS verdict's risks — `project.stage`
in `project.yaml` is updated (only then; a FAIL never advances it) — mirrored to
`production/stage.txt`. At `standard` and `full` the stage drives
the status line and `/studio-next-step`; at `minimal` they follow the brief and stories
instead.

### Reverse Documentation

For code that exists without design docs (common after brownfield adoption):

```
/design-reverse-document design src/gameplay/combat/
```

Reads existing code and generates GDD-format design documentation from it.

---

## Appendix A: Agent Quick-Reference

### "I need to do X -- which agent do I use?"

| I need to... | Agent | Tier |
|-------------|-------|------|
| Come up with a game idea | `/concept-brainstorm` skill | -- |
| Design a game mechanic | `game-designer` | 2 |
| Design specific formulas/numbers | `systems-designer` | 3 |
| Design a game level | `level-designer` | 3 |
| Design loot tables / economy | `economy-designer` | 3 |
| Build world lore | `world-builder` | 3 |
| Write dialogue | `writer` | 3 |
| Plan the story | `narrative-director` | 2 |
| Plan a sprint | `producer` | 1 |
| Make a creative decision | `creative-director` | 1 |
| Make a technical decision | `technical-director` | 1 |
| Implement gameplay code | `gameplay-programmer` | 3 |
| Implement core engine systems | `engine-programmer` | 3 |
| Implement AI behavior | `ai-programmer` | 3 |
| Implement multiplayer | `network-programmer` | 3 |
| Implement UI | `ui-programmer` | 3 |
| Build dev tools | `tools-programmer` | 3 |
| Review code architecture | `lead-programmer` | 2 |
| Create shaders / VFX | `technical-artist` | 3 |
| Define visual style | `art-director` | 2 |
| Define audio style | `audio-director` | 2 |
| Design sound effects | `sound-designer` | 3 |
| Design UX flows | `ux-designer` | 3 |
| Write test cases | `qa-tester` | 3 |
| Plan test strategy | `qa-lead` | 2 |
| Profile performance | `performance-analyst` | 3 |
| Set up CI/CD | `devops-engineer` | 3 |
| Design analytics | `analytics-engineer` | 3 |
| Check accessibility | `accessibility-specialist` | 3 |
| Plan live operations | `live-ops-designer` | 3 |
| Manage a release | `release-manager` | 2 |
| Manage localization | `localization-lead` | 2 |
| Prototype quickly | `prototyper` | 3 |
| Audit security | `security-engineer` | 3 |
| Communicate with players | `community-manager` | 3 |
| Godot-specific help | `godot-specialist` | 3 |
| GDScript-specific help | `godot-gdscript-specialist` | 3 |
| Godot shader help | `godot-shader-specialist` | 3 |
| GDExtension modules | `godot-gdextension-specialist` | 3 |
| Unity-specific help | `unity-specialist` | 3 |
| Unity DOTS/ECS | `unity-dots-specialist` | 3 |
| Unity shaders/VFX | `unity-shader-specialist` | 3 |
| Unity Addressables | `unity-addressables-specialist` | 3 |
| Unity UI Toolkit | `unity-ui-specialist` | 3 |
| Unreal-specific help | `unreal-specialist` | 3 |
| Unreal GAS | `unreal-gas-specialist` | 3 |
| Unreal Blueprints | `unreal-blueprint-specialist` | 3 |
| Unreal replication | `unreal-replication-specialist` | 3 |
| Unreal UMG/CommonUI | `unreal-umg-specialist` | 3 |

### Agent Hierarchy

```
                    creative-director / technical-director / producer
                                         |
          ---------------------------------------------------------------
          |            |           |           |          |        |       |
    game-designer  lead-prog  art-dir  audio-dir  narr-dir  qa-lead  release-mgr
          |            |           |           |          |        |        |
     specialists  programmers  tech-art  snd-design  writer   qa-tester  devops
     (systems,    (gameplay,             (sound)     (world-  (perf,     (analytics,
      economy,     engine,                           builder)  access.)   security)
      level)       ai, net,
                   ui, tools)
```

**Escalation rule:** If two agents disagree, go up. Design conflicts go to
`creative-director`. Technical conflicts go to `technical-director`. Scope
conflicts go to `producer`.

---

## Appendix B: Slash Command Quick-Reference

### All 74 Commands by Category

#### Onboarding and Navigation (7)

| Command | Purpose | Phase |
|---------|---------|-------|
| `/studio-start` | Guided onboarding, routes to right workflow | Any (first session) |
| `/studio-next-step` | Context-aware "what do I do next?" | Any |
| `/studio-detect-stage` | Full project audit to determine current phase | Any |
| `/studio-setup-engine` | Configure engine, pin version, set preferences | 1 |
| `/studio-adopt-project` | Brownfield audit and migration plan | Any (existing projects) |
| `/studio-settings` | View or change project config (rigor, review mode, ...) | Any |
| `/meta-skill-improve` | Improve a skill via test-fix-retest loop | Any |

#### Game Design (6)

| Command | Purpose | Phase |
|---------|---------|-------|
| `/concept-brainstorm` | Collaborative ideation with MDA analysis | 1 |
| `/design-map-systems` | Decompose concept into systems index | 1-2 |
| `/design-system-gdd` | Guided section-by-section GDD authoring | 2 |
| `/design-quick-spec` | Lightweight spec for small changes | 2+ |
| `/review-gdd-suite` | Cross-GDD consistency and design theory review | 2 |
| `/design-propagate-change` | Find ADRs/stories affected by GDD changes | 5 |

#### UX and Interface (2)

| Command | Purpose | Phase |
|---------|---------|-------|
| `/ux-spec` | Author UX specs (screen/flow, HUD, patterns) | 3-4 |
| `/review-ux` | Validate UX specs for accessibility and GDD alignment | 4 |

#### Architecture (4)

| Command | Purpose | Phase |
|---------|---------|-------|
| `/arch-blueprint` | Master architecture document | 3 |
| `/arch-adr` | Create or retrofit an ADR | 3 |
| `/review-architecture` | Validate all ADRs, dependency ordering | 3 |
| `/arch-control-manifest` | Flat programmer rules from Accepted ADRs | 3 |

#### Stories and Sprints (8)

| Command | Purpose | Phase |
|---------|---------|-------|
| `/plan-epics` | Translate GDDs + ADRs into epics (one per module) | 4 |
| `/plan-stories` | Break a single epic into story files | 4 |
| `/build-story` | Implement a story — routes to the correct programmer agent | 5 |
| `/plan-sprint` | Create or manage sprint plans | 4-5 |
| `/plan-sprint-status` | Quick 30-line sprint snapshot | 5 |
| `/plan-story-readiness` | Validate story is implementation-ready | 4-5 |
| `/build-story-done` | 8-phase story completion review | 5 |
| `/plan-estimate` | Effort estimation with risk assessment | 4-5 |

#### Reviews and Analysis (13)

| Command | Purpose | Phase |
|---------|---------|-------|
| `/review-design-doc` | Validate GDD against 8-section standard | 1-2 |
| `/review-code` | Architectural code review | 5+ |
| `/review-balance` | Game balance formula analysis | 5-6 |
| `/art-asset-audit` | Asset naming, format, size verification | 6 |
| `/art-asset-spec` | Per-asset visual specs and AI generation prompts | 5-6 |
| `/review-content` | GDD-specified content vs. implemented | 5 |
| `/review-consistency` | Cross-GDD entity and formula inconsistency scan | 2+ |
| `/review-scope` | Scope creep detection | 5 |
| `/qa-perf-profile` | Performance profiling workflow | 6 |
| `/review-tech-debt` | Tech debt scanning and prioritization | 6 |
| `/review-phase-gate` | Formal phase gate with PASS/CONCERNS/NOT ASSESSED/FAIL | All transitions |
| `/design-reverse-document` | Generate design docs from existing code | Any |
| `/review-security` | Security vulnerability audit (save, network, input) | 6 |

#### QA and Testing (9)

| Command | Purpose | Phase |
|---------|---------|-------|
| `/qa-test-plan` | Generate QA test plan for a sprint or feature | 5 |
| `/qa-smoke` | Critical path smoke test gate before QA hand-off | 5-6 |
| `/qa-soak` | Soak test protocol for extended play sessions | 6 |
| `/qa-regression` | Map test coverage, identify fixed bugs lacking regression tests | 5-6 |
| `/qa-test-setup` | Scaffold test framework and CI/CD pipeline | 3 |
| `/qa-test-helpers` | Generate engine-specific test helper libraries | 3-5 |
| `/qa-evidence-review` | Quality review of test files and manual evidence | 5 |
| `/qa-flaky-tests` | Detect non-deterministic tests from CI logs | 5-6 |
| `/meta-skill-test` | Validate skill files for structural and behavioral correctness | Any |

#### Production Management (6)

| Command | Purpose | Phase |
|---------|---------|-------|
| `/prod-milestone-review` | Milestone progress and go/no-go | 5 |
| `/prod-retro` | Sprint retrospective analysis | 5 |
| `/qa-bug-report` | Structured bug report creation | 5+ |
| `/qa-bug-triage` | Re-evaluate open bugs for priority, severity, and owner | 5+ |
| `/qa-playtest-report` | Structured playtest session report | 4-6 |
| `/studio-onboard` | Onboard a new team member | Any |

#### Release (6)

| Command | Purpose | Phase |
|---------|---------|-------|
| `/release-checklist` | Pre-release validation | 6 |
| `/release-launch-checklist` | Full cross-department launch readiness | 7 |
| `/release-changelog` | Auto-generate internal changelog | 6 |
| `/release-patch-notes` | Player-facing patch notes | 6 |
| `/release-hotfix` | Emergency fix workflow | 7+ |
| `/release-day-one-patch` | Scoped patch for issues found after gold master | 7+ |

#### Creative (4)

| Command | Purpose | Phase |
|---------|---------|-------|
| `/concept-prototype` | Concept prototype — validate core idea before GDDs | 1 |
| `/art-bible` | Guided Art Bible authoring — visual identity spec | 1-4 |
| `/build-vertical-slice` | Production-quality end-to-end build before Production | 4 |
| `/prod-localize` | String extraction and validation | 6-7 |

#### Team Orchestration (9)

| Command | Purpose | Phase |
|---------|---------|-------|
| `/team-combat` | Combat feature: design through implementation | 5 |
| `/team-narrative` | Narrative content: structure through dialogue | 5 |
| `/team-ui` | UI feature: UX spec through polished implementation | 5 |
| `/team-level` | Level: layout through dressed encounters | 5 |
| `/team-audio` | Audio: direction through implemented events | 5-6 |
| `/team-polish` | Coordinated polish: perf + art + audio + QA | 6 |
| `/team-release` | Release coordination: build + QA + deployment | 7 |
| `/team-live-ops` | Live-ops planning: seasonal events, battle pass, retention | 7+ |
| `/team-qa` | Full QA cycle: strategy, execution, coverage, sign-off | 6-7 |

---

## Appendix C: Common Workflows

### Workflow 1: "I just started and have no game idea"

```
1. /studio-start (routes you based on where you are)
2. /concept-brainstorm (collaborative ideation, pick a concept)
3. /studio-setup-engine (pin engine and version)
4. /review-design-doc on concept doc (optional, recommended)
5. /design-map-systems (decompose concept into systems with deps and priorities)
6. /review-phase-gate systems-design (verify you're ready for Systems Design)
7. /design-system-gdd per system (guided GDD authoring)
```

### Workflow 2: "I have designs and want to start coding"

```
1. /review-design-doc on each GDD (make sure they're solid)
2. /review-gdd-suite (cross-GDD consistency)
3. /review-phase-gate technical-setup
4. /arch-blueprint + /arch-adr (per major decision)
5. /review-architecture
6. /arch-control-manifest
7. /art-bible (sections 1–4 now) + /qa-test-setup + /ux-spec accessibility + /ux-spec patterns
8. /review-phase-gate pre-production
9. /ux-spec per key screen + /review-ux
10. /build-vertical-slice (recommended before committing to epics)
11. /plan-epics layer: foundation + /plan-stories [slug] (define epics, break into stories)
12. /plan-sprint new
13. /review-phase-gate production
14. /plan-story-readiness -> implement -> /build-story-done (story lifecycle)
```

### Workflow 3: "I need to add a complex feature mid-production"

```
1. /design-system-gdd or /design-quick-spec (depending on scope)
2. /review-design-doc to validate
3. /design-propagate-change if modifying existing GDDs
4. /plan-estimate for effort and risk
5. /team-combat, /team-narrative, /team-ui, etc. (appropriate team skill)
6. /build-story-done when complete
7. /review-balance if it affects game balance
```

### Workflow 4: "Something broke in production"

```
1. /release-hotfix "description of the issue"
2. Fix is implemented on hotfix branch
3. /review-code the fix
4. Run tests
5. /release-checklist for hotfix build
6. Deploy and backport
```

### Workflow 5: "I have an existing project and want to use this system"

```
1. /studio-start (choose Path D -- existing work)
2. /studio-detect-stage (determines current phase)
3. /studio-adopt-project (audits existing artifacts, builds migration plan)
4. /design-system-gdd retrofit [path] (fill GDD gaps)
5. /arch-adr retrofit [path] (fill ADR gaps)
6. /review-phase-gate at appropriate transition
```

### Workflow 6: "Starting a new sprint"

```
1. /prod-retro (review last sprint)
2. /plan-sprint new (create next sprint)
3. /review-scope (ensure scope is manageable)
4. /plan-story-readiness per story before pickup
5. Implement stories
6. /build-story-done per completed story
7. /plan-sprint-status for quick progress checks
```

### Workflow 7: "Shipping the game"

```
1. /review-tech-debt (decide what's acceptable at launch)
2. /review-security (the release gate reads the newest report)
3. /prod-localize qa for every language you ship
4. /release-checklist all
5. /release-changelog and /release-patch-notes (drafts; /team-release finalizes them)
6. /review-phase-gate release (verify Polish is complete and the game is ready to release)
7. /release-launch-checklist (full cross-department validation)
8. /team-release (coordinate the release)
9. Ship!
10. /release-hotfix if anything breaks post-launch
11. Post-mortem after launch stabilizes
```

### Workflow 8: "I'm lost / don't know what to do next"

```
1. /studio-next-step (reads your phase, checks artifacts, tells you what's next)
2. If /studio-next-step doesn't help: /studio-detect-stage (full audit)
3. If stage seems wrong: /review-phase-gate at the transition you think you're at
```

---

## Tips for Getting the Most Out of the System

1. **Always start with design, then implement.** The agent system is built
   around the assumption that a design document exists before code is written.
   Agents reference GDDs constantly.

2. **Use team skills for cross-cutting features.** Do not try to manually
   coordinate 4 agents yourself -- let `/team-combat`, `/team-narrative`,
   etc. handle the orchestration.

3. **Trust the rules system.** When a rule flags something in your code, fix
   it. The rules encode hard-won game development wisdom (data-driven values,
   delta time, accessibility, etc.).

4. **Compact proactively.** At ~65-70% context usage, compact or `/clear`.
   Your checkpoint in `active.md` survives it, and `session-start.sh` shows it
   again afterwards. Do not wait until you are at the
   limit.

5. **Use the right tier of agent.** Do not ask `creative-director` to write a
   shader. Do not ask `qa-tester` to make design decisions. The hierarchy
   exists for a reason.

6. **Run /studio-next-step when uncertain.** It reads your actual project state and tells
   you the single most important next step.

7. **Run `/review-design-doc` before handing designs to programmers.** This
   catches incomplete specs early, saving rework.

8. **Run `/review-code` after every major feature.** Catch architectural
   issues before they propagate.

9. **Prototype risky mechanics first.** A day of prototyping can save a week
   of production on a mechanic that does not work.

10. **Keep your sprint plans honest.** Use `/review-scope` regularly. Scope
    creep is the number one killer of indie games.

11. **Document decisions with ADRs.** Future-you will thank present-you for
    recording *why* things were built the way they were.

12. **Use the story lifecycle religiously.** `/plan-story-readiness` before pickup,
    `/build-story-done` after completion. This catches deviations early and keeps
    the pipeline honest.

13. **Write to files early and often.** Incremental section writing means your
    design decisions survive crashes and compactions. The file is the memory,
    not the conversation.
