"""readme.py — Workspace documentation, for explorers who click it intentionally."""
import streamlit as st
from app.utils import state_manager as sm


def render(cfg: dict):
    name    = cfg.get("name", "Pranshu Kumar")
    product = cfg.get("product_name", "Forge")

    st.markdown('<div class="forge-editor-canvas">', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="forge-comment">
      # {product} — {name}'s Developer Workspace<br>
      # A portfolio built as a software product.
    </div>

    <div class="forge-code-block" style="margin-bottom:24px">
      <div class="code-line"><span class="code-ln">1</span>
        <span class="code-content"><span class="cmt">## What is this?</span></span></div>
      <div class="code-line"><span class="code-ln">2</span>
        <span class="code-content">&nbsp;</span></div>
      <div class="code-line"><span class="code-ln">3</span>
        <span class="code-content">This is <span class="str">Forge</span> — {name}'s developer workspace.</span></div>
      <div class="code-line"><span class="code-ln">4</span>
        <span class="code-content">Not a traditional portfolio. A product built to demonstrate</span></div>
      <div class="code-line"><span class="code-ln">5</span>
        <span class="code-content">engineering thinking, research depth, and design maturity.</span></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="forge-section-header">How to Navigate</div>', unsafe_allow_html=True)

    nav_items = [
        ("about.md",       "Who I am, what I build, and what I'm focused on right now"),
        ("experience.md",  "6 professional roles — ML research, AI engineering, UI design"),
        ("projects/",      "4 shipped projects — case study format with architecture and lessons"),
        ("research/",      "3 papers — Published · Under Review · In Progress"),
        ("skills.json",    "Evidence-based skills — every skill links to proof"),
        ("playground/",    "6 interactive games — Groq generates a new scenario every round"),
        ("education.md",   "NSUT B.Tech CSAI · 94.8% school topper"),
        ("achievements.md","Leadership at ARES Society · Rotaract · Certifications"),
        ("contact.tsx",    "sendMessage() — let's build something together"),
    ]

    for filename, desc in nav_items:
        dot_class = "dot-md" if filename.endswith(".md") else \
                    "dot-json" if filename.endswith(".json") else \
                    "dot-tsx" if filename.endswith(".tsx") else "dot-ts"
        st.markdown(f"""
        <div style="display:flex;align-items:flex-start;gap:12px;padding:10px 0;
                    border-bottom:1px solid var(--border)">
          <span class="file-dot {dot_class}" style="margin-top:4px;flex-shrink:0"></span>
          <div>
            <div style="font-family:var(--mono);font-size:12px;font-weight:600;
                        color:var(--accent);margin-bottom:2px">{filename}</div>
            <div style="font-family:var(--mono);font-size:11px;color:var(--text-2)">{desc}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="forge-section-header">Keyboard Shortcuts</div>', unsafe_allow_html=True)
    shortcuts = [("Click any filename", "Open that section"), ("Tab navigation", "Move between open tabs")]
    for key, desc in shortcuts:
        st.markdown(f"""
        <div style="display:flex;gap:16px;padding:6px 0;font-family:var(--mono);font-size:12px">
          <span style="color:var(--accent);min-width:180px">{key}</span>
          <span style="color:var(--text-1)">{desc}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="cross-link-bar"><span class="cross-link-label">Start here →</span>', unsafe_allow_html=True)
    if st.button("👤 Open About", key="readme_nav_about", type="primary"):
        sm.navigate("about"); st.rerun()
    st.markdown('</div></div>', unsafe_allow_html=True)
