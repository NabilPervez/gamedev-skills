"""Validate game-dev-skills. Usage: python3 -I validate.py <repo_dir>"""
import re, sys, pathlib

R = pathlib.Path(sys.argv[1])
errs, n = [], 0
NAME_OK = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

def front(p):
    s = p.read_text()
    m = re.match(r"---\n(.*?)\n---\n", s, re.S)
    return m.group(1) if m else None

def desc_len(fm):
    m = re.search(r"^description:(.*?)(?=^\w[\w-]*:|\Z)", fm, re.S | re.M)
    if not m:
        return -1
    d = m.group(1).strip()
    d = re.sub(r"^[>|][-+]?\s*", "", d)
    return len(re.sub(r"\s+", " ", d).strip().strip('"'))

for md in list(R.glob("skills/*/SKILL.md")) + list(R.glob("studio/.claude/skills/*/SKILL.md")):
    n += 1
    fm = front(md)
    d = md.parent.name
    if fm is None:
        errs.append(f"{md}: no frontmatter"); continue
    m = re.search(r"^name:\s*(\S+)\s*$", fm, re.M)
    name = m.group(1) if m else None
    if name != d: errs.append(f"{md}: name '{name}' != folder '{d}'")
    if not name or not NAME_OK.match(name) or len(name) > 64:
        errs.append(f"{md}: bad name '{name}'")
    if name and re.search(r"claude|anthropic", name): errs.append(f"{md}: reserved word in name")
    L = desc_len(fm)
    if L <= 0: errs.append(f"{md}: missing description")
    elif L > 1024: errs.append(f"{md}: description {L} chars > 1024")

agents = list(R.glob("studio/.claude/agents/*.md"))
for a in agents:
    fm = front(a)
    m = fm and re.search(r"^name:\s*(\S+)\s*$", fm, re.M)
    if not m or m.group(1) != a.stem:
        errs.append(f"{a}: agent name mismatch ({m.group(1) if m else None})")

# leftover old names used as invocations
ren = [l.split("\t") for l in (R / "RENAMES.tsv").read_text().splitlines()[1:]]
cc_old = [o for s, t, o, nw in ren if s == "claude-code-game-studios" and t == "skill"]
ag_old = [o for s, t, o, nw in ren if t == "agent"]
pat_cc = re.compile(r"(?<![\w./-])/(" + "|".join(map(re.escape, cc_old)) + r")(?![\w-])")
pat_ag = re.compile(r"(?<![\w-])(" + "|".join(map(re.escape, ag_old)) + r")(?![\w-])")
for p in (R / "studio").rglob("*"):
    if p.is_file() and p.suffix in {".md", ".yaml", ".yml", ".sh", ".json"}:
        s = p.read_text(errors="ignore")
        for m in pat_cc.finditer(s):
            errs.append(f"{p.relative_to(R)}: leftover /{m.group(1)}")
        for m in pat_ag.finditer(s):
            errs.append(f"{p.relative_to(R)}: leftover agent {m.group(1)}")
for d in R.glob("studio/.claude/skills/*/SKILL.md"):
    for m in re.finditer(r"\.claude/skills/([a-z0-9-]+)/", d.read_text()):
        if m.group(1) != "some-skill" and not (R / "studio/.claude/skills" / m.group(1)).exists():
            errs.append(f"{d.relative_to(R)}: path to missing skill {m.group(1)}")

print(f"checked {n} skills, {len(agents)} agents; {len(errs)} problems")
for e in errs[:60]:
    print(" -", e)
sys.exit(1 if errs else 0)
