"""
ContentLoader — the only module that reads from content/.
Every load function is cached. Adding new content files requires
no changes to application logic.
"""
import json
import os
from pathlib import Path
import streamlit as st

CONTENT_DIR = Path("content")


def _read_json(path: str) -> dict | list:
    full = CONTENT_DIR / path
    if not full.exists():
        return {}
    with open(full, encoding="utf-8") as f:
        return json.load(f)


def _read_md(path: str) -> str:
    full = CONTENT_DIR / path
    if not full.exists():
        return ""
    with open(full, encoding="utf-8") as f:
        return f.read()


def _parse_md_frontmatter(content: str) -> tuple[dict, str]:
    """Split YAML frontmatter from Markdown body. Returns (meta, body)."""
    meta = {}
    body = content
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            body = parts[2].strip()
            for line in parts[1].strip().splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    raw = v.strip()
                    # Parse simple lists like [a, b, c]
                    if raw.startswith("[") and raw.endswith("]"):
                        raw = [x.strip() for x in raw[1:-1].split(",")]
                    meta[k.strip()] = raw
    return meta, body


# ── Cached loaders ──────────────────────────────────────────────────────────

@st.cache_data(ttl=3600)
def load_config() -> dict:
    return _read_json("config.json")


@st.cache_data(ttl=3600)
def load_about() -> tuple[dict, str]:
    content = _read_md("about.md")
    return _parse_md_frontmatter(content)


@st.cache_data(ttl=3600)
def load_experience() -> list:
    data = _read_json("experience.json")
    return data if isinstance(data, list) else []


@st.cache_data(ttl=3600)
def load_education() -> list:
    data = _read_json("education.json")
    return data if isinstance(data, list) else []


@st.cache_data(ttl=3600)
def load_skills() -> dict:
    return _read_json("skills.json")


@st.cache_data(ttl=3600)
def load_achievements() -> list:
    data = _read_json("achievements.json")
    return data if isinstance(data, list) else []


@st.cache_data(ttl=3600)
def load_projects() -> list[dict]:
    """Auto-discovers every JSON file in content/projects/."""
    projects_dir = CONTENT_DIR / "projects"
    if not projects_dir.exists():
        return []
    projects = []
    for f in sorted(projects_dir.glob("*.json")):
        try:
            with open(f, encoding="utf-8") as fh:
                projects.append(json.load(fh))
        except Exception:
            pass
    return projects


@st.cache_data(ttl=3600)
def load_project(project_id: str) -> dict:
    path = CONTENT_DIR / "projects" / f"{project_id}.json"
    if not path.exists():
        return {}
    with open(path, encoding="utf-8") as f:
        return json.load(f)


@st.cache_data(ttl=3600)
def load_research() -> dict:
    """Returns dict with keys: published, under_review, in_progress."""
    result = {}
    for status in ["published", "under_review", "in_progress"]:
        content = _read_md(f"research/{status}.md")
        meta, body = _parse_md_frontmatter(content)
        result[status] = {"meta": meta, "body": body}
    return result


def get_project_by_id(project_id: str, projects: list) -> dict:
    for p in projects:
        if p.get("id") == project_id:
            return p
    return projects[0] if projects else {}
