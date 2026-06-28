"""experience.py — Fixed: no raw HTML, uses st.write for bullets."""
import streamlit as st
from app.services.content_loader import load_experience
from app.utils import state_manager as sm

TYPE_COLOR = {"research":"var(--purple)","internship":"var(--accent)"}
TYPE_ICON  = {"research":"🔬","internship":"💼"}


def render():
    experience = load_experience()
    st.markdown('<div class="forge-editor-canvas">', unsafe_allow_html=True)
    st.markdown('<div class="forge-comment">// 3 years · 6 roles · ML research · UI design · AI engineering</div>', unsafe_allow_html=True)

    # Filter
    if "exp_filter" not in st.session_state:
        st.session_state.exp_filter = "all"
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("All Roles", key="ef_all", use_container_width=True,
                     type="primary" if st.session_state.exp_filter=="all" else "secondary"):
            st.session_state.exp_filter = "all"; st.rerun()
    with c2:
        if st.button("ML / Research", key="ef_ml", use_container_width=True,
                     type="primary" if st.session_state.exp_filter=="research" else "secondary"):
            st.session_state.exp_filter = "research"; st.rerun()
    with c3:
        if st.button("Design / Dev", key="ef_design", use_container_width=True,
                     type="primary" if st.session_state.exp_filter=="internship" else "secondary"):
            st.session_state.exp_filter = "internship"; st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    for entry in experience:
        etype = entry.get("type", "internship")
        filt  = st.session_state.exp_filter
        if filt != "all" and etype != filt:
            continue

        org      = entry.get("org", "")
        role     = entry.get("role", "")
        start    = entry.get("start", "")
        end      = entry.get("end", "")
        duration = entry.get("duration", "")
        location = entry.get("location", "")
        bullets  = entry.get("bullets", [])
        tech     = entry.get("tech", [])
        highlight= entry.get("highlight", "")
        org_url  = entry.get("org_url", "")
        color    = TYPE_COLOR.get(etype, "var(--accent)")
        icon     = TYPE_ICON.get(etype, "💼")

        # Card header
        org_link = f'<a href="{org_url}" target="_blank" style="color:{color};text-decoration:none">{icon} {org}</a>' if org_url else f'<span style="color:{color}">{icon} {org}</span>'
        hl_html  = f'<span class="highlight-chip" style="margin-left:8px">{highlight}</span>' if highlight else ""

        st.markdown(f"""
        <div class="timeline-entry">
          <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:8px;margin-bottom:12px">
            <div>
              <div class="timeline-org">{org_link}</div>
              <div class="timeline-role">{role}</div>
            </div>
            <div class="timeline-meta">
              {start} — {end}<br>
              <span style="color:var(--text-2)">{duration} · {location}</span><br>
              {hl_html}
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Bullets — rendered SEPARATELY to avoid HTML escaping issue
        with st.container():
            for bullet in bullets:
                st.markdown(
                    f'<div style="font-family:var(--mono);font-size:12px;color:var(--text-1);'
                    f'padding:3px 0 3px 24px;line-height:1.7;position:relative;">'
                    f'<span style="position:absolute;left:8px;color:var(--accent)">▸</span>'
                    f'{bullet}</div>',
                    unsafe_allow_html=True
                )

        # Tech tags
        if tech:
            tags = " ".join(f'<span class="tech-tag">{t}</span>' for t in tech)
            st.markdown(
                f'<div style="display:flex;flex-wrap:wrap;gap:6px;margin-top:12px;'
                f'margin-bottom:8px;padding:0 0 12px 0;border-bottom:1px solid var(--border)">'
                f'{tags}</div>',
                unsafe_allow_html=True
            )

    # Cross-links
    st.markdown('<div class="cross-link-bar"><span class="cross-link-label">Next →</span>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("🚀 Projects", key="exp_proj", use_container_width=True):
            sm.navigate("projects"); st.rerun()
    with c2:
        if st.button("🛠 Skills", key="exp_skill", use_container_width=True):
            sm.navigate("skills"); st.rerun()
    with c3:
        if st.button("🎓 Education", key="exp_edu", use_container_width=True):
            sm.navigate("education"); st.rerun()
    st.markdown('</div></div>', unsafe_allow_html=True)
