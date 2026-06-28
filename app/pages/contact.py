"""contact.py — Contact page styled as a TSX file."""
import streamlit as st
from app.utils import state_manager as sm


def render(cfg: dict):
    email    = cfg.get("email",    "dev.pranshu04@gmail.com")
    github   = cfg.get("github",   "https://github.com/dev-pranshu04")
    linkedin = cfg.get("linkedin", "https://linkedin.com/in/dev-pranshu")
    avail    = cfg.get("status_message", "Open to new opportunities from July 2026")

    st.markdown('<div class="forge-editor-canvas">', unsafe_allow_html=True)

    st.markdown("""
    <div class="forge-comment">// Let's build something together</div>
    """, unsafe_allow_html=True)

    # Availability badge
    st.markdown(f"""
    <div class="otw-badge" style="margin-bottom:24px">
      <div class="otw-dot"></div>
      {avail}
    </div>
    """, unsafe_allow_html=True)

    # Contact method cards
    st.markdown(f"""
    <div class="contact-method-grid">
      <a href="mailto:{email}" style="text-decoration:none">
        <div class="contact-method">
          <div class="contact-method-label">✉ EMAIL</div>
          <div class="contact-method-value">{email}</div>
        </div>
      </a>
      <a href="{linkedin}" target="_blank" style="text-decoration:none">
        <div class="contact-method">
          <div class="contact-method-label">in LINKEDIN</div>
          <div class="contact-method-value">/in/dev-pranshu</div>
        </div>
      </a>
      <a href="{github}" target="_blank" style="text-decoration:none">
        <div class="contact-method">
          <div class="contact-method-label">⌥ GITHUB</div>
          <div class="contact-method-value">@dev-pranshu04</div>
        </div>
      </a>
      <div class="contact-method">
        <div class="contact-method-label">◆ TWITTER</div>
        <div class="contact-method-value" style="color:var(--text-2)">Not active</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # sendMessage form styled as code
    st.markdown("""
    <div style="font-family:var(--mono);font-size:13px;color:var(--text-0);margin:24px 0 12px">
      <span style="color:#569CD6">sendMessage</span>(<span style="color:var(--text-0)">{</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="form-field-label">&nbsp;&nbsp;name:</div>', unsafe_allow_html=True)
    name = st.text_input("", placeholder='"Your Name"', key="contact_name", label_visibility="collapsed")

    st.markdown('<div class="form-field-label" style="margin-top:8px">&nbsp;&nbsp;email:</div>', unsafe_allow_html=True)
    email_in = st.text_input("", placeholder='"you@company.com"', key="contact_email", label_visibility="collapsed")

    st.markdown('<div class="form-field-label" style="margin-top:8px">&nbsp;&nbsp;message:</div>', unsafe_allow_html=True)
    message = st.text_area("", placeholder='"Tell me about your project..."', key="contact_msg", height=120, label_visibility="collapsed")

    st.markdown("""
    <div style="font-family:var(--mono);font-size:13px;color:var(--text-0);margin:8px 0 16px">
      <span style="color:var(--text-0)">}</span>)
    </div>
    """, unsafe_allow_html=True)

    if st.button("⟶ Send Message", key="contact_send", type="primary"):
        if name and email_in and message:
            st.markdown("""
            <div class="game-answer-option correct" style="margin-top:12px">
              ✅ Message received! I'll get back to you within 24 hours.
            </div>
            """, unsafe_allow_html=True)
            st.balloons()
        else:
            st.markdown("""
            <div class="game-answer-option wrong" style="margin-top:12px">
              ❌ Please fill in all fields before sending.
            </div>
            """, unsafe_allow_html=True)

    # Open to work details
    st.markdown('<div class="forge-section-header">Open To</div>', unsafe_allow_html=True)
    collab_types = ["Full-time roles", "Research internships", "Research collaborations", "Freelance ML projects"]
    tags = "".join(f'<span class="tech-tag">{t}</span>' for t in collab_types)
    st.markdown(f'<div style="display:flex;flex-wrap:wrap;gap:8px">{tags}</div>', unsafe_allow_html=True)

    st.markdown('<div class="cross-link-bar"><span class="cross-link-label">Explore →</span>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("👤 About", key="contact_nav_about", use_container_width=True):
            sm.navigate("about"); st.rerun()
    with c2:
        if st.button("📄 Resume", key="contact_nav_resume", use_container_width=True):
            sm.navigate("resume"); st.rerun()
    st.markdown('</div></div>', unsafe_allow_html=True)
