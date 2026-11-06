# gamedev-skills

A private, merged game-development skill pack for Claude Code: **155 skills and 50 agents**
covering concept → GDD → tech PRD → sprint plan → build → test → deploy across 12 engines.

- **78 portable skills** from [awesome-gamedev-agent-skills](https://github.com/gamedev-skills/awesome-gamedev-agent-skills) (Apache-2.0), renamed with consistent prefixes
- **74 studio skills + 49 agents** from [Claude Code Game Studios](https://github.com/Donchitos/Claude-Code-Game-Studios) (MIT), renamed by lifecycle phase
- **3 new skills + 1 agent** (original): `game-studio-orchestrator`, `game-design-doc`, `game-tech-prd`

## Layout

```
skills/            Portable skills. Work anywhere, globally or per project.
studio/            Ready-to-copy project template (CLAUDE.md, project.yaml, .claude/ with
                   74 skills, 50 agents, hooks, rules, templates). Studio skills reference
                   .claude/hooks by relative path, so they only work inside this layout.
RENAMES.tsv        Every old → new name (skills and agents).
install.sh         Installer (see below).
scripts/           build.py (re-imports and renames from upstream), validate.py (checks names,
                   descriptions, leftover old references and broken skill paths).
THIRD_PARTY/       Upstream licenses and NOTICE, verbatim.
```

## Install

```bash
# Core only, available in every project (recommended global install)
./install.sh --global              # orchestrator, GDD, tech PRD, engine router

# A new game repo: full studio + all portable skills
./install.sh --project ~/games/strike-lattice

# Same, but keep only one engine family's skills (saves context)
./install.sh --project ~/games/strike-lattice --engine threejs

# Then
cd ~/games/strike-lattice && claude --agent game-studio-orchestrator
```

**Why not install everything globally?** Claude Code lists skill descriptions in about 1% of the
context window and drops the least-used ones when the list overflows, so they stop triggering.
150+ skills will overflow it. Install core globally, and the rest per project.

## How the orchestrator works

`game-studio-orchestrator` runs in the main conversation (Claude Code docs say subagents can't
spawn subagents), reads the repo to detect the phase, and calls skills in order:

| Phase | Studio mode | Lite mode (portable skills only) |
|---|---|---|
| Concept | `concept-brainstorm` → `game-design-doc` (one-page) | `game-design-doc` |
| Prototype | `concept-prototype` / `build-greybox-prototype` | `build-greybox-prototype` |
| GDD | `game-design-doc` → `design-map-systems` → `design-system-gdd` → `review-design-doc` | `game-design-doc` |
| Tech PRD | `game-tech-prd` → `arch-adr` → `studio-setup-engine` → `arch-blueprint` → `review-architecture` | `game-tech-prd` → `engine-skill-router` |
| Sprint | `plan-epics` → `plan-stories` → `plan-estimate` → `plan-sprint` (with DoD) | sprint file with DoD |
| Build | `build-story` + engine/`dev-*`/`genre-*` via `engine-skill-router`; `team-*` | engine + `dev-*` + `genre-*` |
| Test | `review-code` → `qa-smoke` → `build-story-done`; `review-phase-gate` | DoD check, `dev-performance` |
| Deploy | `release-checklist` → export → `release-steam` / `release-itch` → `release-launch-checklist` | export → `release-*` |

Studio mode is detected automatically when `.claude/skills/review-phase-gate/` exists.
Rigor follows `project.yaml` → `modes.rigor` (default `minimal`: a one-page brief is enough).

## Naming scheme

| Prefix | Meaning | Prefix | Meaning |
|---|---|---|---|
| `godot-` `unity-` `unreal-` `phaser-` `threejs-` `roblox-` … | engine | `plan-` | epics, stories, sprints |
| `dev-` | cross-engine craft | `build-` | implementing stories / slices |
| `genre-` | genre kits | `review-` | reviews and gates |
| `studio-` | project setup / navigation | `qa-` | testing |
| `concept-` | ideation, prototype | `prod-` | retros, milestones, localization |
| `design-` `art-` `ux-` | design docs | `release-` | shipping |
| `arch-` | architecture, ADRs | `team-` `meta-` | multi-agent teams, skill tooling |

Full map: [`RENAMES.tsv`](RENAMES.tsv). Highlights: `router` → `engine-skill-router`,
`/gate-check` → `/review-phase-gate`, `/dev-story` → `/build-story`, `/help` → `/studio-next-step`,
`ue-*-specialist` → `unreal-*-specialist`. Skill bodies and descriptions are unchanged apart from
updated cross-references.

## Updating from upstream

```bash
git clone --depth 1 https://github.com/NabilPervez/awesome-gamedev-agent-skills.git ../src-agds
git clone --depth 1 https://github.com/NabilPervez/Claude-Code-Game-Studios.git ../src-ccgs
python3 -I scripts/build.py ..     # rebuilds imports; original files are preserved
python3 -I scripts/validate.py .   # must report 0 problems
```
Add any new upstream skill to the rename maps in `scripts/build.py` first.

## Licenses

Original material: MIT ([LICENSE](LICENSE)). `skills/` imports: Apache-2.0, each modified file
carries a change notice. `studio/`: MIT (Donchitos). See [NOTICE](NOTICE) and `THIRD_PARTY/`.

## Known limits

- Studio skill descriptions were kept as upstream wrote them; only names changed.
- `studio-tests/` specs were renamed to match, but upstream's `/meta-skill-test` runs were not
  re-executed after renaming. Run `/meta-skill-test static all` in a project to confirm.
- Nested subagents may be supported in newer Claude Code versions; the orchestrator doesn't rely on it.
