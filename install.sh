#!/usr/bin/env bash
# Install game-dev-skills into Claude Code.
#
#   ./install.sh --global              core skills -> ~/.claude/skills (orchestrator, GDD, tech PRD, router)
#   ./install.sh --global --all        every portable skill -> ~/.claude/skills (heavy; see README)
#   ./install.sh --project <dir>       full studio template + all portable skills into a game repo
#   ./install.sh --project <dir> --engine godot   ...but only one engine family's skills
#
# Existing files are never overwritten unless you pass --force.
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
CORE=(game-studio-orchestrator game-design-doc game-tech-prd engine-skill-router)
ENGINE_PREFIXES="godot unity unreal phaser pixijs threejs bevy defold love2d pygame ebitengine roblox"

mode="" dest="" all=0 force=0 engine=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --global) mode=global; shift ;;
    --project) mode=project; dest="${2:?--project needs a directory}"; shift 2 ;;
    --all) all=1; shift ;;
    --engine) engine="${2:?--engine needs a name, e.g. godot}"; shift 2 ;;
    --force) force=1; shift ;;
    -h|--help) sed -n '2,10p' "$0"; exit 0 ;;
    *) echo "Unknown option: $1" >&2; exit 1 ;;
  esac
done
[[ -z "$mode" ]] && { sed -n '2,10p' "$0"; exit 1; }

copy_dir() {  # src dst
  if [[ -e "$2" && $force -eq 0 ]]; then echo "  skip (exists): $2"; return; fi
  rm -rf "$2"; mkdir -p "$(dirname "$2")"; cp -R "$1" "$2"
}

is_other_engine() {  # skill name -> true if it belongs to an engine other than $engine
  local n="$1" p
  [[ -z "$engine" ]] && return 1
  for p in $ENGINE_PREFIXES; do
    [[ "$n" == "$p"-* && "$p" != "$engine" ]] && return 0
  done
  return 1
}

if [[ "$mode" == global ]]; then
  target="$HOME/.claude/skills"
  if [[ $all -eq 1 ]]; then names=$(ls "$HERE/skills"); else names="${CORE[*]}"; fi
  for n in $names; do copy_dir "$HERE/skills/$n" "$target/$n"; done
  echo "Installed to $target"
  exit 0
fi

# project mode
dest="$(cd "$dest" && pwd)"
mkdir -p "$dest/.claude"
for sub in agents hooks rules docs scripts skills; do
  [[ -d "$HERE/studio/.claude/$sub" ]] || continue
  for item in "$HERE/studio/.claude/$sub"/*; do
    copy_dir "$item" "$dest/.claude/$sub/$(basename "$item")"
  done
done
for f in settings.json statusline.sh; do
  [[ -e "$HERE/studio/.claude/$f" ]] && copy_dir "$HERE/studio/.claude/$f" "$dest/.claude/$f"
done
for f in CLAUDE.md project.yaml; do copy_dir "$HERE/studio/$f" "$dest/$f"; done
for s in "$HERE/skills"/*; do
  n="$(basename "$s")"
  is_other_engine "$n" && continue
  copy_dir "$s" "$dest/.claude/skills/$n"
done
echo "Studio template installed in $dest"
echo "Start with:  claude --agent game-studio-orchestrator"
