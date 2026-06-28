"""
main.py — Forge entry point.
Renders the shell (title bar, activity bar, explorer, tab bar, status bar)
and routes to the active page inside the editor canvas.
"""
import time
import streamlit as st
from pathlib import Path

# ── Page config (must be first) ─────────────────────────────
st.set_page_config(
    page_title="Forge — Pranshu Kumar",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Load CSS ─────────────────────────────────────────────────
css_path = Path("app/styles/forge_theme.css")
if css_path.exists():
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ── Foundation imports ───────────────────────────────────────
from app.utils import state_manager as sm
from app.services.content_loader import load_config

# ── Init session state ───────────────────────────────────────
sm.init()

# ── Load config ──────────────────────────────────────────────
cfg = load_config()
NAME     = cfg.get("name", "Pranshu Kumar")
PRODUCT  = cfg.get("product_name", "Forge")
TITLE_STR = cfg.get("title", "ML & AI Engineer")
ACCENT   = cfg.get("accent_color", "#4FC3F7")

# ── Boot sequence (runs once per session) ────────────────────
if not st.session_state.boot_done:
    boot = st.empty()
    boot.markdown(f"""
    <div class="boot-overlay">
      <div class="boot-logo">{PRODUCT}</div>
      <div class="boot-sub">{NAME} &nbsp;·&nbsp; {TITLE_STR}</div>
      <div class="boot-progress"><div class="boot-progress-bar"></div></div>
      <div class="boot-skip">Loading workspace…</div>
    </div>
    """, unsafe_allow_html=True)
    time.sleep(2)
    st.session_state.boot_done = True
    boot.empty()
    st.rerun()

# ── Title Bar ────────────────────────────────────────────────
st.markdown(f"""
<div class="forge-title-bar">
  <div class="traffic-lights">
    <div class="traffic-light tl-close"></div>
    <div class="traffic-light tl-min"></div>
    <div class="traffic-light tl-max"></div>
    <span style="font-family:var(--mono);font-size:11px;color:var(--text-2);margin-left:8px">
      {NAME} — {PRODUCT}
    </span>
  </div>
  <div class="title-text">{NAME} — {PRODUCT} — Visual Studio Code</div>
  <div class="title-menu">
    <span class="title-menu-item">File</span>
    <span class="title-menu-item">Edit</span>
    <span class="title-menu-item">View</span>
    <span class="title-menu-item">Terminal</span>
    <span class="title-menu-item">Help</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── File tree data ────────────────────────────────────────────
FILE_TREE = [
    {"label": "▾ FORGE",           "key": None,            "type": "section", "indent": 0},
    {"label": "▾ src",             "key": None,            "type": "folder",  "indent": 0},
    {"label": "about.md",          "key": "about",         "type": "md",      "indent": 1},
    {"label": "skills.json",       "key": "skills",        "type": "json",    "indent": 1},
    {"label": "▾ projects",        "key": None,            "type": "folder",  "indent": 1},
    {"label": "resumeiq.ts",       "key": "projects",      "type": "ts",      "indent": 2},
    {"label": "cardiorisk.ts",     "key": "projects",      "type": "ts",      "indent": 2},
    {"label": "nanocluster.ts",    "key": "projects",      "type": "ts",      "indent": 2},
    {"label": "▾ research",        "key": None,            "type": "folder",  "indent": 1},
    {"label": "published.md",      "key": "research",      "type": "md",      "indent": 2},
    {"label": "under_review.md",   "key": "research",      "type": "md",      "indent": 2},
    {"label": "in_progress.md",    "key": "research",      "type": "md",      "indent": 2},
    {"label": "experience.md",     "key": "experience",    "type": "md",      "indent": 1},
    {"label": "education.md",      "key": "education",     "type": "md",      "indent": 1},
    {"label": "▾ playground",      "key": None,            "type": "folder",  "indent": 1},
    {"label": "bug_hunter.ts",     "key": "playground",    "type": "ts",      "indent": 2},
    {"label": "git_rescue.ts",     "key": "playground",    "type": "ts",      "indent": 2},
    {"label": "ml_academy.ts",     "key": "playground",    "type": "ts",      "indent": 2},
    {"label": "achievements.md",   "key": "achievements",  "type": "md",      "indent": 1},
    {"label": "contact.tsx",       "key": "contact",       "type": "tsx",     "indent": 1},
    {"label": "README.md",         "key": "readme",        "type": "md",      "indent": 1},
    {"label": "resume.pdf",        "key": "resume",        "type": "pdf",     "indent": 1},
]

DOT_CLASS = {"ts": "dot-ts", "md": "dot-md", "tsx": "dot-tsx", "json": "dot-json", "pdf": "dot-pdf"}
FILE_LANG  = {"ts": "TypeScript", "md": "Markdown", "tsx": "TSX", "json": "JSON", "pdf": "PDF"}

# ── Tab metadata ──────────────────────────────────────────────
TAB_META = {
    "about":        {"label": "about.md",        "type": "md"},
    "skills":       {"label": "skills.json",      "type": "json"},
    "projects":     {"label": "projects/",        "type": "ts"},
    "research":     {"label": "research/",        "type": "md"},
    "experience":   {"label": "experience.md",    "type": "md"},
    "education":    {"label": "education.md",     "type": "md"},
    "playground":   {"label": "playground/",      "type": "ts"},
    "achievements": {"label": "achievements.md",  "type": "md"},
    "contact":      {"label": "contact.tsx",      "type": "tsx"},
    "readme":       {"label": "README.md",        "type": "md"},
}

# ── Three-column workspace layout ────────────────────────────
col_activity, col_sidebar, col_editor = st.columns([1, 4, 14], gap="small")

# ─── Activity Bar ─────────────────────────────────────────────
with col_activity:
    st.markdown("""
    <div class="forge-activity-bar">
      <div class="activity-icon active" title="Explorer">⊞</div>
      <div class="activity-icon" title="Search">⊘</div>
      <div class="activity-icon" title="AI Assistant">✦</div>
      <div class="activity-icon bottom" title="Settings">⚙</div>
    </div>
    """, unsafe_allow_html=True)

# ─── Explorer Sidebar ──────────────────────────────────────────
with col_sidebar:
    st.markdown('<div class="forge-sidebar">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-section-title">Explorer</div>', unsafe_allow_html=True)

    active = sm.get_active()

    for item in FILE_TREE:
        if item["type"] == "section":
            st.markdown(f'<div class="sidebar-section-title" style="padding-top:8px">{item["label"]}</div>', unsafe_allow_html=True)
            continue
        if item["type"] == "folder":
            indent_cls = f"indent-{item['indent']}" if item["indent"] else ""
            st.markdown(f'<div class="file-tree-item folder {indent_cls}">{item["label"]}</div>', unsafe_allow_html=True)
            continue

        # Clickable file items
        dot  = DOT_CLASS.get(item["type"], "dot-md")
        indent_cls = f"indent-{item['indent']}"
        is_active  = (item["key"] == active)
        active_cls = "active" if is_active else ""

        if item["key"] == "resume":
            st.markdown(
                f'<div class="file-tree-item {indent_cls}">'
                f'<span class="file-dot {dot}"></span>{item["label"]}</div>',
                unsafe_allow_html=True
            )
        elif item["key"]:
            if st.button(
                f'{"  " * item["indent"]}· {item["label"]}',
                key=f"nav_{item['label']}_{item['key']}",
                use_container_width=True,
                type="secondary",
            ):
                sm.navigate(item["key"])
                st.rerun()

    # Sidebar footer
    st.markdown("""
    <div class="sidebar-footer">
      <div class="avatar-pk">PK</div>
      <div class="branch-info">✓ main — up to date</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ─── Editor Area ───────────────────────────────────────────────
with col_editor:
    active      = sm.get_active()
    open_tabs   = sm.get_tabs()
    tab_info    = TAB_META.get(active, {"label": active, "type": "md"})
    lang_label  = FILE_LANG.get(tab_info["type"], "Text")

    # Tab bar
    tab_html = '<div class="forge-tab-bar">'
    for t in open_tabs:
        meta  = TAB_META.get(t, {"label": t, "type": "md"})
        dot   = DOT_CLASS.get(meta["type"], "dot-md")
        is_a  = "active" if t == active else ""
        tab_html += (
            f'<div class="forge-tab {is_a}">'
            f'<span class="file-dot tab-dot {dot}"></span>'
            f'<span class="tab-name">{meta["label"]}</span>'
            f'</div>'
        )
    tab_html += "</div>"
    st.markdown(tab_html, unsafe_allow_html=True)

    # Clickable tab buttons (real interactivity)
    if len(open_tabs) > 1:
        tab_cols = st.columns(len(open_tabs))
        for i, t in enumerate(open_tabs):
            with tab_cols[i]:
                meta = TAB_META.get(t, {"label": t, "type": "md"})
                if st.button(meta["label"], key=f"tab_{t}", use_container_width=True):
                    sm.navigate(t)
                    st.rerun()

    # Breadcrumb
    st.markdown(
        f'<div class="forge-breadcrumb">'
        f'<span class="breadcrumb-path">forge › <span>{tab_info["label"]}</span></span>'
        f'<span class="breadcrumb-lang">{lang_label}</span>'
        f'</div>',
        unsafe_allow_html=True
    )

    # ── Route to active page ─────────────────────────────────
    if active == "about":
        from app.pages.about import render
        render(cfg)
    elif active == "experience":
        from app.pages.experience import render
        render()
    elif active == "projects":
        from app.pages.projects import render
        render()
    elif active == "research":
        from app.pages.research import render
        render()
    elif active == "skills":
        from app.pages.skills import render
        render()
    elif active == "playground":
        from app.pages.playground import render
        render()
    elif active == "education":
        from app.pages.education import render
        render()
    elif active == "achievements":
        from app.pages.achievements import render
        render()
    elif active == "contact":
        from app.pages.contact import render
        render(cfg)
    elif active == "readme":
        from app.pages.readme import render
        render(cfg)
    elif active == "resume":
        st.markdown("""
        <div class="forge-editor-canvas">
          <div class="forge-comment">// resume.pdf — download to view</div>
          <div style="text-align:center;padding:60px 0">
            <div style="font-family:var(--mono);font-size:48px;margin-bottom:16px">📄</div>
            <div style="font-family:var(--mono);font-size:14px;color:var(--text-1);margin-bottom:24px">
              Pranshu_Kumar_Resume.pdf
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)
        resume_path = Path("assets/resume.pdf")
        if resume_path.exists():
            with open(resume_path, "rb") as f:
                st.download_button(
                    "⬇ Download Resume",
                    f.read(),
                    file_name="Pranshu_Kumar_Resume.pdf",
                    mime="application/pdf",
                )
        else:
            st.markdown(
                '<p style="font-family:var(--mono);font-size:12px;color:var(--text-2);text-align:center">'
                'Resume file not found. Place your PDF at assets/resume.pdf</p>',
                unsafe_allow_html=True,
            )
    else:
        sm.navigate("about")
        st.rerun()

# ── Status Bar ───────────────────────────────────────────────
active    = sm.get_active()
tab_info  = TAB_META.get(active, {"label": active, "type": "md"})
lang      = FILE_LANG.get(tab_info["type"], "Text")

st.markdown(f"""
<div class="forge-status-bar">
  <div class="status-left">
    <span class="status-item">⎇ main</span>
    <span class="status-item">✓ 0 errors, 0 warnings</span>
  </div>
  <div class="status-right">
    <span class="status-item">Ln 1, Col 1</span>
    <span class="status-item">UTF-8</span>
    <span class="status-item">{lang}</span>
    <span class="status-item">Spaces: 2</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Command palette hint ─────────────────────────────────────
st.markdown("""
<style>
div[data-testid="stVerticalBlock"] > div > div > div > div[data-testid="stButton"] button {
  font-size: 11px !important;
  padding: 2px 8px !important;
  height: auto !important;
  min-height: 0 !important;
}
</style>
""", unsafe_allow_html=True)
