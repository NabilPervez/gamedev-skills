---
name: game-studio-orchestrator
description: Orchestrates end-to-end game development by detecting the project's current phase and calling the right skills and agents in order, from concept to GDD, technical PRD, sprint plan with Definition of Done, build, test and deploy. Use when the user says "make a game", "plan my game", "what's next" on a game project, "take this from idea to release", or asks which game-dev skill or agent to use.
---

# Game Studio Orchestrator

You coordinate; specialist skills and agents do the work. Run in the **main conversation**.
Invoke skills one at a time, delegate self-contained work to subagents, and keep decisions,
gates and user dialogue yourself. Never ask a subagent to orchestrate other subagents.

## 0. Rules

- **The user decides** at every branch: give 2–4 options with trade-offs. Ask before writing files.
- **Respect rigor.** Read `project.yaml` → `modes.rigor` (default `minimal`). Don't create
  documents the current rigor doesn't require; extra docs cost time and don't improve the game.
- **One phase at a time.** Don't start a phase until the previous gate passes or the user
  overrides it; record overrides in `production/decisions.md`.
- **Engine first, then code.** Once an engine is pinned, invoke `engine-skill-router` before
  any game code so the right engine, `dev-*` and `genre-*` skills load.
- **Report after every step:** phase · files produced · gate status · the one recommended next skill.

## 1. Detect the mode

- **Studio mode** — `.claude/skills/review-phase-gate/` exists (the `studio/` template is
  installed). Use the full routing in section 3, including agents and `team-*` skills.
- **Lite mode** — only the portable `skills/` pack. Use the Lite column; you play the producer.

## 2. Detect the phase (read the repo, don't guess)

| Signal | Phase |
|---|---|
| no `design/` | P1 Concept |
| `design/game-brief.md`, no prototype verdict | P2 Prototype |
| verdict PROCEED, no `design/gdd/` and rigor ≥ standard | P3 GDD |
| GDD/brief approved, no `docs/tech-prd.md` | P4 Tech PRD |
| tech PRD approved, no `production/sprints/` | P5 Sprint plan |
| active sprint file | P6 Build ↔ P7 Test |
| milestone = release candidate | P8 Deploy |

Ambiguous? In Studio mode run `studio-detect-stage`; then confirm with the user.
At `minimal` rigor, P3 is skipped: the one-page brief is the GDD.

## 3. Pipeline and routing

| Phase | Studio mode (in order) | Agents | Lite mode | Gate to exit |
|---|---|---|---|---|
| P1 Concept | `concept-brainstorm` → `game-design-doc` (one-page) | creative-director | `game-design-doc` (one-page) | Pitch, pillars, core loop, platforms approved |
| P2 Prototype | `concept-prototype` (or `build-greybox-prototype` in-engine, after `engine-skill-router`) | prototyper, game-designer | `build-greybox-prototype` | PROCEED / PIVOT / KILL recorded |
| P3 GDD | `game-design-doc` (living-gdd) → `design-map-systems` → `design-system-gdd` per system → `review-design-doc`; `art-bible`, `ux-spec` as needed | game-designer, systems-designer, economy-designer, art-director, ux-designer | `game-design-doc` (living-gdd / system-spec) | `review-gdd-suite` no blockers |
| P4 Tech PRD | `game-tech-prd` → `arch-adr` (engine) → `studio-setup-engine` → `arch-blueprint` → `review-architecture` | technical-director, lead-programmer, performance-analyst | `game-tech-prd` → `engine-skill-router` | All GDD IDs traced; budgets numeric; engine ADR written |
| P5 Sprint plan | `plan-epics` → `plan-stories` → `plan-estimate` → `plan-story-readiness` → `plan-sprint` | producer | Write `production/sprints/sprint-NN.md` (section 4) | Goal, capacity, ready stories, DoD included |
| P6 Build | `build-story` per story (engine + `dev-*` + `genre-*` via `engine-skill-router`); `team-*` for multi-discipline features | gameplay/engine/ui/ai/network programmers, engine specialists | Engine skills via `engine-skill-router`, plus `dev-*` / `genre-*` | Story acceptance criteria met |
| P7 Test | `review-code` → `qa-smoke` → `build-story-done`; per milestone `qa-test-plan`, `qa-regression`, `qa-perf-profile`, `qa-playtest-report`, `qa-bug-triage`, `review-phase-gate` | qa-lead, qa-tester, performance-analyst | Check every DoD item from `docs/tech-prd.md` §15; `dev-performance` vs budgets | DoD met; milestone gate PASS |
| P8 Deploy | `release-checklist` → `release-changelog` / `release-patch-notes` → export (`godot-export`, `unity-build`, `unreal-packaging`) → `release-steam` / `release-itch` / web host → `release-launch-checklist` | release-manager, devops-engineer | Export skill → `release-steam` / `release-itch` / web host | Go/no-go recorded; build live; rollback path known |
| Ongoing | `prod-retro` after each sprint · `design-propagate-change` when design shifts · `release-hotfix` for emergencies · `plan-game-jam` for jams | producer | Short retro in the sprint file | — |

## 4. Sprint plan format (`production/sprints/sprint-NN.md`)

Goal (one sentence) · dates · capacity · stories (ID, title, GDD/TR IDs, estimate marked as
estimate, owner, acceptance criteria) · risks · **Definition of Done** (copied from
`docs/tech-prd.md` §15; change only with user approval) · demo plan.
Done is binary: a story missing any DoD item is not done. Push to git at each sprint completion.

## 5. Delegation pattern

- **Subagents** for context-heavy, self-contained work: code review, test-evidence review,
  performance analysis, codebase exploration, research. Give a precise brief and the output path.
- **Main thread** keeps decisions, gates and user dialogue.
- For multi-agent features, call the matching `team-*` skill instead of improvising a roster.

## 6. Skill map (quick reference)

- **Docs:** `game-design-doc`, `game-tech-prd`
- **Routing:** `engine-skill-router` (engines: `godot-*`, `unity-*`, `unreal-*`, `phaser-*`,
  `pixijs-core`, `threejs-*`, `bevy-ecs`, `defold-core`, `love2d-core`, `pygame-core`,
  `ebitengine-core`, `roblox-*`)
- **Craft:** `dev-*` (feel, camera, input, AI, procgen, save, audio, shaders, physics, HUD,
  performance, level blockout, art assets, dialogue)
- **Genres:** `genre-*` · **Workflow:** `plan-game-jam`, `build-greybox-prototype`,
  `release-steam`, `release-itch`
- **Studio (template only):** `studio-*`, `concept-*`, `design-*`, `art-*`, `ux-*`, `arch-*`,
  `plan-*`, `build-*`, `review-*`, `qa-*`, `prod-*`, `release-*`, `team-*`, `meta-*`
