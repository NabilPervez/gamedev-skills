---
name: game-design-doc
description: Writes and maintains engine-agnostic game design documents, scaling from a one-page concept brief to a modular living GDD covering pillars, core loop, mechanics, progression, content, UX, art and audio direction, scope and cut list. Use when the user asks for a GDD, game design doc, one-pager, concept doc, design pillars or core loop, or wants to update the design after a playtest. Not for engine, architecture or performance decisions; use game-tech-prd for those.
---

# Game Design Document (engine-agnostic)

Produce the single source of truth for WHAT the game is and WHY. Keep it short enough that
people actually read it, and update it whenever the game changes.

Evidence for staying lean: in Claude Code Game Studios' own four-build experiment, the build
that wrote 30 documents before code ranked last in blind review and playtest. Stone Librande's
GDC 2010 "One-Page Designs" talk makes the same point. Documents are a cost, not a quality
guarantee.

## 1. Choose the depth first (ask if unclear)

| Mode | When | Output | Length |
|---|---|---|---|
| one-page | jam, solo, pitch, pre-prototype | `design/game-brief.md` | 1 page |
| living-gdd | a prototype proved the core loop (PROCEED) | `design/gdd/index.md` + one file per system | 5–15 focused pages |
| system-spec | one system needs detail | `design/gdd/systems/<system>.md` | 1–3 pages |

Default to **one-page**. Escalate only after a PROCEED verdict or when the user asks.

## 2. Workflow

1. **Gather inputs.** Read any existing `design/`, prototype notes, playtest reports, references.
   Ask at most 5 questions at a time. Never invent the core fantasy, audience or platform.
2. **Draft** the sections for the chosen mode. Mark unknowns `OPEN:` with an owner. Never pad.
3. **Show the draft** and ask "May I write this to `<path>`?" before writing files.
4. **Run the quality checklist** (section 6). Fix failures before handing off.
5. **Append to the Change Log** at the bottom: date, what changed, why, evidence.
6. **Hand off:** once pillars, core loop and platforms are approved, recommend `game-tech-prd`.

## 3. One-page template (`design/game-brief.md`)

- **Title · one-sentence pitch · genre · target platforms · target audience**
- **Core fantasy** — what the player feels
- **Design pillars (3–5)** — each phrased as a tie-breaker ("Readable over realistic")
- **Core loop** at three time scales: every ~30 seconds, every session, across sessions
- **Key mechanic(s)** and what makes them distinct; 2–3 comparable titles and the difference
- **Look and feel** — 3 adjectives, reference links, audio mood
- **Scope** — MVP feature list, explicit NOT-doing list, target length, team, timeline
- **Biggest design risk** and the prototype question that tests it

## 4. Living GDD template (`design/gdd/index.md` links to per-system files)

0. **Overview** — the one-pager, kept current; version, owner, last-updated date
1. **Player experience goals** — pillars, target emotions, audience, accessibility goals
2. **Core loop and session structure** — loop diagram (Mermaid fine), session length, fail/retry
3. **Mechanics and systems** — one System Spec per system (section 5)
4. **Progression and economy** — curves, currencies, sources/sinks table, pacing chart
5. **Content** — worlds/levels list; enemies/items/cards tables; content volume targets
6. **Narrative** (if any) — premise, characters, structure, tone
7. **UX and controls** — input map per device, HUD/menu flow, onboarding/tutorial plan
8. **Art and audio direction** — references, palette, readability rules, music/SFX direction
9. **Monetization and live plans** (if any) — model, ethics constraints, cadence
10. **Scope, milestones, cut list** — MVP / vertical slice / content-complete; what was cut and why
11. **Open questions and risks** — each with the prototype or playtest that resolves it
12. **Change Log** — dated entries; never silently rewrite history

## 5. System Spec template (one per system)

| Field | Content |
|---|---|
| Objective | Which pillar this system serves |
| Player-facing rules | Plain-language rules |
| Inputs → outcomes | What the player does and what happens |
| Feedback | Visual / audio / haptic response |
| Failure and edge cases | What breaks, what's ambiguous |
| Tuning table | name · default · range · owner |
| Dependencies | Other systems it reads or writes |
| Acceptance criteria | Testable, player-observable statements |
| Requirement IDs | `GDD-<SYS>-NN` — traced by the tech PRD |

## 6. Rules

- **Engine-agnostic:** describe behavior and feel, not nodes, classes or engine APIs.
- **Every number lives in a tuning table**, never buried in prose.
- **Every mechanic names the pillar it serves**; cut mechanics that serve none.
- Prefer tables, diagrams and short bullets; link instead of duplicating.
- Acceptance criteria are observable in play ("player can jump within 150 ms of leaving a
  ledge"), not implementation tasks.

## 7. Quality checklist

- [ ] Pitch fits one sentence; 3–5 pillars, each resolving a real trade-off
- [ ] Core loop explicit at three time scales
- [ ] MVP and NOT-doing lists exist; scope fits team and timeline
- [ ] Each system has rules, edge cases, tuning table, acceptance criteria with IDs
- [ ] Every `OPEN:` item has an owner and a resolving test
- [ ] Change Log updated with today's date
