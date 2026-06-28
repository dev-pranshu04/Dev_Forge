"""
about.py — The default landing screen.
Shows the TypeScript developer object + profile card + stats + bio.
"""
import streamlit as st
from app.services.content_loader import load_about, load_config
from app.utils import state_manager as sm


def render(cfg: dict):
    meta, body = load_about()

    st.markdown('<div class="forge-editor-canvas">', unsafe_allow_html=True)

    # ── Code comment ────────────────────────────────────────
    st.markdown("""
    <div class="forge-comment">
      /**<br>
      &nbsp;* Pranshu Kumar — ML &amp; AI Engineer<br>
      &nbsp;* Building systems that turn raw data into decisions.<br>
      &nbsp;*/
    </div>
    """, unsafe_allow_html=True)

    # ── TypeScript developer object ──────────────────────────
    st.markdown(f"""
    <div class="forge-code-block">
      <div class="code-line"><span class="code-ln">1</span><span class="code-content"><span class="kw">const</span> <span class="prop">developer</span> <span class="op">=</span> {{</span></div>
      <div class="code-line"><span class="code-ln">2</span><span class="code-content">&nbsp;&nbsp;<span class="prop">name</span><span class="op">:</span> <span class="str">"Pranshu Kumar"</span>,</span></div>
      <div class="code-line"><span class="code-ln">3</span><span class="code-content">&nbsp;&nbsp;<span class="prop">role</span><span class="op">:</span> <span class="str">"ML &amp; AI Engineer"</span>,</span></div>
      <div class="code-line"><span class="code-ln">4</span><span class="code-content">&nbsp;&nbsp;<span class="prop">university</span><span class="op">:</span> <span class="str">"NSUT, Delhi"</span>,</span></div>
      <div class="code-line"><span class="code-ln">5</span><span class="code-content">&nbsp;&nbsp;<span class="prop">graduating</span><span class="op">:</span> <span class="str">"May 2026"</span>,</span></div>
      <div class="code-line"><span class="code-ln">6</span><span class="code-content">&nbsp;&nbsp;<span class="prop">focus</span><span class="op">:</span> [<span class="str">"LLMs"</span>, <span class="str">"RAG"</span>, <span class="str">"XAI"</span>, <span class="str">"HCI Research"</span>],</span></div>
      <div class="code-line"><span class="code-ln">7</span><span class="code-content">&nbsp;&nbsp;<span class="prop">openToWork</span><span class="op">:</span> <span class="bool">true</span>,</span></div>
      <div class="code-line"><span class="code-ln">8</span><span class="code-content">&nbsp;&nbsp;<span class="prop">availableFrom</span><span class="op">:</span> <span class="str">"July 2026"</span>,</span></div>
      <div class="code-line"><span class="code-ln">9</span><span class="code-content">}};</span></div>
      <div class="code-line"><span class="code-ln">10</span><span class="code-content">&nbsp;</span></div>
      <div class="code-line"><span class="code-ln">11</span><span class="code-content"><span class="kw">function</span> <span class="fn">introduce</span>() {{</span></div>
      <div class="code-line"><span class="code-ln">12</span><span class="code-content">&nbsp;&nbsp;<span class="kw">return</span> <span class="str">"I build ML systems that do something real."</span></span></div>
      <div class="code-line"><span class="code-ln">13</span><span class="code-content">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="op">+</span> <span class="str">"Not just models that score well on benchmarks."</span>;</span></div>
      <div class="code-line"><span class="code-ln">14</span><span class="code-content">}}</span></div>
    </div>
    """, unsafe_allow_html=True)

    # ── Open to Work badge ───────────────────────────────────
    st.markdown("""
    <div class="otw-badge">
      <div class="otw-dot"></div>
      Open to new opportunities — available from July 2026
    </div>
    """, unsafe_allow_html=True)

    # ── Profile card ─────────────────────────────────────────
    github  = cfg.get("github",   "https://github.com/dev-pranshu04")
    linkedin= cfg.get("linkedin", "https://linkedin.com/in/dev-pranshu")
    email   = cfg.get("email",    "dev.pranshu04@gmail.com")

    st.markdown(f"""
    <div class="profile-card">
      <div class="profile-avatar">PK</div>
      <div class="profile-info">
        <div class="profile-name">Pranshu Kumar</div>
        <div class="profile-role">ML &amp; AI Engineer &nbsp;·&nbsp; NSUT, Delhi &nbsp;·&nbsp; Graduating May 2026</div>
        <div class="profile-bio">
          Six internships across ML research, fintech UI, crypto analytics, and AI content automation.<br>
          Passionate about the intersection of data, systems, and human decision-making.<br>
          Currently working on RAG evaluation and explainable AI in clinical contexts.
        </div>
        <div class="profile-links">
          <a href="{github}" target="_blank" class="btn btn-secondary">⌥ GitHub</a>
          <a href="{linkedin}" target="_blank" class="btn btn-secondary">in LinkedIn</a>
          <a href="mailto:{email}" class="btn btn-secondary">@ Email</a>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Stats ────────────────────────────────────────────────
    st.markdown("""
    <div class="stat-row">
      <div class="stat-chip"><span class="stat-n">6</span><span class="stat-l">Internships</span></div>
      <div class="stat-chip"><span class="stat-n">4</span><span class="stat-l">Projects shipped</span></div>
      <div class="stat-chip"><span class="stat-n">3</span><span class="stat-l">Research papers</span></div>
      <div class="stat-chip"><span class="stat-n">1</span><span class="stat-l">Under Springer review</span></div>
      <div class="stat-chip"><span class="stat-n">0.912</span><span class="stat-l">Best ROC-AUC</span></div>
      <div class="stat-chip"><span class="stat-n">94.8%</span><span class="stat-l">Class XII, School Topper</span></div>
    </div>
    """, unsafe_allow_html=True)

    # ── Current focus ────────────────────────────────────────
    st.markdown('<div class="forge-section-header">Current Focus</div>', unsafe_allow_html=True)
    focus_items = [
        ("🔍", "RAG evaluation", "Measuring retrieval faithfulness under domain shift"),
        ("🧠", "Explainable AI", "SHAP-based clinical risk interpretation"),
        ("🤖", "LLM fine-tuning", "LoRA/QLoRA for domain-specific tasks"),
        ("📱", "HCI Research",   "Automated usability evaluation framework (Springer, under review)"),
    ]
    cols = st.columns(2)
    for i, (icon, title, desc) in enumerate(focus_items):
        with cols[i % 2]:
            st.markdown(f"""
            <div style="background:var(--bg-1);border:1px solid var(--border);border-radius:var(--radius-m);
                        padding:14px 16px;margin-bottom:12px">
              <div style="font-family:var(--mono);font-size:13px;color:var(--text-0);margin-bottom:4px">
                {icon} {title}
              </div>
              <div style="font-family:var(--mono);font-size:11px;color:var(--text-2)">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    # ── Philosophy excerpt ───────────────────────────────────
    if body:
        st.markdown('<div class="forge-section-header">Working Philosophy</div>', unsafe_allow_html=True)
        # Render the markdown body
        st.markdown(
            f'<div style="font-family:var(--mono);font-size:12px;color:var(--text-1);'
            f'line-height:1.8;background:var(--bg-1);border:1px solid var(--border);'
            f'border-radius:var(--radius-m);padding:20px 24px">{body}</div>',
            unsafe_allow_html=True,
        )

    # ── Cross-links ──────────────────────────────────────────
    st.markdown('<div class="cross-link-bar"><span class="cross-link-label">Explore →</span>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("💼 Experience", key="about_nav_exp", use_container_width=True):
            sm.navigate("experience"); st.rerun()
    with c2:
        if st.button("🚀 Projects", key="about_nav_proj", use_container_width=True):
            sm.navigate("projects"); st.rerun()
    with c3:
        if st.button("🔬 Research", key="about_nav_res", use_container_width=True):
            sm.navigate("research"); st.rerun()
    with c4:
        if st.button("🎮 Playground", key="about_nav_play", use_container_width=True):
            sm.navigate("playground"); st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  # close editor-canvas
