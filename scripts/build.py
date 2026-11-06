"""Build NabilPervez/game-dev-skills from the two source repos.
Usage: python3 -I build.py <work_dir>   (expects src-agds, src-ccgs; writes game-dev-skills)
"""
import os, re, shutil, sys, pathlib

W = pathlib.Path(sys.argv[1])
AG, CC, OUT = W / "src-agds", W / "src-ccgs", W / "game-dev-skills"

AGDS_RENAMES = {
    "router": "engine-skill-router",
    "godot-nodes-scenes": "godot-scenes", "godot-signals-groups": "godot-signals",
    "godot-ui-control": "godot-ui", "godot-3d-essentials": "godot-3d",
    "godot-gdscript-headless-testing": "godot-headless-tests",
    "unity-csharp-scripting": "unity-csharp", "unity-input-system": "unity-input",
    "unity-scriptableobjects": "unity-scriptable-objects", "unity-build-pipeline": "unity-build",
    "unreal-cpp-gameplay": "unreal-cpp", "ebitengine-game": "ebitengine-core",
    "pixijs-rendering": "pixijs-core", "threejs-scene-setup": "threejs-scene",
    "threejs-gltf-loading": "threejs-gltf", "roblox-studio-workflow": "roblox-studio",
    "roblox-simulator-economy": "roblox-economy",
    "create-game-assets": "dev-art-assets", "game-ai": "dev-npc-ai",
    "ai-behavior-trees-utility-ai": "dev-behavior-trees-utility-ai",
    "procedural-gen": "dev-procgen", "dialogue-systems": "dev-dialogue",
    "save-systems": "dev-save-system", "audio-design": "dev-audio-mixing",
    "shader-programming": "dev-shaders", "physics-tuning": "dev-physics-tuning",
    "level-design": "dev-level-blockout", "input-systems": "dev-input",
    "game-feel": "dev-game-feel", "game-ui-ux": "dev-hud-menus",
    "camera-systems": "dev-camera", "performance-optimization": "dev-performance",
    "platformer": "genre-platformer", "roguelike": "genre-roguelike", "rpg": "genre-rpg",
    "fps-shooter": "genre-fps", "tower-defense": "genre-tower-defense",
    "card-game": "genre-card-game", "visual-novel": "genre-visual-novel",
    "survival-crafting": "genre-survival-crafting", "puzzle": "genre-puzzle",
    "game-jam": "plan-game-jam", "prototype-fast": "build-greybox-prototype",
    "steam-publish": "release-steam", "itch-publish": "release-itch",
}

CCGS_RENAMES = {
    "start": "studio-start", "help": "studio-next-step",
    "project-stage-detect": "studio-detect-stage", "setup-engine": "studio-setup-engine",
    "adopt": "studio-adopt-project", "settings": "studio-settings", "onboard": "studio-onboard",
    "brainstorm": "concept-brainstorm", "prototype": "concept-prototype",
    "map-systems": "design-map-systems", "design-system": "design-system-gdd",
    "quick-design": "design-quick-spec", "propagate-design-change": "design-propagate-change",
    "reverse-document": "design-reverse-document", "asset-spec": "art-asset-spec",
    "asset-audit": "art-asset-audit", "ux-design": "ux-spec", "ux-review": "review-ux",
    "create-architecture": "arch-blueprint", "architecture-decision": "arch-adr",
    "architecture-review": "review-architecture", "create-control-manifest": "arch-control-manifest",
    "create-epics": "plan-epics", "create-stories": "plan-stories", "estimate": "plan-estimate",
    "sprint-plan": "plan-sprint", "sprint-status": "plan-sprint-status",
    "story-readiness": "plan-story-readiness", "dev-story": "build-story",
    "story-done": "build-story-done", "vertical-slice": "build-vertical-slice",
    "design-review": "review-design-doc", "review-all-gdds": "review-gdd-suite",
    "code-review": "review-code", "balance-check": "review-balance",
    "content-audit": "review-content", "scope-check": "review-scope",
    "tech-debt": "review-tech-debt", "gate-check": "review-phase-gate",
    "consistency-check": "review-consistency", "security-audit": "review-security",
    "perf-profile": "qa-perf-profile", "qa-plan": "qa-test-plan", "smoke-check": "qa-smoke",
    "soak-test": "qa-soak", "regression-suite": "qa-regression", "test-setup": "qa-test-setup",
    "test-helpers": "qa-test-helpers", "test-evidence-review": "qa-evidence-review",
    "test-flakiness": "qa-flaky-tests", "bug-report": "qa-bug-report",
    "bug-triage": "qa-bug-triage", "playtest-report": "qa-playtest-report",
    "milestone-review": "prod-milestone-review", "retrospective": "prod-retro",
    "localize": "prod-localize", "launch-checklist": "release-launch-checklist",
    "changelog": "release-changelog", "patch-notes": "release-patch-notes",
    "hotfix": "release-hotfix", "day-one-patch": "release-day-one-patch",
    "skill-test": "meta-skill-test", "skill-improve": "meta-skill-improve",
}
AGENT_RENAMES = {f"ue-{x}-specialist": f"unreal-{x}-specialist"
                 for x in ("blueprint", "gas", "replication", "umg")}

TEXT_EXT = {".md", ".yaml", ".yml", ".sh", ".json", ".txt", ".py", ".toml", ""}

def alt(keys):
    return "|".join(re.escape(k) for k in sorted(keys, key=len, reverse=True))

AG_TICK = re.compile(r"`(" + alt(AGDS_RENAMES) + r")`")
CC_SLASH = re.compile(r"(?<![\w./-])/(" + alt(CCGS_RENAMES) + r")(?![\w-])")
CC_PATH = re.compile(r"(\.claude/skills/)(" + alt(CCGS_RENAMES) + r")(?=/|\b)(?![\w-])")
SPEC_PATH = re.compile(r"(studio-tests/skills/[a-z-]+/)(" + alt(CCGS_RENAMES) + r")\.md")
AGENT_RE =re.compile(r"(?<![\w-])(" + alt(AGENT_RENAMES) + r")(?![\w-])")

def text_files(root):
    for p in root.rglob("*"):
        if p.is_file() and p.suffix in TEXT_EXT and ".git" not in p.parts:
            yield p

def set_name(skill_md, new):
    s = skill_md.read_text()
    s = re.sub(r"^name:.*$", f"name: {new}", s, count=1, flags=re.M)
    skill_md.write_text(s)

NOTICE_LINE = ("> Modified by Nabil Pervez, 2026: {what}. Original © Abhishek Barali and the "
               "awesome-gamedev-agent-skills contributors, Apache-2.0 (see THIRD_PARTY/).\n")

def add_apache_notice(skill_md, what):
    s = skill_md.read_text()
    m = re.match(r"(---\n.*?\n---\n)", s, re.S)
    head, body = (m.group(1), s[m.end():]) if m else ("", s)
    skill_md.write_text(head + "\n" + NOTICE_LINE.format(what=what) + body)

ORIGINAL = ["skills/game-studio-orchestrator", "skills/game-design-doc", "skills/game-tech-prd",
            "studio/.claude/agents/game-studio-orchestrator.md", "install.sh", "scripts",
            "README.md", "NOTICE", "LICENSE", ".gitignore"]

def main():
    # Original work (not imported) is stashed and restored so a rebuild never loses it.
    keep = W / ".original-backup"
    if keep.exists():
        shutil.rmtree(keep)
    for rel in ORIGINAL:
        src = OUT / rel
        if src.exists():
            (keep / rel).parent.mkdir(parents=True, exist_ok=True)
            if src.is_dir():
                shutil.copytree(src, keep / rel)
            else:
                shutil.copy2(src, keep / rel)
    if OUT.exists():
        for child in OUT.iterdir():
            if child.name != ".git":
                shutil.rmtree(child) if child.is_dir() else child.unlink()
    skills = OUT / "skills"
    skills.mkdir(parents=True)
    try:
        build(skills)
    finally:
        for rel in ORIGINAL:
            src = keep / rel
            if src.exists():
                (OUT / rel).parent.mkdir(parents=True, exist_ok=True)
                if src.is_dir():
                    shutil.copytree(src, OUT / rel, dirs_exist_ok=True)
                else:
                    shutil.copy2(src, OUT / rel)

def build(skills):

    # --- 1. awesome-gamedev-agent-skills -> flat skills/<name>/ ---
    src_dirs = [AG / "router"] + [d for cat in sorted((AG / "skills").iterdir()) if cat.is_dir()
                                  for d in sorted(cat.iterdir()) if (d / "SKILL.md").exists()]
    for d in src_dirs:
        old = d.name
        new = AGDS_RENAMES.get(old, old)
        dst = skills / new
        shutil.copytree(d, dst)
        set_name(dst / "SKILL.md", new)
    for p in text_files(skills):
        s = p.read_text()
        s2 = AG_TICK.sub(lambda m: "`" + AGDS_RENAMES[m.group(1)] + "`", s)
        if s2 != s:
            p.write_text(s2)
    for d in src_dirs:
        old = d.name
        new = AGDS_RENAMES.get(old, old)
        what = (f"renamed from `{old}`; skill references updated" if new != old
                else "skill references updated to new names")
        add_apache_notice(skills / new / "SKILL.md", what)

    # --- 2. Claude-Code-Game-Studios -> studio/ project template ---
    studio = OUT / "studio"
    shutil.copytree(CC, studio, ignore=shutil.ignore_patterns(".git", ".github"))
    (studio / "README.md").rename(studio / "UPSTREAM-README.md")
    sk = studio / ".claude" / "skills"
    for old, new in CCGS_RENAMES.items():
        (sk / old).rename(sk / new)
        set_name(sk / new / "SKILL.md", new)
    for spec in list((studio / "studio-tests").rglob("*.md")):
        if spec.stem in CCGS_RENAMES and "skills" in spec.parts:
            spec.rename(spec.with_name(CCGS_RENAMES[spec.stem] + ".md"))
    ag = studio / ".claude" / "agents"
    for old, new in AGENT_RENAMES.items():
        (ag / f"{old}.md").rename(ag / f"{new}.md")
    for p in studio.rglob(f"*ue-*-specialist*"):
        p.rename(p.with_name(AGENT_RE.sub(lambda m: AGENT_RENAMES[m.group(1)], p.name)))
    for p in text_files(studio):
        try:
            s = p.read_text()
        except UnicodeDecodeError:
            continue
        s2 = CC_PATH.sub(lambda m: m.group(1) + CCGS_RENAMES[m.group(2)], s)
        s2 = SPEC_PATH.sub(lambda m: m.group(1) + CCGS_RENAMES[m.group(2)] + ".md", s2)
        s2 = CC_SLASH.sub(lambda m: "/" + CCGS_RENAMES[m.group(1)], s2)
        s2 = AGENT_RE.sub(lambda m: AGENT_RENAMES[m.group(1)], s2)
        if s2 != s:
            p.write_text(s2)

    cat = studio / "studio-tests" / "catalog.yaml"
    if cat.exists():
        s = cat.read_text()
        s = re.sub(r"(-\s+name:\s+)(" + alt(CCGS_RENAMES) + r")\s*$",
                   lambda m: m.group(1) + CCGS_RENAMES[m.group(2)], s, flags=re.M)
        s = re.sub(r"(-\s+name:\s+)(" + alt(AGENT_RENAMES) + r")\s*$",
                   lambda m: m.group(1) + AGENT_RENAMES[m.group(2)], s, flags=re.M)
        cat.write_text(s)

    # --- 3. licenses ---
    tp = OUT / "THIRD_PARTY"
    tp.mkdir()
    shutil.copy(AG / "LICENSE", tp / "awesome-gamedev-agent-skills.LICENSE")
    shutil.copy(AG / "NOTICE", tp / "awesome-gamedev-agent-skills.NOTICE")
    shutil.copy(CC / "LICENSE", tp / "claude-code-game-studios.LICENSE")

    # --- 4. rename map ---
    with open(OUT / "RENAMES.tsv", "w") as f:
        f.write("source\ttype\told\tnew\n")
        for o, n in AGDS_RENAMES.items():
            f.write(f"awesome-gamedev-agent-skills\tskill\t{o}\t{n}\n")
        for o, n in CCGS_RENAMES.items():
            f.write(f"claude-code-game-studios\tskill\t{o}\t{n}\n")
        for o, n in AGENT_RENAMES.items():
            f.write(f"claude-code-game-studios\tagent\t{o}\t{n}\n")

if __name__ == "__main__":
    main()
