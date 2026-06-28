"""
research.py — Three-tab research viewer: Published · Under Review · In Progress.
"""
import streamlit as st
from app.services.content_loader import load_research
from app.services import groq_service
from app.utils import state_manager as sm

STATUS_CONFIG = {
    "published":    {"label": "Published",    "badge": "badge-published", "icon": "✅"},
    "under_review": {"label": "Under Review", "badge": "badge-review",    "icon": "⏳"},
    "in_progress":  {"label": "In Progress",  "badge": "badge-progress",  "icon": "🔬"},
}


def render():
    research = load_research()

    st.markdown('<div class="forge-editor-canvas">', unsafe_allow_html=True)

    st.markdown("""
    <div class="forge-comment">
      // Research — 1 published · 1 under review at Springer · 1 in active development
    </div>
    """, unsafe_allow_html=True)

    # ── Tab selector ─────────────────────────────────────────
    tab_cols = st.columns(3)
    active_tab = st.session_state.get("active_research_tab", "under_review")

    labels = [
        ("published",    "✅ Published"),
        ("under_review", "⏳ Under Review"),
        ("in_progress",  "🔬 In Progress"),
    ]
    for i, (key, label) in enumerate(labels):
        with tab_cols[i]:
            btn_type = "primary" if active_tab == key else "secondary"
            if st.button(label, key=f"res_tab_{key}", use_container_width=True, type=btn_type):
                st.session_state.active_research_tab = key
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Active research entry ────────────────────────────────
    entry  = research.get(active_tab, {})
    meta   = entry.get("meta", {})
    body   = entry.get("body", "")
    config = STATUS_CONFIG[active_tab]

    if not meta and not body:
        st.markdown("""
        <div class="forge-comment" style="margin-top:24px">
          // This research entry is being prepared.<br>
          // Check back for updates, or explore the other tabs.
        </div>
        """, unsafe_allow_html=True)
    else:
        title   = meta.get("title",   "Untitled Research")
        authors = meta.get("authors", "Pranshu Kumar")
        venue   = meta.get("venue",   "")
        year    = meta.get("year",    "")
        keywords= meta.get("keywords", [])
        doi     = meta.get("doi",     "")
        pdf     = meta.get("pdf",     "")
        target  = meta.get("venue",   "")

        # Keywords can be a list or string from frontmatter
        if isinstance(keywords, str):
            keywords = [k.strip() for k in keywords.split(",")]

        kw_html = "".join(
            f'<span class="tech-tag">{k}</span>' for k in keywords if k
        )

        st.markdown(f"""
        <div class="research-card">
          <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:12px;flex-wrap:wrap;gap:8px">
            <span class="badge {config['badge']}">{config['icon']} {config['label']}</span>
            <span style="font-family:var(--mono);font-size:11px;color:var(--text-2)">{year}</span>
          </div>

          <div class="research-title">{title}</div>
          <div class="research-authors">👥 {authors}</div>
          <div class="research-venue">📍 {venue}</div>

          <div class="research-keywords">{kw_html}</div>
        </div>
        """, unsafe_allow_html=True)

        # Body content (abstract + sections)
        if body:
            # Split into sections by ## headers
            sections = body.split("\n## ")
            for i, section in enumerate(sections):
                if not section.strip():
                    continue
                if i == 0:
                    # First section has no ## prefix
                    lines = section.strip().splitlines()
                    heading = lines[0].lstrip("#").strip() if lines[0].startswith("#") else None
                    content = "\n".join(lines[1:] if heading else lines).strip()
                    if heading:
                        st.markdown(
                            f'<div class="forge-section-header">{heading}</div>'
                            f'<div class="research-abstract">{content}</div>',
                            unsafe_allow_html=True,
                        )
                    else:
                        st.markdown(
                            f'<div class="research-abstract">{content}</div>',
                            unsafe_allow_html=True,
                        )
                else:
                    lines   = section.strip().splitlines()
                    heading = lines[0].strip()
                    content = "\n".join(lines[1:]).strip()
                    st.markdown(
                        f'<div class="forge-section-header">{heading}</div>'
                        f'<div class="research-abstract">{content}</div>',
                        unsafe_allow_html=True,
                    )

        # Links row
        links_html = '<div style="display:flex;gap:8px;margin-top:16px;flex-wrap:wrap">'
        if doi and doi != "placeholder":
            links_html += f'<a href="https://doi.org/{doi}" target="_blank" class="btn btn-secondary">DOI ↗</a>'
        if pdf:
            links_html += f'<a href="{pdf}" target="_blank" class="btn btn-secondary">📄 PDF</a>'
        if target and active_tab == "in_progress":
            links_html += f'<span class="badge badge-progress" style="align-self:center">Target: {target}</span>'
        links_html += '</div>'
        st.markdown(links_html, unsafe_allow_html=True)

        # ── AI explain ───────────────────────────────────────
        st.markdown('<div style="margin-top:24px">', unsafe_allow_html=True)
        explain_key = f"res_explain_{active_tab}"
        if explain_key not in st.session_state:
            st.session_state[explain_key] = None

        if st.button("✦ Explain this research in plain English", key=f"res_explain_btn_{active_tab}"):
            with st.spinner("Generating plain-language summary…"):
                st.session_state[explain_key] = groq_service.explain_research(entry)

        if st.session_state[explain_key]:
            st.markdown(
                f'<div class="explanation-box">✦ {st.session_state[explain_key]}</div>',
                unsafe_allow_html=True,
            )
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Cross-links ──────────────────────────────────────────
    st.markdown('<div class="cross-link-bar"><span class="cross-link-label">Related →</span>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("🚀 Projects", key="res_nav_proj", use_container_width=True):
            sm.navigate("projects"); st.rerun()
    with c2:
        if st.button("🛠 Skills", key="res_nav_skill", use_container_width=True):
            sm.navigate("skills"); st.rerun()
    with c3:
        if st.button("💼 Experience", key="res_nav_exp", use_container_width=True):
            sm.navigate("experience"); st.rerun()
    st.markdown('</div></div>', unsafe_allow_html=True)
