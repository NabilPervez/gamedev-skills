---
name: engine-skill-router
description: >
  Routes any game-development request to the right specialized skill(s): it detects the engine
  (Godot, Unity, Unreal, Ebitengine, Bevy, Phaser, PixiJS, three.js, Defold, LÖVE, pygame, Roblox) and the task, then
  reads the chosen skill before acting. Use to make a game or to decide which skill applies — for
  players, levels, enemies, shaders, art direction, sprites, tiles, textures, 3D assets, UI/UX,
  cameras, game feel, physics, input, audio, saving, multiplayer, AI, dialogue, procedural
  generation, or performance, for genres (platformer,
  roguelike, RPG, FPS, tower-defense, card game, visual novel, survival-crafting, puzzle), and for
  shipping (game jam, Steam, itch). Start here
  when unsure which gamedev skill to use.
---

> Modified by Nabil Pervez, 2026: renamed from `router`; skill references updated. Original © Abhishek Barali and the awesome-gamedev-agent-skills contributors, Apache-2.0 (see THIRD_PARTY/).

# Master Router — Game-Development Skill Dispatcher

The entry point for game-development work. It fingerprints the project to pick **one** engine,
classifies the task from the request, names the **minimal** set of specialized skills, and tells
you to read them before acting. It **dispatches and composes** — it does not re-teach engine APIs.

## When to use

- Use at the **start of any game-development request** — building or debugging a game, level,
  player, enemy, shader, UI, save system, multiplayer, input, audio, AI, dialogue, procedural
  content, or visual asset set — to decide which skill(s) to load.
- Use when the user names an engine or genre, says "make a game", or asks "which skill should I
  use?".

**When *not* to use:** once the right skill is loaded and the task is squarely inside it, work
from that skill — don't re-run the router every turn. Re-route only when the task **pivots** to a
new engine or concern (router step 6).

## Routing algorithm

1. **Detect engine and version** — project fingerprint → at most one engine skill set (or
   "unknown"), then read the project's version source. §1.
2. **Classify task** — phrasing → discipline(s) + at most one genre + workflow(s). §2.
3. **Resolve** — the minimal set: engine skill(s) + discipline(s) + genre + workflow(s). §3.
4. **Read (disclosure)** — open only the chosen `SKILL.md` bodies; `references/` only on demand. §4.
5. **Compose** — order: engine fundamentals → discipline concept → genre glue → workflow. §5.
6. **Fallback** — preserve existing engines, including custom/proprietary ones; bind missing APIs
   from project evidence and state any gap. For a new project with no engine preference, see §6.

---

## 1. Engine detection (project fingerprint)

Scan for the highest-confidence signal; **choose exactly one** engine for the target project.
An explicitly identified custom/proprietary engine is a valid result even without a catalog skill.
Check the target's build and runtime entry point before treating a bundled library/tool as its engine.

| # | Engine | Primary signal | Skill set root |
|:-:|--------|----------------|----------------|
| 1 | Godot | `project.godot` | `skills/godot/` |
| 2 | Unreal | `*.uproject` | `skills/unreal/` |
| 3 | Unity | `Assets/` **and** `ProjectSettings/ProjectVersion.txt` | `skills/unity/` |
| 4 | Ebitengine | `go.mod` requiring `github.com/hajimehoshi/ebiten/v2` | `skills/ebitengine/` |
| 5 | Bevy | `Cargo.toml` with a `bevy` dependency | `skills/other-engines/bevy-ecs/` |
| 6 | Phaser | `package.json` dep `phaser` | `skills/web-engines/phaser-*` |
| 7 | PixiJS | `package.json` dep `pixi.js` | `skills/web-engines/pixijs-rendering/` |
| 8 | three.js | `package.json` dep `three` | `skills/web-engines/threejs-*` |
| 9 | Defold | `game.project` | `skills/other-engines/defold-core/` |
| 10 | LÖVE | `conf.lua` / `main.lua` calling `love.*` | `skills/other-engines/love2d-core/` |
| 11 | pygame | `*.py` with `import pygame` | `skills/other-engines/pygame-core/` |
| 12 | Roblox | `*.rbxl(x)` / `*.project.json` (Rojo) | `skills/other-engines/roblox-*` |

For secondary signals, the Godot-C#/Unity/Bevy, Defold/LÖVE/Lua and multi-web disambiguation
rules, monorepos, and plain-text engine mentions, read `references/engine-detection.md`.

After identifying the engine, read its version from project metadata or dependency locks before
choosing APIs. Existing projects keep their pinned version unless migration is requested; the
catalog baseline is only for new projects. The exact version sources are in the detection reference;
each engine skill states its new-project baseline, and the catalog-wide table is
`docs/VERSION-SUPPORT.md` in the source repository (it is not installed with the router).

## 2. Task classification (phrasing → category)

After the engine, read the request for task signals (three **additive** categories):

- **disciplines** (cross-engine concepts): `dev-art-assets`, `dev-npc-ai`, `dev-behavior-trees-utility-ai`, `dev-procgen`, `dev-dialogue`,
  `dev-save-system`, `dev-audio-mixing`, `dev-shaders`, `dev-physics-tuning`, `dev-level-blockout`,
  `dev-input`, `dev-game-feel`, `dev-camera`, `dev-hud-menus`, `dev-performance`.
  Triggered by concept words ("sprite sheet", "art direction", "texture", "pathfinding",
  "save slots", "fragment shader", "screen shake", "camera follow", "HUD/menu",
  "optimize/low FPS").
- **genres** (whole-game templates): `genre-platformer`, `genre-roguelike`, `genre-rpg`, `genre-fps`,
  `genre-tower-defense`, `genre-card-game`, `genre-visual-novel`, `genre-survival-crafting`, `genre-puzzle`. Triggered by genre
  words ("make a roguelike", "deckbuilder").
- **workflows** (process/shipping): `plan-game-jam`, `build-greybox-prototype`, `release-steam`,
  `release-itch`. Triggered by process words ("publish on Steam", "vertical slice").

File signals sharpen this: `*.yarn`/`*.ink` → `dev-dialogue`/`genre-visual-novel`; `steam_appid.txt`
→ `release-steam`; `*.inputactions` → `unity-input`.

## 3. Routing table (task → category → skill)

### 3a. Engine skills — read the one matching the detected engine + sub-task

- **Godot** (`skills/godot/`): language `godot-gdscript` / `godot-csharp`; structure
  `godot-scenes`, `godot-signals`; 2D `godot-2d-movement`, `godot-tilemap`; 3D
  `godot-3d`; physics `godot-physics`; UI `godot-ui`; animation
  `godot-animation`; shaders `godot-shaders`; data `godot-resources`; audio `godot-audio`;
  netcode `godot-multiplayer`; headless CLI tests `godot-headless-tests`; ship
  `godot-export`.
- **Unity** (`skills/unity/`): scripting `unity-csharp`; input `unity-input`;
  physics `unity-physics`; animation `unity-animation`; data `unity-scriptable-objects`; 2D
  `unity-tilemap-2d`; AI nav `unity-navmesh`; ship `unity-build`.
- **Unreal** (`skills/unreal/`): visual scripting `unreal-blueprints`; C++ gameplay
  `unreal-cpp`; input `unreal-enhanced-input`; AI `unreal-behavior-trees`; VFX
  `unreal-niagara`; ship `unreal-packaging`.
- **Ebitengine** (`skills/ebitengine/`): `ebitengine-core` for Go 2D games and focused
  input, rendering, text, audio, state/testing and build work. Select only its relevant
  references; generating the starter is optional for an existing project.
- **Web** (`skills/web-engines/`): `phaser-core`, `phaser-arcade-physics`; `pixijs-core`;
  `threejs-scene`, `threejs-gltf`, `threejs-materials-lighting`.
- **Other** (`skills/other-engines/`): `bevy-ecs`, `pygame-core`, `love2d-core`; Defold
  `defold-core` (collections, game objects, scripts, input, messages, factories, proxies,
  Bob builds); Roblox foundation
  `roblox-luau`, persistence `roblox-datastores`, UI `roblox-ui`, remotes/security
  `roblox-networking`, character lifecycle `roblox-characters`, simulation/queries
  `roblox-physics`, in-Studio operation `roblox-studio`, and simulator/tycoon/idle
  economy balancing `roblox-economy`.

### 3b. Disciplines — load **with** the engine skill (concept ↔ engine API)

| Concept (`says:`) | Discipline skill | Pairs with (engine API) |
|-------------------|------------------|-------------------------|
| art direction, game assets, sprites, tilesets, textures, icons, 3D props | `dev-art-assets` | engine importer/rendering skill; `imagegen` when available |
| enemy AI, behavior tree, pathfinding, steering | `dev-npc-ai` | `unity-navmesh` / `unreal-behavior-trees` / Godot nav |
| BT runtime, blackboard, decorator, selector/sequence, utility AI, response curve, consideration | `dev-behavior-trees-utility-ai` | `dev-npc-ai` (model choice) / `unreal-behavior-trees` (engine assets) |
| procedural, noise, seed, dungeon generator, WFC | `dev-procgen` | engine tilemap/grid skill |
| dialogue, Yarn, Ink, conversation tree | `dev-dialogue` | engine UI skill |
| save/load, slots, persistence | `dev-save-system` | `roblox-datastores` / engine IO |
| adaptive music, mixer, ducking, SFX | `dev-audio-mixing` | `godot-audio` / Unity AudioMixer |
| shader, fragment, dissolve/outline | `dev-shaders` | `godot-shaders` / engine material |
| jitter, tunneling, fixed timestep | `dev-physics-tuning` | `godot-physics` / `unity-physics` |
| whitebox, blockout, tile layout, pacing | `dev-level-blockout` | `godot-tilemap` / `unity-tilemap-2d` |
| rebind, gamepad, input buffering | `dev-input` | `unity-input` / `unreal-enhanced-input` / Godot InputMap |
| screen shake, hit-stop, juice, squash & stretch, "make it punchy" | `dev-game-feel` | engine animation/tween + `dev-camera` (shake) |
| camera follow, deadzone, look-ahead, orbit, first-person | `dev-camera` | `godot-2d-movement` / `godot-3d` / Cinemachine |
| HUD, menu, UI layout, scaling, safe area, focus nav | `dev-hud-menus` | `godot-ui` / Unity UI (UGUI/UI Toolkit) |
| low FPS, optimize, draw calls, GC spike, pooling, profiler | `dev-performance` | engine profiler + `dev-physics-tuning` |

For Roblox, compose cross-engine concepts with the focused engine skill: HUD/menu requests use
`roblox-ui` + `dev-hud-menus` (+ `dev-input` for gameplay bindings); remote exploit or
replication requests use `roblox-networking` + `roblox-luau`; respawn/rig requests use
`roblox-characters`; physical simulation/query requests use `roblox-physics` (+
`dev-physics-tuning` for stability); simulator, tycoon, clicker or idle economy requests (upgrade
costs, rebirths, offline earnings, big numbers, paid eggs/crates odds) use
`roblox-economy` + `roblox-networking` (+ `roblox-datastores` for saving); direct place
editing also uses `roblox-studio`.

For Ebitengine, bind engine-specific slots to `ebitengine-core` and its relevant reference
(input, rendering, text/UI, audio, gameplay, tilemaps or state/testing). Add only the needed
disciplines; do not load Godot or Unity APIs from a genre's example bindings. Native 3D and a
ready-made network backend are not supplied by this 2D skill; state those gaps when relevant.

For Defold, bind engine-specific slots (movement, input, spawning, level loading, build) to
`defold-core` and add only the needed disciplines, e.g. "add player movement to my Defold
game" → `defold-core` + `dev-input` (+ `genre-platformer` for a platformer). Defold has no
dedicated GUI, tilemap or physics skill yet; use `defold-core` and its build reference's
pointers, and state the gap.

### 3c. Genres — **compose** engine + disciplines (bind `*` to the detected engine)

| Genre (`says:`) | composes |
|-----------------|----------|
| platformer, jump, double jump | `godot-2d-movement` (or engine physics) + `godot-tilemap`/`unity-tilemap-2d` + `dev-level-blockout` + `dev-camera` + `dev-game-feel` |
| roguelike, procedural dungeon, permadeath | `dev-procgen` + `godot-tilemap`/`unity-tilemap-2d` + `dev-npc-ai` + `dev-save-system` + `dev-game-feel` |
| RPG, stats, inventory, quests | `godot-resources`/`unity-scriptable-objects` + `dev-dialogue` + `dev-save-system` + `dev-hud-menus` |
| FPS, first-person, hitscan | `godot-3d`/`unreal-cpp` + `dev-input` + `dev-npc-ai` + `dev-camera` + `dev-game-feel` |
| tower defense, waves, lanes | `dev-npc-ai` + engine movement + `dev-level-blockout` + `dev-hud-menus` |
| card game, deckbuilder, TCG | `godot-resources`/`unity-scriptable-objects` + `dev-hud-menus` (+ engine UI) |
| visual novel, branching story | `dev-dialogue` + `dev-save-system` + `dev-hud-menus` |
| survival, crafting, gathering | `dev-save-system` + `godot-resources`/`unity-scriptable-objects` + `dev-procgen` + `dev-hud-menus` |
| puzzle, match-3, grid logic | `godot-tilemap`/`unity-tilemap-2d` + `dev-level-blockout` + `dev-game-feel` |

### 3d. Workflows — engine-independent process & shipping

`plan-game-jam` (jam, 48-hour, Ludum Dare/GMTK) · `build-greybox-prototype` (vertical slice, MVP, greybox) ·
`release-steam` (Steam, Steamworks, depot; `steam_appid.txt`) · `release-itch` (itch.io, butler;
`.itch.toml`).

For the exhaustive per-skill trigger list and every engine binding, read
`references/routing-table.md`.

## 4. Read protocol (progressive disclosure)

1. **Preloaded:** only each skill's `name` + `description` are in context. Decide from those plus
   the fingerprint — do **not** pre-read bodies.
2. **On selection:** read the body of **each chosen** `skills/<category>/<name>/SKILL.md` — and
   only those. Never bulk-load a whole category.
3. **On demand:** read a skill's bundled `references/` files only when the subtask needs that
   depth (the skill body says when).
4. **Re-route on pivot:** if the task changes (movement → saving), select and read the newly
   relevant skill instead of keeping everything loaded.

Announce what you load and why, e.g.: *"Detected Godot (`project.godot`). Loading
`godot-2d-movement` for the controller and `genre-platformer` for jump feel; will open the platformer
skill's `feel-tuning.md` reference if you want coyote-time/buffering."*

## 5. Composition rules

- **One engine, additive concepts.** Use its engine skill set when available; for an unsupported
  engine, use project evidence as the API binding instead. Add the disciplines the
  task needs and usually **at most one** genre. Workflows attach independently.
- **Order:** engine fundamentals → discipline concept → genre orchestration → workflow. For asset
  production, approve the visual target before generating a family, then finish with the engine
  import settings and an in-context capture.
- **Ownership on overlap:** the **engine** skill owns API/syntax; the **discipline** skill owns
  the portable concept/algorithm and defers to the engine skill for code; the **genre** skill owns
  structure/glue and links out instead of re-teaching a primitive.
- **Hand-offs:** when a genre's `composes` names a slot like `*-2d-movement`, bind it to the
  detected engine. If that engine lacks the exact skill, see §6 and `references/routing-table.md`
  ("Binding gaps").

## 6. Unknown-engine & no-skill fallback

**Engine unknown** (no fingerprint, no engine named):

1. Check the request for a plain-text engine name ("in Unity", "using Phaser"). If found, adopt it.
2. If the task is a pure concept/genre/workflow question, route straight to the engine-agnostic
   discipline/genre/workflow skill — no engine needed ("what's a good save format?" → `dev-save-system`).
3. Only if engine choice actually blocks the answer, ask **one** targeted question about the
   engine or project entry point. For a **new project** with no existing engine and no user
   preference, **default to Godot** (the most fully covered engine here) and say so.
4. Never invent an engine or load an engine skill on a guess.

**Custom, proprietary, in-house, or unsupported engine:** keep that engine and its toolchain.
Read `references/custom-engines.md` to map the relevant discipline/genre concepts onto verified
project APIs, using local documentation, headers/source, examples, and build/test commands.
No catalog engine skill is required. Do not switch engines or invent a compatible API.

**Catalog engine known but no skill covers the subtask:** load the closest skill for that same engine plus the relevant
discipline and **state the gap** plainly (e.g. "no dedicated Unity 2D-movement skill; using
`unity-csharp` + `unity-physics`"). Never fabricate a skill name.

**Conflicting/multiple genres:** pick the dominant genre from the phrasing; mention the secondary
and offer to load it if the user confirms.

## Worked examples

| Request | Detected engine | Skills loaded (in order) |
|---------|-----------------|--------------------------|
| "add a double jump to my Godot player" | Godot (`project.godot`) | `godot-2d-movement` → `genre-platformer` |
| "make an inventory for my Unity RPG" | Unity (`Assets/`+`ProjectSettings/`) | `unity-scriptable-objects` → `genre-rpg` → `dev-save-system` |
| "add an inventory to my proprietary C++ RPG" | existing custom engine | custom-engine reference → `genre-rpg` + `dev-save-system`; bind data/UI to verified project APIs |
| "build a 2D puzzle in Go with Ebitengine" | Ebitengine (named; later `go.mod`) | `ebitengine-core` → `genre-puzzle` |
| "fix a stale HUD in my Go game" | Ebitengine (`go.mod` + game imports) | `ebitengine-core` → `dev-hud-menus`; read text/UI, no new scaffold |
| "add player movement to my Defold game" | Defold (`game.project`) | `defold-core` → `dev-input` |
| "rebirths in my Roblox simulator take forever" | Roblox (`*.project.json` / place file) | `roblox-luau` → `roblox-economy` → `roblox-networking` |
| "procedural dungeon roguelike in Godot" | Godot | `godot-tilemap` → `dev-procgen` → `genre-roguelike` |
| "branching dialogue from a `.yarn` file" | (none required) | `dev-dialogue` (+ engine UI skill if an engine is detected) |
| "how do I design save slots with migration?" | (none) | `dev-save-system` only |
| "publish my game on itch with butler" | (any/none) | `release-itch` only |
| "I want to make a game but don't know what to use" | unknown → ask, default Godot | router asks once; then e.g. `godot-scenes` |
| "make hits feel punchy in my Godot game" | Godot (`project.godot`) | `dev-game-feel` (+ `dev-camera` for shake) |
| "the camera should follow my player smoothly" | (detected engine) | `dev-camera` (+ engine movement skill) |
| "my Unity game drops to 30 FPS, optimize it" | Unity (`Assets/`+`ProjectSettings/`) | `dev-performance` (profile first) → engine skill |
| "make a cohesive pixel-art player and enemy set" | (detected engine) | `dev-art-assets` → relevant engine import/rendering skill |

## References

- Full engine fingerprints, secondary signals, and disambiguation: `references/engine-detection.md`.
- Exhaustive per-skill trigger words, engine bindings, and binding gaps: `references/routing-table.md`.
- Custom/proprietary or unsupported engine integration: `references/custom-engines.md`.
