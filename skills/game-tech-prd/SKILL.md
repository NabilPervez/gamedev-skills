---
name: game-tech-prd
description: Writes an engine-agnostic technical PRD (technical design document) for a game, turning an approved GDD into platforms, engine choice, architecture, data and save formats, content pipeline, measurable performance budgets, networking, testing, CI/CD, risks, milestones and a Definition of Done, with traceability back to GDD requirement IDs. Use when the user asks for a TDD, tech spec, technical PRD, architecture plan, performance budget or engine decision for a game, or before sprint planning. Not for game-design content; use game-design-doc.
---

# Technical PRD for Games (engine-agnostic)

Define HOW the game in the approved GDD will be built, what it must run on, and how the team
will know it is done. Every requirement traces to a GDD ID; every budget is a number.

## 1. Preconditions

- An approved `design/game-brief.md` or `design/gdd/` exists. If not, stop and recommend
  `game-design-doc`.
- Pillars, core loop and target platforms are not `OPEN:`. If they are, list them as blockers.

## 2. Workflow

1. **Trace.** Read the GDD; pull every `GDD-<SYS>-NN` into the traceability table (section 3, §2).
   If the GDD has no IDs, assign them and tell the user.
2. **Ask only for missing technical facts:** platforms and min-spec hardware, engine preference
   or constraints, team skills, online needs, budget/timeline, store/compliance requirements.
3. **Engine decision** (if undecided): present 2–4 options scored against the requirements —
   platforms, 2D/3D, team language skills, licensing/cost, tooling, web export. The user decides.
   Record it as an ADR (`docs/adr/ADR-0001-engine.md`: context, options, decision, consequences).
4. **Draft** the template, scaled to project size (a jam game may need 2 pages; skip sections
   that don't apply and say so).
5. **Show the draft;** ask "May I write this to `docs/tech-prd.md`?" before writing.
6. **Run the checklist** (section 6), then hand off to sprint planning.
7. **Once the engine is pinned,** recommend `engine-skill-router` so engine skills load.

## 3. Template (`docs/tech-prd.md`)

1. **Summary** — product, goals, non-goals, success metrics; links to GDD version and ADRs
2. **Requirements traceability** — `| GDD ID | Tech requirement (TR-NN) | Module | Test | Status |`
3. **Platforms and targets** — platforms, min/recommended spec, input devices,
   resolutions/aspect ratios, store/cert rules, accessibility and localization requirements
4. **Engine, language, versions** — pinned engine version, language, middleware/plugins,
   licensing, upgrade policy
5. **Architecture** — context diagram (Mermaid), module boundaries and owners, game loop and
   update order, state management, event/messaging pattern, scene/level loading, dependency rules
   (e.g. "UI never owns game state")
6. **Data and persistence** — data-driven config (where tuning tables live), content schemas,
   save format, versioning and migration, cloud sync, analytics event schema
7. **Networking** (if any) — topology, authority model, tick/replication rate, latency
   tolerance, anti-cheat, backend services
8. **Content and tool pipeline** — source → import → runtime formats, naming conventions,
   asset budgets, editor tools to build, version control incl. large files
9. **Performance budgets** — per platform, each with a number and a measurement method:
   frame time (16.6 ms @ 60 fps / 33.3 ms @ 30 fps) split CPU/GPU by subsystem, memory ceiling,
   load times, build/download size, draw calls/entity counts, battery/thermal on mobile
10. **Quality strategy** — unit/integration/visual/perf/soak tests, automation level, test
    devices, playtest cadence, crash reporting
11. **Build, release, deploy** — CI pipeline, branching, build configs, versioning,
    distribution (Steam, itch, app stores, web/Netlify), rollback/hotfix path
12. **Security, privacy, compliance** — PII, age ratings, platform policies, licenses
13. **Risks** — `| Risk | Likelihood | Impact | Mitigation / spike | Owner | Due |`
14. **Milestones** — prototype → vertical slice → alpha (feature complete) → beta (content
    complete) → release, each with exit criteria
15. **Definition of Done** (section 4) and story acceptance-criteria rules
16. **Open questions and ADR log**

## 4. Default Definition of Done (edit per project, with user approval)

- Builds in CI for every target platform with zero new errors or warnings
- Acceptance criteria for linked GDD/TR IDs pass; automated tests for logic pass
- Player-visible changes were run, observed and evidenced (screenshot or clip)
- Within performance budgets on min-spec hardware for the affected scene
- No hard-coded tuning values; strings localization-ready; input works on all target devices
- Code reviewed; GDD, tech PRD or ADR updated if behavior or architecture changed
- Merged to main and pushed; changelog entry written

## 5. Rules

- Engine-agnostic until an ADR pins the engine; after that, name engine features explicitly.
- Every budget has a number, a platform and a measurement method.
- Every TR traces to a GDD ID or an explicit technical need (tooling, compliance).
- Write decisions with rationale, not descriptions; flag which choices are hard to reverse.
- Mark estimates as estimates.

## 6. Quality checklist

- [ ] Traceability covers 100% of GDD requirement IDs
- [ ] Platforms, min-spec and budgets are numeric and testable
- [ ] Architecture diagram and module owners exist
- [ ] Save/data versioning strategy defined
- [ ] Top 5 risks each have a spike or mitigation with owner and date
- [ ] Milestones have exit criteria; Definition of Done is explicit
