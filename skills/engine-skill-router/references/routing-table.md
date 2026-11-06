# Full routing table — every authored skill

The exhaustive `task → category → skill` lookup the router body summarizes. Every name here is
a real folder at `skills/<category>/<name>/SKILL.md`. Trigger words (`says:`) and file signals
(`files:`) are the cues that should select each skill. `*` in a binding is filled with the
**detected** engine (router body §1); where an engine lacks the exact skill, see "Binding gaps".

## Engine skills

### Godot (`skills/godot/`, target Godot 4.7) — read after `project.godot` is detected

| Skill | Pick it when the request says / file signal |
|-------|---------------------------------------------|
| `godot-gdscript` | "GDScript", `_ready`/`_process`, typing, `@export`, `await`; `*.gd` |
| `godot-scenes` | "scene", "node tree", "instance a scene", autoloads, `PackedScene`; `*.tscn` |
| `godot-signals` | "signal", "emit", "connect", "groups", decoupling/observer |
| `godot-2d-movement` | "2D movement", "platformer controller", `CharacterBody2D`, `move_and_slide` |
| `godot-tilemap` | "tilemap", "tileset", "autotile", `TileMapLayer`; tileset `*.tres` |
| `godot-physics` | "rigidbody", "area2d", "collision layer", "raycast" (2D + 3D) |
| `godot-ui` | "UI", "Control node", "anchors", "theme", "HUD" |
| `godot-animation` | `AnimationPlayer`, `AnimationTree`, "blend", `Tween` |
| `godot-shaders` | "Godot shader", "gdshader", fragment/vertex, screen-reading; `*.gdshader` |
| `godot-3d` | "3D", `Camera3D`, `WorldEnvironment`, `GridMap`; `Node3D` |
| `godot-resources` | "custom Resource", "data resource", `.tres`, `ResourceLoader` |
| `godot-audio` | "Godot audio", "audio bus", "play sound/music", sync-to-beat |
| `godot-multiplayer` | "multiplayer", "RPC", "networked", `MultiplayerSpawner`; `@rpc` |
| `godot-export` | "export Godot", "build for web/windows", `export_presets.cfg` |
| `godot-csharp` | "Godot C#", "GodotSharp", "C# signals in Godot"; `*.cs` + `*.csproj` in a Godot project |
| `godot-headless-tests` | "headless test", "run tests from CLI", `godot --headless --script`, CI job for `.gd` tests |

### Unity (`skills/unity/`, target Unity 6.3 LTS / 6000.3)

| Skill | Pick it when |
|-------|--------------|
| `unity-csharp` | "Unity script", `MonoBehaviour`, `Start`/`Update`, coroutines; `*.cs` + `*.asmdef` |
| `unity-input` | "Input System", `InputAction`, "action map"; `*.inputactions` |
| `unity-physics` | "Unity physics", `Rigidbody`, "collision layers", "joint" |
| `unity-animation` | "Animator", "state machine", "blend tree", "Mecanim"; `*.controller` |
| `unity-scriptable-objects` | `ScriptableObject`, "SO architecture", "data asset", event channels |
| `unity-tilemap-2d` | "Unity tilemap", "tile palette", "rule tile" |
| `unity-navmesh` | `NavMesh`, `NavMeshAgent`, "pathfinding in Unity" |
| `unity-build` | "build Unity", "player settings", "IL2CPP", "Addressables" |

### Unreal (`skills/unreal/`, target UE 5.8)

| Skill | Pick it when |
|-------|--------------|
| `unreal-blueprints` | "Blueprint", "BP graph", "event graph"; Blueprint `*.uasset` |
| `unreal-cpp` | "Unreal C++", `GameMode`, `Pawn`, `ACharacter`; `Source/**/*.cpp` + `*.Build.cs` |
| `unreal-enhanced-input` | "Enhanced Input", "Input Mapping Context", `IA_`/`IMC_` |
| `unreal-behavior-trees` | "Behavior Tree", "Blackboard", `AIController`, `BTTask`; `BT_`/`BB_` |
| `unreal-niagara` | "Niagara", "VFX", "particle system"; `NS_`/`NE_` |
| `unreal-packaging` | "package Unreal", "cook content", "shipping build" |

### Ebitengine (`skills/ebitengine/`, target v2.10.5 / Go 1.25+)

| Skill | Pick it when |
|-------|--------------|
| `ebitengine-core` | "Ebitengine", "Ebiten", "2D game in Go", `Update`/`Draw`/`Layout`, action input, sprites, text, audio, scenes, testing or builds in an Ebitengine game; `go.mod` requiring `github.com/hajimehoshi/ebiten/v2` plus game imports |

### Web engines (`skills/web-engines/`) — detected from `package.json` + imports

| Skill | Pick it when |
|-------|--------------|
| `phaser-core` | "Phaser", "Phaser scene", `preload`/`create`/`update`; dep `phaser` |
| `phaser-arcade-physics` | "Arcade Physics", "collider", "overlap", world bounds |
| `pixijs-core` | "PixiJS", "Pixi sprite", "stage", `Container`; dep `pixi.js` |
| `threejs-scene` | "three.js", `THREE.Scene`, `WebGLRenderer`, render loop; dep `three` |
| `threejs-gltf` | "load gltf", `GLTFLoader`, `AnimationMixer`; `*.gltf`/`*.glb` |
| `threejs-materials-lighting` | `MeshStandardMaterial`, "lighting", "shadows", env maps |

### Other engines (`skills/other-engines/`)

| Skill | Pick it when |
|-------|--------------|
| `bevy-ecs` | "Bevy", "ECS system/query", `Commands`, "Bevy plugin"; `Cargo.toml` dep `bevy` |
| `pygame-core` | "pygame", "blit", "sprite group", game loop; `import pygame` |
| `love2d-core` | "LÖVE", "love2d", `love.draw`, `love.update(dt)`; `main.lua`/`conf.lua`/`*.love` |
| `defold-core` | "Defold", collection/game object/component, `msg.post`, `on_message`, `on_input`, `acquire_input_focus`, `go.property`, `factory.create`, collection proxy, `bob.jar`, Defold build error; `game.project` + `*.collection`/`*.go`/`*.script` (target Defold 1.14.0) |
| `roblox-luau` | "Roblox", "Luau", `RemoteEvent`, services; `*.luau` + `*.rbxl(x)` / Rojo |
| `roblox-datastores` | "DataStore", "save player data", `GetDataStore`; `DataStoreService` |
| `roblox-ui` | Roblox HUD/menu/inventory/shop, `ScreenGui`, `PlayerGui`, `UDim2`, `AutomaticSize`, `GuiService`, UI clipping/respawn, touch/gamepad focus, generic generated UI |
| `roblox-networking` | Roblox remotes/security/replication, `RemoteEvent`, `RemoteFunction`, `UnreliableRemoteEvent`, exploit, request spam, server authority, desync |
| `roblox-characters` | Roblox character/respawn/rig/movement/animation, `CharacterAdded`, `Humanoid`, `Animator`, R6/R15, Tool, stale character reference |
| `roblox-physics` | Roblox assembly/constraint/collision/query/ownership, `RaycastParams`, overlap, `CanQuery`, impulse, BodyMover, projectile/vehicle/knockback |
| `roblox-studio` | edit/inspect/test a Roblox place in Studio, Explorer, Script/LocalScript/ModuleScript placement, tags/Attributes, duplicate remotes/systems, Server & Clients, Output |
| `roblox-economy` | Roblox simulator/tycoon/clicker/idle economy, upgrade cost curve, `costGrowth`, buy max, income per second, rebirth/prestige requirement or multiplier, offline earnings, big-number suffixes (K/M/B/Qa), "1000K" display bug, currency exploit, save repair, paid eggs/crates/spins odds, `PolicyService` paid random items; pairs with `roblox-networking` + `roblox-datastores` |

## Disciplines (`skills/disciplines/`) — cross-engine concepts, load **with** the engine skill

| Concept skill | `says:` triggers | Pairs with (engine API skill) |
|---------------|------------------|-------------------------------|
| `dev-art-assets` | art direction, game assets, sprite/sprite sheet, tileset, texture, icon, concept art, 3D prop, consistent style | engine importer/rendering skill; installed `imagegen` for raster generation when available |
| `dev-npc-ai` | enemy AI, behavior tree, state machine, steering, pathfinding | `unity-navmesh` / `unreal-behavior-trees` / Godot nav (`godot-scenes` + `godot-physics`) |
| `dev-behavior-trees-utility-ai` | behavior tree runtime, blackboard, action/condition node, selector/sequence/parallel, decorator, utility AI, scoring/response curve, consideration, hybrid AI | `dev-npc-ai` (FSM/BT/steering choice) / `unreal-behavior-trees` (engine BT/Blackboard assets) |
| `dev-procgen` | procedural generation, perlin/simplex noise, random seed, dungeon generator, wave function collapse (WFC) | engine tilemap/grid: `godot-tilemap` / `unity-tilemap-2d` / `godot-3d` |
| `dev-dialogue` | dialogue system, branching dialogue, Yarn Spinner, Ink, conversation tree; `*.yarn`/`*.ink` | engine UI: `godot-ui` / Unity UI |
| `dev-save-system` | save system, save/load, persistence, save slots; `save*.json`/`*.sav` | `roblox-datastores` / Godot IO / engine serialization |
| `dev-audio-mixing` | audio design, adaptive music, audio mixer, ducking, SFX | `godot-audio` / Unity AudioMixer |
| `dev-shaders` | shader, fragment shader, dissolve/outline effect, GLSL/HLSL; `*.gdshader`/`*.shader`/`*.hlsl` | `godot-shaders` / engine material docs |
| `dev-physics-tuning` | physics feel, jitter/tunneling, fixed timestep, collision tuning | `godot-physics` / `unity-physics` |
| `dev-level-blockout` | level design, whitebox/blockout, tilemap layout, pacing | `godot-tilemap` / `unity-tilemap-2d` / `godot-3d` (GridMap) |
| `dev-input` | input mapping, rebind controls, gamepad support, input buffering; `*.inputactions`/IMC | `unity-input` / `unreal-enhanced-input` / Godot InputMap |
| `dev-game-feel` | game feel, juice, screen shake, hit-stop/freeze frame, squash & stretch, knockback, "make it punchy/satisfying" | engine animation/tween (`godot-animation`/`unity-animation`) + `dev-camera` (shake) + `dev-audio-mixing` |
| `dev-camera` | camera follow, follow camera, deadzone, look-ahead, camera bounds/limits, third-person/orbit camera, first-person look, Cinemachine, camera jitter | `godot-2d-movement`/`godot-3d` / Unity Cinemachine 3 / Godot `Camera2D`/`Camera3D` |
| `dev-hud-menus` | HUD, health bar, main/pause/settings menu, UI layout, anchors, UI scaling, aspect ratio, safe area, controller/keyboard menu nav | `godot-ui` / Unity UI (UGUI/UI Toolkit) |
| `dev-performance` | performance, optimize, low/dropping FPS, frame drops, stutter, lag, frame budget, draw calls, batching, GC spikes, object pooling, profiler | engine profiler (Godot Monitors / Unity Profiler / Unreal `stat unit`) + `dev-physics-tuning` |

## Genres (`skills/genres/`) — whole-game templates, **compose** engine + disciplines

| Genre skill | `says:` triggers | composes (bind `*` to the detected engine) |
|-------------|------------------|---------------------------------------------|
| `genre-platformer` | platformer, jump mechanic, double jump, wall jump, wall slide, Mario-like | `godot-2d-movement` (or engine physics) + `godot-tilemap`/`unity-tilemap-2d` + `dev-level-blockout` + `dev-camera` + `dev-game-feel` |
| `genre-roguelike` | roguelike, procedural dungeon, permadeath, turn-based grid | `dev-procgen` + `godot-tilemap`/`unity-tilemap-2d` + `dev-npc-ai` + `dev-save-system` + `dev-game-feel` |
| `genre-rpg` | RPG, stats/leveling, inventory, quest system | `godot-resources`/`unity-scriptable-objects` + `dev-dialogue` + `dev-save-system` + `dev-hud-menus` |
| `genre-fps` | FPS, first-person shooter, hitscan, aim/shoot | `godot-3d`/`unreal-cpp` + `dev-input` + `dev-npc-ai` + `dev-camera` + `dev-game-feel` |
| `genre-tower-defense` | tower defense, wave spawner, enemy path, tower targeting | `dev-npc-ai` + `godot-2d-movement`/engine movement + `dev-level-blockout` + `dev-hud-menus` |
| `genre-card-game` | card game, deckbuilder, hand/deck/discard, TCG | `godot-resources`/`unity-scriptable-objects` + `dev-hud-menus` + `godot-ui` (engine UI) |
| `genre-visual-novel` | visual novel, VN, branching story, choice menu, Ren'Py; `*.ink`/`*.yarn`/`*.rpy` | `dev-dialogue` + `dev-save-system` + `dev-hud-menus` |
| `genre-survival-crafting` | survival game, crafting system, inventory, resource gathering | `dev-save-system` + `godot-resources`/`unity-scriptable-objects` + `dev-procgen` + `dev-hud-menus` |
| `genre-puzzle` | puzzle game, match-3, grid logic, tile-matching | `godot-tilemap`/`unity-tilemap-2d` + `dev-level-blockout` + `dev-game-feel` |

## Workflows (`skills/workflows/`) — process & shipping, engine-independent

| Workflow skill | `says:` / `files:` triggers |
|----------------|------------------------------|
| `plan-game-jam` | game jam, 48-hour game, Ludum Dare / GMTK, jam submission |
| `build-greybox-prototype` | prototype fast, vertical slice, MVP game, greybox |
| `release-steam` | publish on Steam, Steamworks, store page, depot/build upload, Steam Deck compatibility review; `steam_appid.txt` |
| `release-itch` | publish on itch, itch.io page, `butler push`, upload build; `.itch.toml` |

## Binding gaps (be honest; do not fabricate a skill)

For a **custom, proprietary, in-house, or unsupported engine**, keep the engine and use the
router's `custom-engines.md` reference. Load the relevant genre/discipline skills; replace
catalog engine bindings with verified project APIs. Engine-specific names in composition
tables are examples, not mandatory dependencies for portable genre systems.

The collection does not yet have a skill for every engine × concept. Several cross-cutting
concerns are now covered **engine-neutrally** by disciplines that pair with any detected engine —
camera work (`dev-camera`), HUD/menus (`dev-hud-menus`), juice/feedback (`dev-game-feel`), and
performance (`dev-performance`) — so those are no longer gaps; bind them on top of the
engine. The remaining true gaps are engine-specific primitives. When a genre binding names a slot
the detected engine lacks, load the closest skill(s) and **state the gap** plainly:

- **No `*-2d-movement` for Unity / Unreal / web.** For a Unity platformer, bind movement to
  `unity-csharp` + `unity-physics`; for Phaser, `phaser-arcade-physics`. Say there is
  no dedicated `unity-2d-movement` skill.
- **No dedicated 3D-essentials for Unity.** For a Unity FPS, use `unity-csharp` +
  `unity-physics` + `unity-navmesh`; only Godot has `godot-3d` and Unreal has
  `unreal-cpp`.
- **No `*-tilemap` for web / Bevy / pygame / Roblox / LÖVE / Defold.** Use `dev-level-blockout` for the concept
  and the engine's rendering skill for drawing; note the missing engine tilemap skill.
- **No engine-specific save skill except Roblox.** `dev-save-system` owns the concept and cites
  Godot IO; `roblox-datastores` is the one engine-specific persistence skill.
- **Ebitengine uses one engine skill with focused references.** Bind engine movement,
  collision, rendering/camera, UI, audio, data/save and build slots to `ebitengine-core`;
  open only the matching reference. A puzzle/card request does not require a platformer
  scaffold. The Tiled loader is deliberately constrained, not a complete editor importer.
  Networking guidance does not supply transport/matchmaking; native 3D is outside this
  2D skill. Never substitute another engine's API to hide one of these gaps.
- **Defold has one core skill.** Bind movement, input, spawning, level loading and build slots
  to `defold-core`. There is no Defold GUI, sprite/tilemap or collision skill yet: use
  `defold-core` (its build reference links the official manuals for those subsystems) plus
  `dev-hud-menus` / `dev-level-blockout` / `dev-physics-tuning`, and state the gap.
