"""
projects.py — Split panel: project list (left) + case study detail (right).
"""
import streamlit as st
from app.services.content_loader import load_projects, get_project_by_id
from app.services import groq_service
from app.utils import state_manager as sm


def render():
    projects = load_projects()
    if not projects:
        st.markdown("""
        <div class="forge-editor-canvas">
          <div class="forge-comment">// No projects found. Add JSON files to content/projects/</div>
        </div>""", unsafe_allow_html=True)
        return

    # Ensure active project is valid
    if "active_project" not in st.session_state or \
       st.session_state.active_project not in [p["id"] for p in projects]:
        st.session_state.active_project = projects[0]["id"]

    active_id = st.session_state.active_project
    project   = get_project_by_id(active_id, projects)

    st.markdown('<div class="forge-editor-canvas" style="padding:0">', unsafe_allow_html=True)
    st.markdown("""
    <div style="padding:12px 24px;background:var(--bg-0);border-bottom:1px solid var(--border);
                font-family:var(--mono);font-size:12px;color:var(--text-2)">
      // Projects — Pranshu Kumar &nbsp;·&nbsp; Click a project to explore
    </div>
    """, unsafe_allow_html=True)

    # ── Split layout: list | detail ──────────────────────────
    col_list, col_detail = st.columns([2, 5], gap="small")

    with col_list:
        st.markdown("""
        <div class="project-list">
          <div class="project-list-header">PROJECTS</div>
        """, unsafe_allow_html=True)

        for p in projects:
            pid   = p.get("id", "")
            title = p.get("title", pid)
            status= p.get("status", "")
            badge_cls = "badge-production" if status == "production" else "badge-progress"
            is_active = "active" if pid == active_id else ""

            st.markdown(
                f'<div class="project-list-item {is_active}">'
                f'<span class="file-dot dot-ts"></span>{title}</div>',
                unsafe_allow_html=True,
            )
            if st.button(f"Open {title}", key=f"proj_{pid}", use_container_width=True):
                st.session_state.active_project = pid
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    with col_detail:
        st.markdown('<div class="project-detail">', unsafe_allow_html=True)

        # Header
        status   = project.get("status", "")
        badge_cls= "badge-production" if status == "production" else "badge-progress"
        badge_lbl= "production" if status == "production" else status
        github   = project.get("github", "")
        live     = project.get("live_demo", "")

        st.markdown(f"""
        <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:4px">
          <div>
            <div class="project-title">{project.get('title','')}</div>
            <div class="project-subtitle">{project.get('subtitle','')}</div>
          </div>
          <div>
            <span class="badge {badge_cls}">{badge_lbl}</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Action buttons
        btn_html = '<div class="project-actions">'
        if github:
            btn_html += f'<a href="{github}" target="_blank" class="btn btn-secondary">⌥ View Code</a>'
        if live:
            btn_html += f'<a href="{live}" target="_blank" class="btn btn-primary">↗ Live Demo</a>'
        btn_html += '</div>'
        st.markdown(btn_html, unsafe_allow_html=True)

        # Tech stack
        tech = project.get("tech", [])
        if tech:
            tags = "".join(f'<span class="tech-tag">{t}</span>' for t in tech)
            st.markdown(
                f'<div class="project-section-title">STACK</div>'
                f'<div style="display:flex;flex-wrap:wrap;gap:6px;margin-bottom:16px">{tags}</div>',
                unsafe_allow_html=True,
            )

        # Sections
        sections = [
            ("OVERVIEW",     project.get("overview",      "")),
            ("PROBLEM",      project.get("problem",       "")),
            ("SOLUTION",     project.get("solution",      "")),
            ("ARCHITECTURE", project.get("architecture",  "")),
            ("CHALLENGES",   project.get("challenges",    "")),
            ("RESULTS",      project.get("results",       "")),
            ("LESSONS",      project.get("lessons",       "")),
            ("FUTURE",       project.get("future",        "")),
        ]
        for label, text in sections:
            if text:
                st.markdown(
                    f'<div class="project-section-title">{label}</div>'
                    f'<div class="project-text">{text}</div>',
                    unsafe_allow_html=True,
                )

        # Features list
        features = project.get("features", [])
        if features:
            items = "".join(f"<li>{f}</li>" for f in features)
            st.markdown(
                f'<div class="project-section-title">FEATURES</div>'
                f'<ul class="timeline-bullets">{items}</ul>',
                unsafe_allow_html=True,
            )

        # ── AI explain button ────────────────────────────────
        st.markdown('<div class="forge-section-header">AI Explanation</div>', unsafe_allow_html=True)
        explain_key = f"explain_{active_id}"
        if explain_key not in st.session_state:
            st.session_state[explain_key] = None

        if st.button("✦ Explain for non-technical visitors", key=f"ai_explain_{active_id}"):
            with st.spinner("Generating explanation…"):
                st.session_state[explain_key] = groq_service.explain_project(project)

        if st.session_state[explain_key]:
            st.markdown(
                f'<div class="explanation-box">✦ {st.session_state[explain_key]}</div>',
                unsafe_allow_html=True,
            )

        # Related links
        related_skills = project.get("related_skills", [])
        related_res    = project.get("related_research", "")
        if related_skills or related_res:
            st.markdown('<div class="cross-link-bar"><span class="cross-link-label">Related →</span>', unsafe_allow_html=True)
            nav_cols = st.columns(3)
            with nav_cols[0]:
                if st.button("🛠 Skills", key=f"proj_nav_skill_{active_id}", use_container_width=True):
                    sm.navigate("skills"); st.rerun()
            with nav_cols[1]:
                if related_res and st.button("🔬 Research", key=f"proj_nav_res_{active_id}", use_container_width=True):
                    sm.navigate("research"); st.rerun()
            with nav_cols[2]:
                if st.button("💼 Experience", key=f"proj_nav_exp_{active_id}", use_container_width=True):
                    sm.navigate("experience"); st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)  # close project-detail

    st.markdown('</div>', unsafe_allow_html=True)  # close editor-canvas

