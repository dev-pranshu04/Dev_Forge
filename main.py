"""
main.py — Forge. Rebuilt with st.sidebar for reliable layout.
Works on desktop and mobile. No column hacks.
"""
import time
import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="Forge — Pranshu Kumar",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ───────────────────────────────────────────────────────
css_path = Path("app/styles/forge_theme.css")
if css_path.exists():
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

from app.utils import state_manager as sm
from app.services.content_loader import load_config

sm.init()
cfg     = load_config()
NAME    = cfg.get("name", "Pranshu Kumar")
PRODUCT = cfg.get("product_name", "Forge")

# ── Boot ──────────────────────────────────────────────────────
if not st.session_state.boot_done:
    boot = st.empty()
    boot.markdown(f"""
    <div class="boot-overlay">
      <div class="boot-logo">{PRODUCT}</div>
      <div class="boot-sub">{NAME} · ML &amp; AI Engineer</div>
      <div class="boot-progress"><div class="boot-progress-bar"></div></div>
      <div class="boot-skip">Loading workspace…</div>
    </div>
    """, unsafe_allow_html=True)
    time.sleep(2)
    st.session_state.boot_done = True
    boot.empty()
    st.rerun()

# ── Title bar (fixed HTML) ────────────────────────────────────
st.markdown(f"""
<div class="forge-title-bar">
  <div class="title-left">
    <span class="tl-close"></span>
    <span class="tl-min"></span>
    <span class="tl-max"></span>
    <span class="title-name">{NAME} — {PRODUCT}</span>
  </div>
  <div class="title-center">
    {NAME} — {PRODUCT} — Visual Studio Code
  </div>
  <div class="title-right">
    <span>File</span><span>Edit</span><span>View</span><span>Terminal</span>
  </div>
</div>
<div class="title-spacer"></div>
""", unsafe_allow_html=True)

# ── File tree data ────────────────────────────────────────────
TAB_META = {
    "about":        {"label": "about.md",        "dot": "dot-md",   "lang": "Markdown"},
    "skills":       {"label": "skills.json",      "dot": "dot-json", "lang": "JSON"},
    "projects":     {"label": "projects/",        "dot": "dot-ts",   "lang": "TypeScript"},
    "research":     {"label": "research/",        "dot": "dot-md",   "lang": "Markdown"},
    "experience":   {"label": "experience.md",    "dot": "dot-md",   "lang": "Markdown"},
    "education":    {"label": "education.md",     "dot": "dot-md",   "lang": "Markdown"},
    "playground":   {"label": "playground/",      "dot": "dot-ts",   "lang": "TypeScript"},
    "achievements": {"label": "achievements.md",  "dot": "dot-md",   "lang": "Markdown"},
    "contact":      {"label": "contact.tsx",      "dot": "dot-tsx",  "lang": "TSX"},
    "readme":       {"label": "README.md",        "dot": "dot-md",   "lang": "Markdown"},
    "resume":       {"label": "resume.pdf",       "dot": "dot-pdf",  "lang": "PDF"},
}

# ── Sidebar (native Streamlit — works on mobile) ──────────────
with st.sidebar:
    st.markdown('<div class="sb-header">EXPLORER</div>', unsafe_allow_html=True)
    st.markdown('<div class="sb-section">▾ FORGE / src</div>', unsafe_allow_html=True)

    active = sm.get_active()

    def nav_btn(label: str, key: str, dot: str, indent: int = 0):
        is_a = key == active
        pad  = indent * 14
        cls  = "sb-item-active" if is_a else "sb-item"
        st.markdown(
            f'<div class="{cls}" style="padding-left:{pad+12}px">'
            f'<span class="file-dot {dot}"></span>'
            f'<span class="sb-label">{label}</span></div>',
            unsafe_allow_html=True,
        )
        if st.button(label, key=f"nav_{key}", label_visibility="collapsed",
                     use_container_width=True):
            sm.navigate(key)
            st.rerun()

    nav_btn("about.md",       "about",        "dot-md",   0)
    nav_btn("skills.json",    "skills",       "dot-json", 0)

    st.markdown('<div class="sb-folder" style="padding-left:12px">▾ projects</div>',
                unsafe_allow_html=True)
    nav_btn("resumeiq.ts",    "projects",     "dot-ts",   1)
    nav_btn("cardiorisk.ts",  "projects",     "dot-ts",   1)
    nav_btn("nanocluster.ts", "projects",     "dot-ts",   1)

    st.markdown('<div class="sb-folder" style="padding-left:12px">▾ research</div>',
                unsafe_allow_html=True)
    nav_btn("published.md",   "research",     "dot-md",   1)
    nav_btn("under_review.md","research",     "dot-md",   1)
    nav_btn("in_progress.md", "research",     "dot-md",   1)

    nav_btn("experience.md",  "experience",   "dot-md",   0)
    nav_btn("education.md",   "education",    "dot-md",   0)

    st.markdown('<div class="sb-folder" style="padding-left:12px">▾ playground</div>',
                unsafe_allow_html=True)
    nav_btn("bug_hunter.ts",  "playground",   "dot-ts",   1)
    nav_btn("git_rescue.ts",  "playground",   "dot-ts",   1)
    nav_btn("ml_academy.ts",  "playground",   "dot-ts",   1)

    nav_btn("achievements.md","achievements", "dot-md",   0)
    nav_btn("contact.tsx",    "contact",      "dot-tsx",  0)
    nav_btn("README.md",      "readme",       "dot-md",   0)
    nav_btn("resume.pdf",     "resume",       "dot-pdf",  0)

    st.markdown("""
    <div class="sb-footer">
      <div class="avatar-pk">PK</div>
      <span class="sb-branch">✓ main — up to date</span>
    </div>
    """, unsafe_allow_html=True)

# ── Editor area ───────────────────────────────────────────────
active    = sm.get_active()
open_tabs = sm.get_tabs()
meta      = TAB_META.get(active, {"label": active, "dot": "dot-md", "lang": "Text"})

# Tab bar — horizontal radio styled as tabs
if open_tabs:
    tab_labels = [TAB_META.get(t, {"label": t})["label"] for t in open_tabs]
    active_idx = open_tabs.index(active) if active in open_tabs else 0
    selected_label = st.radio(
        "tabs", tab_labels,
        index=active_idx,
        horizontal=True,
        label_visibility="collapsed",
        key="tab_radio"
    )
    # Map label back to key
    for t in open_tabs:
        if TAB_META.get(t, {}).get("label") == selected_label and t != active:
            sm.navigate(t)
            st.rerun()

# Breadcrumb
st.markdown(
    f'<div class="forge-breadcrumb">'
    f'<span class="bc-path">forge › <span class="bc-active">{meta["label"]}</span></span>'
    f'<span class="bc-lang">{meta["lang"]}</span>'
    f'</div>',
    unsafe_allow_html=True
)

# ── Route ────────────────────────────────────────────────────
if active == "about":
    from app.pages.about import render; render(cfg)
elif active == "experience":
    from app.pages.experience import render; render()
elif active == "projects":
    from app.pages.projects import render; render()
elif active == "research":
    from app.pages.research import render; render()
elif active == "skills":
    from app.pages.skills import render; render()
elif active == "playground":
    from app.pages.playground import render; render()
elif active == "education":
    from app.pages.education import render; render()
elif active == "achievements":
    from app.pages.achievements import render; render()
elif active == "contact":
    from app.pages.contact import render; render(cfg)
elif active == "readme":
    from app.pages.readme import render; render(cfg)
elif active == "resume":
    st.markdown('<div class="forge-editor-canvas" style="text-align:center;padding:60px 0">', unsafe_allow_html=True)
    st.markdown('<div style="font-size:48px">📄</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-family:var(--mono);color:var(--text-1);margin:12px 0 24px">resume.pdf</div>', unsafe_allow_html=True)
    rp = Path("assets/resume.pdf")
    if rp.exists():
        with open(rp, "rb") as f:
            st.download_button("⬇ Download Resume", f.read(), "Pranshu_Kumar_Resume.pdf", "application/pdf")
    else:
        st.markdown('<p style="font-family:var(--mono);font-size:12px;color:var(--text-2)">Place your PDF at assets/resume.pdf</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
else:
    sm.navigate("about"); st.rerun()

# ── Status bar ────────────────────────────────────────────────
active = sm.get_active()
lang   = TAB_META.get(active, {"lang": "Text"})["lang"]
st.markdown(f"""
<div class="forge-status-bar">
  <div class="status-left">
    <span>⎇ main</span>
    <span>✓ 0 errors</span>
  </div>
  <div class="status-right">
    <span>Ln 1, Col 1</span>
    <span>UTF-8</span>
    <span>{lang}</span>
  </div>
</div>
""", unsafe_allow_html=True)
