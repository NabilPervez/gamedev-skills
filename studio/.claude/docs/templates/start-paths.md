# Your Path

Here's your path at rigor `[value]`. Every skill still runs at any rigor; rigor changes
what's required, not what's allowed.

**`minimal`: 4 steps to running code**
1. `/studio-setup-engine`: choose and configure the engine
2. `/concept-brainstorm`: write the one-page `design/game-brief.md`
3. `/plan-stories`: turn the brief's MVP list into stories (no epics or sprint plan needed)
4. `/build-story`: the first line of game code

**`standard`**
- Concept: `/studio-setup-engine` → `/concept-brainstorm` → `/concept-prototype` → `/art-bible` → `/review-phase-gate`
- Systems Design: `/design-map-systems` → `/design-system-gdd` (once per system) → `/review-gdd-suite` →
  `/review-phase-gate`
- Architecture: `/arch-blueprint` → `/arch-adr` (once per decision) →
  `/arch-control-manifest` → `/review-architecture` → `/qa-test-setup` → `/ux-spec`
  (accessibility and interaction patterns) → `/review-phase-gate`
- Pre-Production: `/ux-spec` (HUD and key screens) → `/plan-epics` → `/plan-stories` →
  `/plan-sprint` → `/review-phase-gate`
- Production: `/build-story`

Each `/review-phase-gate` moves the project one stage, and only when it passes.

**`full`:** everything in `standard`, plus `/build-vertical-slice` and `/qa-playtest-report` in
Pre-Production and `/review-design-doc` after each GDD.

**Path D with existing work** (stage `Systems Design` or later, or code on disk) gets this instead.
Print only the steps that apply, and for the brief only the one source that applies. At `minimal`:
1. `/studio-detect-stage`: what stage the project is at and what is missing
2. `/studio-adopt-project`: whether the existing files are in the format the skills read
3. `/studio-setup-engine`: only when no engine is set; leave it out when `engine` names one
4. The brief, only if `concept` is absent: `/design-reverse-document design [code_root]` when the code
   root holds 10 or more source files (it writes the brief from the game), and then do not mention
   `/concept-brainstorm` at all; `/concept-brainstorm` only when it holds fewer

At `standard` and `full`, steps 1 to 3, then `/design-system-gdd retrofit [path]`,
`/arch-adr retrofit [path]`, `/review-architecture` and `/review-phase-gate`.

`minimal` is the documented floor, not a lesser mode. Its trade: no GDDs, so design
problems show up in code.
