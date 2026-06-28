"""
experience.py — Vertical timeline of all professional roles.
"""
import streamlit as st
from app.services.content_loader import load_experience
from app.utils import state_manager as sm

TYPE_ICON = {"research": "🔬", "internship": "💼", "design": "🎨"}
TYPE_COLOR = {"research": "var(--purple)", "internship": "var(--accent)", "design": "var(--orange)"}


def render():
    experience = load_experience()

    st.markdown('<div class="forge-editor-canvas">', unsafe_allow_html=True)

    st.markdown("""
    <div class="forge-comment">// 3 years of hands-on experience · 6 roles · ML research · UI design · AI engineering</div>
    """, unsafe_allow_html=True)

    # ── Filter tabs ─────────────────────────────────────────
    col_all, col_ml, col_design = st.columns(3)
    if "exp_filter" not in st.session_state:
        st.session_state.exp_filter = "all"

    with col_all:
        if st.button("All Roles", key="exp_all", use_container_width=True):
            st.session_state.exp_filter = "all"
    with col_ml:
        if st.button("ML / Research", key="exp_ml", use_container_width=True):
            st.session_state.exp_filter = "research"
    with col_design:
        if st.button("Design / Dev", key="exp_design", use_container_width=True):
            st.session_state.exp_filter = "design"

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Timeline ─────────────────────────────────────────────
    st.markdown('<div class="timeline">', unsafe_allow_html=True)

    filter_val = st.session_state.exp_filter
    design_types = {"internship"}  # broad catch-all for non-research

    for entry in experience:
        etype = entry.get("type", "internship")

        # Filter logic
        if filter_val == "research" and etype != "research":
            continue
        if filter_val == "design" and etype not in design_types:
            continue

        org      = entry.get("org", "")
        role     = entry.get("role", "")
        start    = entry.get("start", "")
        end      = entry.get("end", "")
        duration = entry.get("duration", "")
        location = entry.get("location", "")
        bullets  = entry.get("bullets", [])
        tech     = entry.get("tech", [])
        highlight= entry.get("highlight")
        org_url  = entry.get("org_url", "")
        icon     = TYPE_ICON.get(etype, "💼")
        color    = TYPE_COLOR.get(etype, "var(--accent)")

        # Build bullet HTML
        bullets_html = "".join(f"<li>{b}</li>" for b in bullets)
        tech_html    = "".join(
            f'<span class="tech-tag">{t}</span>' for t in tech
        )
        hl_html = f'<span class="highlight-chip">{highlight}</span>' if highlight else ""
        org_html = f'<a href="{org_url}" target="_blank" style="color:{color};text-decoration:none">{org}</a>' if org_url else f'<span style="color:{color}">{org}</span>'

        st.markdown(f"""
        <div style="position:relative;margin-bottom:8px">
          <div class="timeline-node" style="border-color:{color}"></div>
          <div class="timeline-entry">
            <div class="timeline-header">
              <div>
                <div class="timeline-org">{icon} {org_html}</div>
                <div class="timeline-role">{role}</div>
              </div>
              <div class="timeline-meta">
                {start} — {end}<br>
                <span style="color:var(--text-2)">{duration}</span><br>
                <span style="color:var(--text-2)">{location}</span>
                {hl_html}
              </div>
            </div>
            <ul class="timeline-bullets">{bullets_html}</ul>
            <div style="display:flex;flex-wrap:wrap;gap:6px;margin-top:12px">
              {tech_html}
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  # close timeline

    # ── Cross-links ──────────────────────────────────────────
    st.markdown('<div class="cross-link-bar"><span class="cross-link-label">Next →</span>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("🚀 Projects", key="exp_nav_proj", use_container_width=True):
            sm.navigate("projects"); st.rerun()
    with c2:
        if st.button("🛠 Skills", key="exp_nav_skill", use_container_width=True):
            sm.navigate("skills"); st.rerun()
    with c3:
        if st.button("🎓 Education", key="exp_nav_edu", use_container_width=True):
            sm.navigate("education"); st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  # close editor-canvas
