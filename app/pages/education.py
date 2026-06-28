"""
education.py — Academic background with course highlights.
"""
import streamlit as st
from app.services.content_loader import load_education
from app.utils import state_manager as sm


def render():
    education = load_education()
    st.markdown('<div class="forge-editor-canvas">', unsafe_allow_html=True)
    st.markdown("""
    <div class="forge-comment">// education.md — academic foundation</div>
    """, unsafe_allow_html=True)

    for edu in education:
        institution = edu.get("institution", "")
        degree      = edu.get("degree", "")
        field       = edu.get("field", "")
        spec        = edu.get("specialisation", "")
        start       = edu.get("start", "")
        end         = edu.get("end", "")
        status      = edu.get("status", "completed")
        location    = edu.get("location", "")
        coursework  = edu.get("coursework", [])
        achievements= edu.get("achievements", [])
        url         = edu.get("url", "")

        status_badge = (
            '<span class="badge badge-production">Current</span>'
            if status == "current" else
            '<span class="badge" style="background:var(--bg-2);color:var(--text-2);border:1px solid var(--border)">Completed</span>'
        )
        inst_html = f'<a href="{url}" target="_blank" style="color:var(--accent);text-decoration:none">{institution}</a>' if url else f'<span style="color:var(--accent)">{institution}</span>'
        spec_str  = f" &nbsp;·&nbsp; Specialisation: {spec}" if spec else ""
        course_html = "".join(f'<span class="tech-tag">{c}</span>' for c in coursework)
        ach_html    = "".join(f'<li>{a}</li>' for a in achievements)

        st.markdown(f"""
        <div class="timeline-entry" style="margin-bottom:20px">
          <div class="timeline-header">
            <div>
              <div style="font-family:var(--mono);font-size:15px;font-weight:600;color:var(--text-0)">
                {inst_html}
              </div>
              <div style="font-family:var(--mono);font-size:13px;color:var(--text-1);margin-top:2px">
                {degree} — {field}{spec_str}
              </div>
            </div>
            <div class="timeline-meta">
              {start} — {end}<br>
              <span style="color:var(--text-2)">{location}</span><br>
              {status_badge}
            </div>
          </div>
          {f'<div style="margin-top:12px"><div class="evidence-label">Key Coursework</div><div class="evidence-row" style="margin-top:6px">{course_html}</div></div>' if course_html else ""}
          {f'<ul class="timeline-bullets" style="margin-top:12px">{ach_html}</ul>' if ach_html else ""}
        </div>
        """, unsafe_allow_html=True)

    # Cross-links
    st.markdown('<div class="cross-link-bar"><span class="cross-link-label">Next →</span>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🏆 Achievements", key="edu_nav_ach", use_container_width=True):
            sm.navigate("achievements"); st.rerun()
    with c2:
        if st.button("🛠 Skills", key="edu_nav_skill", use_container_width=True):
            sm.navigate("skills"); st.rerun()
    st.markdown('</div></div>', unsafe_allow_html=True)
