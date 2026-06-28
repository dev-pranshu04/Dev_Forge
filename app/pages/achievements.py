"""achievements.py — Leadership, certifications, awards."""
import streamlit as st
from app.services.content_loader import load_achievements
from app.utils import state_manager as sm

TYPE_ICON  = {"leadership": "🏛", "certification": "📜", "award": "🏆"}
TYPE_COLOR = {"leadership": "var(--purple)", "certification": "var(--amber)", "award": "var(--accent)"}


def render():
    achievements = load_achievements()
    st.markdown('<div class="forge-editor-canvas">', unsafe_allow_html=True)
    st.markdown("""
    <div class="forge-comment">// achievements.md — leadership · certifications · recognition</div>
    """, unsafe_allow_html=True)

    # Split by type
    leadership = [a for a in achievements if a.get("type") == "leadership"]
    certs      = [a for a in achievements if a.get("type") == "certification"]
    awards     = [a for a in achievements if a.get("type") == "award"]

    def render_section(title: str, items: list, icon: str, color: str):
        if not items:
            return
        st.markdown(f'<div class="forge-section-header">{icon} {title}</div>', unsafe_allow_html=True)
        for item in items:
            impact = item.get("impact", "")
            desc   = item.get("description", "")
            start  = item.get("start", "")
            end    = item.get("end", "")
            date_str = f"{start} — {end}" if start else ""

            st.markdown(f"""
            <div class="timeline-entry" style="margin-bottom:12px">
              <div class="timeline-header">
                <div>
                  <div style="font-family:var(--mono);font-size:14px;font-weight:600;color:var(--text-0)">
                    {item.get('title','')}
                  </div>
                  <div style="font-family:var(--mono);font-size:12px;color:{color};margin-top:2px">
                    {item.get('org','')}
                  </div>
                </div>
                <div class="timeline-meta">{date_str}</div>
              </div>
              {f'<div style="font-family:var(--mono);font-size:12px;color:var(--text-1);margin-top:10px;line-height:1.7">{desc}</div>' if desc else ""}
              {f'<div class="highlight-chip" style="margin-top:10px">{impact}</div>' if impact else ""}
            </div>
            """, unsafe_allow_html=True)

    render_section("Leadership", leadership, "🏛", "var(--purple)")
    render_section("Certifications", certs, "📜", "var(--amber)")
    render_section("Awards", awards, "🏆", "var(--accent)")

    st.markdown('<div class="cross-link-bar"><span class="cross-link-label">Next →</span>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("📬 Contact", key="ach_nav_contact", use_container_width=True):
            sm.navigate("contact"); st.rerun()
    with c2:
        if st.button("🎓 Education", key="ach_nav_edu", use_container_width=True):
            sm.navigate("education"); st.rerun()
    st.markdown('</div></div>', unsafe_allow_html=True)
