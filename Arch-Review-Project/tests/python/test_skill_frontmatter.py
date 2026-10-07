"""Every SKILL.md must have valid YAML frontmatter."""
from pathlib import Path
import yaml

SKILLS_DIR = Path("claude-skills")

def test_frontmatter_present():
    for skill_md in SKILLS_DIR.glob("*/SKILL.md"):
        text = skill_md.read_text(encoding="utf-8")
        assert text.startswith("---"), f"{skill_md} missing frontmatter"
        end = text.index("---", 3)
        fm = yaml.safe_load(text[3:end])
        assert "name" in fm and "description" in fm
        assert len(fm["description"]) > 50

def test_name_matches_folder():
    for skill_md in SKILLS_DIR.glob("*/SKILL.md"):
        text = skill_md.read_text(encoding="utf-8")
        end = text.index("---", 3)
        fm = yaml.safe_load(text[3:end])
        assert fm["name"] == skill_md.parent.name
