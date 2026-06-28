"""
skills.py — Evidence-based skills with ECharts force graph + detail panel.
Falls back gracefully if streamlit-echarts is not installed.
"""
import streamlit as st
from app.services.content_loader import load_skills, load_projects, load_experience
from app.utils import state_manager as sm

PROFICIENCY_ORDER = ["Beginner", "Building", "Proficient", "Advanced", "Deep expertise"]
PROFICIENCY_COLOR = {
    "Beginner":      "#6E7681",
    "Building":      "#D29922",
    "Proficient":    "#4FC3F7",
    "Advanced":      "#3FB950",
    "Deep expertise":"#BC8CFF",
}


def _build_graph_data(skills_data: dict) -> tuple[list, list]:
    """Build ECharts nodes and links from skills JSON."""
    nodes, links = [], []
    categories = skills_data.get("categories", [])

    for cat in categories:
        cat_id    = cat["id"]
        cat_label = cat["label"]
        cat_color = cat.get("color", "#4FC3F7")

        # Category node
        nodes.append({
            "id":         cat_id,
            "name":       cat_label,
            "symbolSize": 28,
            "itemStyle":  {"color": cat_color},
            "label":      {"fontSize": 11, "fontWeight": "bold"},
            "category":   cat_id,
        })

        for skill in cat.get("skills", []):
            sid   = skill["id"]
            prof  = skill.get("proficiency", "Proficient")
            color = PROFICIENCY_COLOR.get(prof, "#4FC3F7")
            # Size = number of linked proofs
            proof_count = (
                len(skill.get("projects", [])) +
                len(skill.get("experience", [])) +
                len(skill.get("research", []))
            )
            size = max(16, min(36, 14 + proof_count * 4))

            nodes.append({
                "id":         sid,
                "name":       skill["name"],
                "symbolSize": size,
                "itemStyle":  {"color": color},
                "label":      {"fontSize": 10},
                "category":   cat_id,
                "value":      prof,
            })
            links.append({"source": cat_id, "target": sid, "lineStyle": {"opacity": 0.3}})

    return nodes, links


def _render_skill_detail(skill: dict, projects: list, experience: list):
    """Render the evidence panel for a selected skill."""
    name  = skill.get("name", "")
    prof  = skill.get("proficiency", "")
    since = skill.get("since", "")
    last  = skill.get("last_used", "active")
    learning = skill.get("currently_learning", False)
    color = PROFICIENCY_COLOR.get(prof, "#4FC3F7")

    st.markdown(f"""
    <div class="skill-detail-panel">
      <div class="skill-name-large" style="color:{color}">{name}</div>
      <div class="skill-proficiency">
        <span style="color:{color};font-weight:600">{prof}</span>
        &nbsp;·&nbsp; Since {since}
        &nbsp;·&nbsp; {"Active today" if last == "active" else f"Last used: {last}"}
        {"&nbsp;·&nbsp; 📚 Currently deepening" if learning else ""}
      </div>
    """, unsafe_allow_html=True)

    # Linked projects
    linked_proj_ids = skill.get("projects", [])
    linked_projs    = [p for p in projects if p.get("id") in linked_proj_ids]
    if linked_projs:
        st.markdown('<div class="evidence-label">Projects using this skill</div>', unsafe_allow_html=True)
        st.markdown('<div class="evidence-row">', unsafe_allow_html=True)
        for p in linked_projs:
            if st.button(f"🚀 {p.get('title', p['id'])}", key=f"skill_proj_{p['id']}_{name}"):
                st.session_state.active_project = p["id"]
                sm.navigate("projects")
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # Linked experience
    linked_exp_ids = skill.get("experience", [])
    linked_exp     = [e for e in experience if e.get("id") in linked_exp_ids]
    if linked_exp:
        exp_tags = "".join(
            f'<span class="tech-tag">💼 {e.get("org","")}</span>' for e in linked_exp
        )
        st.markdown(
            f'<div class="evidence-label">Where I used it professionally</div>'
            f'<div class="evidence-row">{exp_tags}</div>',
            unsafe_allow_html=True,
        )

    # Linked research
    linked_res = skill.get("research", [])
    if linked_res:
        res_map = {"published": "✅ Published", "under_review": "⏳ Under Review", "in_progress": "🔬 In Progress"}
        res_tags = "".join(
            f'<span class="tech-tag">{res_map.get(r, r)}</span>' for r in linked_res
        )
        st.markdown(
            f'<div class="evidence-label">Appears in research</div>'
            f'<div class="evidence-row">{res_tags}</div>',
            unsafe_allow_html=True,
        )

    # GitHub link
    gh_link = skill.get("github_search", "")
    if gh_link:
        st.markdown(
            f'<a href="{gh_link}" target="_blank" class="btn btn-ghost" style="margin-top:8px">⌥ View on GitHub</a>',
            unsafe_allow_html=True,
        )

    st.markdown('</div>', unsafe_allow_html=True)


def render():
    skills_data = load_skills()
    projects    = load_projects()
    experience  = load_experience()
    categories  = skills_data.get("categories", [])

    st.markdown('<div class="forge-editor-canvas">', unsafe_allow_html=True)

    st.markdown("""
    <div class="forge-comment">
      // Skills — evidence-based · every skill links to proof · no percentage bars
    </div>
    """, unsafe_allow_html=True)

    # ── Category filter ──────────────────────────────────────
    if "skills_filter" not in st.session_state:
        st.session_state.skills_filter = "all"

    filter_labels = [("all", "All Skills")] + [(c["id"], c["label"]) for c in categories]
    filter_cols   = st.columns(len(filter_labels))
    for i, (key, label) in enumerate(filter_labels):
        with filter_cols[i]:
            btn_type = "primary" if st.session_state.skills_filter == key else "secondary"
            if st.button(label, key=f"sf_{key}", use_container_width=True, type=btn_type):
                st.session_state.skills_filter = key
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Skill selector (flat list fallback — always works) ───
    active_filter = st.session_state.skills_filter
    all_skills    = []
    for cat in categories:
        if active_filter == "all" or cat["id"] == active_filter:
            for skill in cat.get("skills", []):
                all_skills.append((cat, skill))

    # Try ECharts graph, fall back to skill cards
    try:
        from streamlit_echarts import st_echarts

        nodes, links = _build_graph_data(skills_data)
        # Filter if needed
        if active_filter != "all":
            visible_ids = {s["id"] for _, s in all_skills} | {active_filter}
            nodes = [n for n in nodes if n["id"] in visible_ids]
            links = [l for l in links if l["source"] in visible_ids and l["target"] in visible_ids]

        option = {
            "backgroundColor": "#0D1117",
            "tooltip":  {"trigger": "item", "formatter": "{b}<br/>{c}"},
            "legend":   {"show": False},
            "series": [{
                "type":             "graph",
                "layout":           "force",
                "data":             nodes,
                "links":            links,
                "roam":             True,
                "draggable":        True,
                "label":            {"show": True, "position": "right", "color": "#8B949E", "fontSize": 10},
                "lineStyle":        {"color": "#30363D", "curveness": 0.1},
                "emphasis":         {"focus": "adjacency"},
                "force":            {"repulsion": 180, "edgeLength": [60, 120], "gravity": 0.08},
                "itemStyle":        {"borderColor": "#0D1117", "borderWidth": 2},
            }],
        }
        events = {"click": "function(params){return params.data.id}"}
        clicked = st_echarts(option, height="420px", events=events, key="skills_graph")

        if clicked:
            # Find clicked skill
            for _, skill in all_skills:
                if skill["id"] == clicked:
                    st.session_state.active_skill = skill
                    break

    except Exception:
        # Fallback: skill cards in a grid
        st.markdown("""
        <div style="font-family:var(--mono);font-size:11px;color:var(--text-2);margin-bottom:16px">
          💡 Install streamlit-echarts for the interactive skill graph.
        </div>
        """, unsafe_allow_html=True)

        cols = st.columns(3)
        for i, (cat, skill) in enumerate(all_skills):
            prof  = skill.get("proficiency", "")
            color = PROFICIENCY_COLOR.get(prof, "#4FC3F7")
            proof = (
                len(skill.get("projects", [])) +
                len(skill.get("experience", [])) +
                len(skill.get("research", []))
            )
            with cols[i % 3]:
                if st.button(
                    f"{skill['name']}\n{prof} · {proof} proofs",
                    key=f"skill_card_{skill['id']}",
                    use_container_width=True,
                ):
                    st.session_state.active_skill = skill
                    st.rerun()

    # ── Skill detail panel ────────────────────────────────────
    active_skill = st.session_state.get("active_skill")
    if not active_skill and all_skills:
        # Default: show first skill
        active_skill = all_skills[0][1]

    if active_skill:
        st.markdown('<div class="forge-section-header">Skill Evidence</div>', unsafe_allow_html=True)
        _render_skill_detail(active_skill, projects, experience)

    # ── Proficiency legend ────────────────────────────────────
    st.markdown('<div class="forge-section-header">Proficiency Scale</div>', unsafe_allow_html=True)
    legend_html = '<div style="display:flex;gap:12px;flex-wrap:wrap">'
    for level, color in PROFICIENCY_COLOR.items():
        legend_html += (
            f'<div style="display:flex;align-items:center;gap:6px">'
            f'<span style="width:10px;height:10px;border-radius:50%;background:{color};display:inline-block"></span>'
            f'<span style="font-family:var(--mono);font-size:11px;color:var(--text-1)">{level}</span>'
            f'</div>'
        )
    legend_html += '</div>'
    st.markdown(legend_html, unsafe_allow_html=True)

    # ── Cross-links ──────────────────────────────────────────
    st.markdown('<div class="cross-link-bar"><span class="cross-link-label">Explore →</span>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("🚀 Projects", key="skill_nav_proj", use_container_width=True):
            sm.navigate("projects"); st.rerun()
    with c2:
        if st.button("💼 Experience", key="skill_nav_exp", use_container_width=True):
            sm.navigate("experience"); st.rerun()
    with c3:
        if st.button("🔬 Research", key="skill_nav_res", use_container_width=True):
            sm.navigate("research"); st.rerun()
    st.markdown('</div></div>', unsafe_allow_html=True)
