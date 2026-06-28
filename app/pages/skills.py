"""skills.py — Evidence-based skills. Always shows card grid. ECharts optional."""
import streamlit as st
from app.services.content_loader import load_skills, load_projects, load_experience
from app.utils import state_manager as sm

PROF_COLOR = {
    "Beginner":"#6E7681","Building":"#D29922",
    "Proficient":"#4FC3F7","Advanced":"#3FB950","Deep expertise":"#BC8CFF"
}


def render():
    skills_data = load_skills()
    projects    = load_projects()
    experience  = load_experience()
    categories  = skills_data.get("categories", [])

    st.markdown('<div class="forge-editor-canvas">', unsafe_allow_html=True)
    st.markdown('<div class="forge-comment">// Skills — evidence-based · every skill links to proof · no percentage bars</div>', unsafe_allow_html=True)

    # Category filter
    if "skills_filter" not in st.session_state:
        st.session_state.skills_filter = "all"

    filter_opts = [("all","All Skills")] + [(c["id"], c["label"]) for c in categories]
    fcols = st.columns(len(filter_opts))
    for i, (key, label) in enumerate(filter_opts):
        with fcols[i]:
            t = "primary" if st.session_state.skills_filter == key else "secondary"
            if st.button(label, key=f"sf_{key}", use_container_width=True, type=t):
                st.session_state.skills_filter = key
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Build filtered skill list
    active_filter = st.session_state.skills_filter
    all_skills = []
    for cat in categories:
        if active_filter in ("all", cat["id"]):
            for skill in cat.get("skills", []):
                all_skills.append((cat, skill))

    if not all_skills:
        st.markdown('<div class="forge-comment">// No skills found for this filter.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        return

    # Try ECharts graph
    graph_shown = False
    try:
        from streamlit_echarts import st_echarts
        nodes, links = [], []
        for cat in categories:
            if active_filter not in ("all", cat["id"]):
                continue
            nodes.append({"id":cat["id"],"name":cat["label"],"symbolSize":28,
                          "itemStyle":{"color":cat.get("color","#4FC3F7")},
                          "label":{"fontSize":11,"fontWeight":"bold"}})
            for skill in cat.get("skills",[]):
                proof = len(skill.get("projects",[])) + len(skill.get("experience",[])) + len(skill.get("research",[]))
                size  = max(16, min(36, 14 + proof*4))
                color = PROF_COLOR.get(skill.get("proficiency",""), "#4FC3F7")
                nodes.append({"id":skill["id"],"name":skill["name"],"symbolSize":size,
                              "itemStyle":{"color":color},"label":{"fontSize":10},
                              "value":skill.get("proficiency","")})
                links.append({"source":cat["id"],"target":skill["id"]})

        option = {
            "backgroundColor":"#0D1117",
            "tooltip":{"trigger":"item","formatter":"{b} — {c}"},
            "series":[{"type":"graph","layout":"force","data":nodes,"links":links,
                       "roam":True,"draggable":True,
                       "label":{"show":True,"position":"right","color":"#8B949E","fontSize":10},
                       "lineStyle":{"color":"#30363D","curveness":0.1},
                       "force":{"repulsion":180,"edgeLength":[60,120],"gravity":0.08},
                       "itemStyle":{"borderColor":"#0D1117","borderWidth":2}}]
        }
        events = {"click":"function(p){return p.data.id}"}
        clicked = st_echarts(option, height="380px", events=events, key="skills_graph")
        graph_shown = True

        if clicked:
            for _, skill in all_skills:
                if skill["id"] == clicked:
                    st.session_state.active_skill = skill
                    break
    except Exception:
        pass

    # Skill card grid (always shown — primary interface if no graph)
    st.markdown('<div class="forge-section-header">All Skills</div>', unsafe_allow_html=True)
    cols = st.columns(3)
    for i, (cat, skill) in enumerate(all_skills):
        prof  = skill.get("proficiency","Proficient")
        color = PROF_COLOR.get(prof, "#4FC3F7")
        proof = (len(skill.get("projects",[])) + len(skill.get("experience",[])) + len(skill.get("research",[])))
        learning = " · 📚 learning" if skill.get("currently_learning") else ""
        with cols[i % 3]:
            st.markdown(f"""
            <div style="background:var(--bg-1);border:1px solid var(--border);border-radius:var(--r6);
                        padding:12px 14px;margin-bottom:10px;cursor:pointer"
                 onclick="">
              <div style="font-family:var(--mono);font-size:13px;font-weight:600;
                          color:{color};margin-bottom:4px">{skill['name']}</div>
              <div style="font-family:var(--mono);font-size:10px;color:var(--text-2)">
                {prof}{learning}
              </div>
              <div style="font-family:var(--mono);font-size:10px;color:var(--text-2);margin-top:4px">
                {proof} proof{"s" if proof!=1 else ""} linked
              </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"View {skill['name']}", key=f"sk_{skill['id']}", use_container_width=True):
                st.session_state.active_skill = skill
                st.rerun()

    # Detail panel
    active_skill = st.session_state.get("active_skill") or (all_skills[0][1] if all_skills else None)
    if active_skill:
        st.markdown('<div class="forge-section-header">Skill Evidence</div>', unsafe_allow_html=True)
        prof  = active_skill.get("proficiency","")
        color = PROF_COLOR.get(prof, "#4FC3F7")
        since = active_skill.get("since","")
        last  = active_skill.get("last_used","active")
        learn = active_skill.get("currently_learning", False)

        st.markdown(f"""
        <div class="skill-detail-panel">
          <div class="skill-name-large" style="color:{color}">{active_skill.get('name','')}</div>
          <div class="skill-proficiency">
            <span style="color:{color};font-weight:600">{prof}</span>
            &nbsp;·&nbsp; Since {since}
            &nbsp;·&nbsp; {"Active today" if last=="active" else f"Last: {last}"}
            {"&nbsp;·&nbsp; 📚 Currently deepening" if learn else ""}
          </div>
        """, unsafe_allow_html=True)

        # Linked projects
        proj_ids = active_skill.get("projects",[])
        linked_p = [p for p in projects if p.get("id") in proj_ids]
        if linked_p:
            st.markdown('<div class="evidence-label">Projects using this skill</div>', unsafe_allow_html=True)
            pc = st.columns(len(linked_p))
            for j, p in enumerate(linked_p):
                with pc[j]:
                    if st.button(f"🚀 {p.get('title',p['id'])}", key=f"sp_{p['id']}_{active_skill['id']}"):
                        st.session_state.active_project = p["id"]
                        sm.navigate("projects"); st.rerun()

        # Linked experience
        exp_ids = active_skill.get("experience",[])
        linked_e = [e for e in experience if e.get("id") in exp_ids]
        if linked_e:
            etags = " ".join(f'<span class="tech-tag">💼 {e.get("org","")}</span>' for e in linked_e)
            st.markdown(f'<div class="evidence-label">Professional use</div><div class="evidence-row">{etags}</div>', unsafe_allow_html=True)

        # Linked research
        res_ids = active_skill.get("research",[])
        if res_ids:
            rmap = {"published":"✅ Published","under_review":"⏳ Under Review","in_progress":"🔬 In Progress"}
            rtags = " ".join(f'<span class="tech-tag">{rmap.get(r,r)}</span>' for r in res_ids)
            st.markdown(f'<div class="evidence-label">Appears in research</div><div class="evidence-row">{rtags}</div>', unsafe_allow_html=True)

        gh = active_skill.get("github_search","")
        if gh:
            st.markdown(f'<a href="{gh}" target="_blank" class="btn btn-ghost" style="margin-top:8px">⌥ View on GitHub</a>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Legend
    st.markdown('<div class="forge-section-header">Proficiency Scale</div>', unsafe_allow_html=True)
    legend = " ".join(
        f'<span style="display:inline-flex;align-items:center;gap:6px;margin-right:12px">'
        f'<span style="width:10px;height:10px;border-radius:50%;background:{c};display:inline-block"></span>'
        f'<span style="font-family:var(--mono);font-size:11px;color:var(--text-1)">{l}</span></span>'
        for l, c in PROF_COLOR.items()
    )
    st.markdown(f'<div style="flex-wrap:wrap;display:flex">{legend}</div>', unsafe_allow_html=True)

    st.markdown('<div class="cross-link-bar"><span class="cross-link-label">Explore →</span>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("🚀 Projects", key="sk_proj", use_container_width=True): sm.navigate("projects"); st.rerun()
    with c2:
        if st.button("💼 Experience", key="sk_exp", use_container_width=True): sm.navigate("experience"); st.rerun()
    with c3:
        if st.button("🔬 Research", key="sk_res", use_container_width=True): sm.navigate("research"); st.rerun()
    st.markdown('</div></div>', unsafe_allow_html=True)

