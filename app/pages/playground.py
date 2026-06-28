"""
playground.py — All 6 educational games. Groq generates a fresh scenario
every round, making each visit unique across unlimited plays.
"""
import streamlit as st
from app.services import groq_service
from app.utils import state_manager as sm

GAMES = [
    {
        "id":    "bug_hunter",
        "icon":  "🐛",
        "title": "Bug Hunter",
        "desc":  "Find and fix the bug in a realistic code snippet. Groq generates a fresh bug every round — Python, JS, SQL, and more.",
        "topic": "Debugging & Code Reasoning",
        "live":  True,
    },
    {
        "id":    "git_rescue",
        "icon":  "🔀",
        "title": "Git Rescue",
        "desc":  "Your repository is broken. Diagnose the problem and write the correct git commands to fix it.",
        "topic": "Git Workflows",
        "live":  True,
    },
    {
        "id":    "terminal_quest",
        "icon":  "💻",
        "title": "Terminal Quest",
        "desc":  "Solve Linux terminal puzzles — pipes, grep, permissions, one-liners. Every puzzle is different.",
        "topic": "Linux & Shell",
        "live":  True,
    },
    {
        "id":    "ml_academy",
        "icon":  "🧠",
        "title": "ML Academy",
        "desc":  "Real ML scenarios — choose the right model, spot data leakage, fix the evaluation metric. Groq creates new dataset stories each time.",
        "topic": "Machine Learning Concepts",
        "live":  True,
    },
    {
        "id":    "dl_lab",
        "icon":  "🔬",
        "title": "Deep Learning Lab",
        "desc":  "Architecture decision challenges — pick the right layer, fix the network, explain why it breaks.",
        "topic": "Deep Learning Architecture",
        "live":  True,
    },
    {
        "id":    "nlp_detective",
        "icon":  "🕵️",
        "title": "NLP Detective",
        "desc":  "Find the hidden NLP problem in a text passage — prompt injection, hallucination, retrieval failure, tokenisation quirks.",
        "topic": "NLP & LLMs",
        "live":  True,
    },
]


# ── Game selector lobby ───────────────────────────────────────
def render_lobby():
    st.markdown("""
    <div class="forge-comment">
      // Playground — 6 interactive games · Groq generates infinite variations<br>
      // Every visit is different · Learn by doing
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(3)
    for i, game in enumerate(GAMES):
        with cols[i % 3]:
            live_badge = '<span class="badge badge-production" style="margin-bottom:8px">Live</span>' if game["live"] else '<span class="badge badge-review" style="margin-bottom:8px">Coming soon</span>'
            st.markdown(f"""
            <div class="game-card {'live' if game['live'] else ''}">
              <div>{live_badge}</div>
              <div class="game-icon">{game['icon']}</div>
              <div class="game-title">{game['title']}</div>
              <div class="game-desc">{game['desc']}</div>
              <div style="font-family:var(--mono);font-size:10px;color:var(--text-2);margin-top:4px">
                📚 {game['topic']}
              </div>
            </div>
            """, unsafe_allow_html=True)
            if game["live"]:
                if st.button(f"Play {game['title']}", key=f"play_{game['id']}", use_container_width=True, type="primary"):
                    sm.start_game(game["id"])
                    st.rerun()
            else:
                st.button("Coming Soon", key=f"soon_{game['id']}", disabled=True, use_container_width=True)


# ── Generic MCQ renderer (ML Academy, DL Lab, NLP Detective) ──
def render_mcq_game(game_id: str, scenario: dict):
    question = scenario.get("question", "")
    options  = scenario.get("options", [])
    correct  = scenario.get("correct", 0)
    answered = st.session_state.game_answered
    user_ans = st.session_state.game_user_answer

    st.markdown(f'<div class="game-scenario-box">{question}</div>', unsafe_allow_html=True)

    if not answered:
        for j, opt in enumerate(options):
            if st.button(opt, key=f"opt_{game_id}_{j}", use_container_width=True):
                st.session_state.game_user_answer = j
                st.session_state.game_answered    = True
                if j == correct:
                    st.session_state.game_score += 1
                st.session_state.game_attempts += 1
                st.rerun()
    else:
        for j, opt in enumerate(options):
            cls = "correct" if j == correct else ("wrong" if j == user_ans else "")
            icon = "✅ " if j == correct else ("❌ " if j == user_ans else "")
            st.markdown(
                f'<div class="game-answer-option {cls}">{icon}{opt}</div>',
                unsafe_allow_html=True,
            )


# ── Bug Hunter ────────────────────────────────────────────────
def render_bug_hunter():
    scenario = st.session_state.game_scenario
    if not scenario:
        return

    code     = scenario.get("code", "").replace("\\n", "\n")
    bug_line = scenario.get("bug_line", 1)
    answered = st.session_state.game_answered

    st.markdown(f"""
    <div class="game-scenario-box" style="background:var(--bg-1)">
      <div style="color:var(--text-2);font-size:10px;margin-bottom:8px">
        DIFFICULTY: {scenario.get('difficulty','medium').upper()} &nbsp;·&nbsp;
        Find the bug and select the line number.
      </div>
      <pre style="margin:0;color:var(--text-0);font-size:12px">{code}</pre>
    </div>
    """, unsafe_allow_html=True)

    lines = code.strip().splitlines()

    if not answered:
        st.markdown('<div style="font-family:var(--mono);font-size:12px;color:var(--text-1);margin-bottom:8px">Which line contains the bug?</div>', unsafe_allow_html=True)
        cols = st.columns(min(len(lines), 8))
        for i, _ in enumerate(lines, start=1):
            with cols[(i - 1) % len(cols)]:
                if st.button(f"Ln {i}", key=f"bugline_{i}"):
                    st.session_state.game_user_answer = i
                    st.session_state.game_answered    = True
                    if i == bug_line:
                        st.session_state.game_score += 1
                    st.session_state.game_attempts += 1
                    st.rerun()
    else:
        user_ans = st.session_state.game_user_answer
        if user_ans == bug_line:
            st.markdown(f'<div class="game-answer-option correct">✅ Correct! The bug is on line {bug_line}.</div>', unsafe_allow_html=True)
        else:
            st.markdown(
                f'<div class="game-answer-option wrong">❌ You chose line {user_ans}. The bug is on line {bug_line}.</div>',
                unsafe_allow_html=True,
            )


# ── Git Rescue ────────────────────────────────────────────────
def render_git_rescue():
    scenario = st.session_state.game_scenario
    if not scenario:
        return

    situation = scenario.get("situation", "")
    repo_state= scenario.get("repo_state", "")
    goal      = scenario.get("goal", "")
    answered  = st.session_state.game_answered

    st.markdown(f"""
    <div class="game-scenario-box">
      <div style="color:var(--amber);margin-bottom:8px;font-weight:600">⚠ SITUATION</div>
      {situation}
      <div style="color:var(--text-2);margin:12px 0 4px">CURRENT REPO STATE:</div>
      <pre style="color:var(--text-0);background:var(--bg-0);padding:10px;border-radius:4px;font-size:11px">{repo_state}</pre>
      <div style="color:var(--accent);margin-top:8px">GOAL: {goal}</div>
    </div>
    """, unsafe_allow_html=True)

    solution_cmds = scenario.get("solution_commands", [])
    solution_str  = "\n".join(solution_cmds)

    if not answered:
        user_input = st.text_area(
            "Write the git command(s) to fix this:",
            key="git_answer_input",
            height=100,
            placeholder="git ...",
        )
        if st.button("Submit", key="git_submit", type="primary"):
            st.session_state.game_user_answer = user_input.strip()
            st.session_state.game_answered    = True
            st.session_state.game_attempts   += 1
            # Simple scoring: check if key commands appear
            answered_lower = user_input.lower()
            key_cmds = [c.split()[1] if len(c.split()) > 1 else c for c in solution_cmds]
            if any(kw in answered_lower for kw in key_cmds):
                st.session_state.game_score += 1
            st.rerun()
    else:
        user_ans = st.session_state.game_user_answer or "(no answer)"
        st.markdown(f"""
        <div class="game-answer-option" style="background:var(--bg-2);margin-bottom:8px">
          Your answer:<br><code style="color:var(--accent)">{user_ans}</code>
        </div>
        <div class="game-answer-option correct">
          ✅ Solution:<br><code>{solution_str}</code>
        </div>
        """, unsafe_allow_html=True)


# ── Terminal Quest ────────────────────────────────────────────
def render_terminal_quest():
    scenario = st.session_state.game_scenario
    if not scenario:
        return

    context  = scenario.get("context", "")
    task     = scenario.get("task", "")
    answered = st.session_state.game_answered

    st.markdown(f"""
    <div class="game-scenario-box">
      <div style="color:var(--green);margin-bottom:8px">$ {context}</div>
      <div style="color:var(--text-0);margin-top:8px">
        <strong>Task:</strong> {task}
      </div>
    </div>
    """, unsafe_allow_html=True)

    if not answered:
        if st.button("💡 Show hint", key="tq_hint"):
            st.markdown(
                f'<div style="font-family:var(--mono);font-size:12px;color:var(--amber);'
                f'background:var(--amber-dim);padding:10px;border-radius:4px;margin-bottom:12px">'
                f'Hint: {scenario.get("hint", "")}</div>',
                unsafe_allow_html=True,
            )
        user_cmd = st.text_input("Your command:", key="tq_input", placeholder="$ ")
        if st.button("Submit", key="tq_submit", type="primary"):
            st.session_state.game_user_answer = user_cmd.strip()
            st.session_state.game_answered    = True
            st.session_state.game_attempts   += 1
            sol = scenario.get("solution", "").lower()
            if user_cmd.strip().lower() in sol or sol in user_cmd.strip().lower():
                st.session_state.game_score += 1
            st.rerun()
    else:
        solution = scenario.get("solution", "")
        st.markdown(f"""
        <div class="game-answer-option" style="background:var(--bg-2);margin-bottom:8px">
          You wrote: <code style="color:var(--accent)">{st.session_state.game_user_answer}</code>
        </div>
        <div class="game-answer-option correct">
          ✅ Solution: <code>{solution}</code>
        </div>
        """, unsafe_allow_html=True)


# ── Shared: explanation + next round ──────────────────────────
def render_post_answer(scenario: dict, game_id: str):
    if not st.session_state.game_answered:
        return

    explanation = scenario.get("explanation", "")
    concept     = scenario.get("concept", "") or scenario.get("bug_type", "")

    if explanation:
        st.markdown(
            f'<div class="explanation-box">'
            f'{"📚 " + concept + "<br>" if concept else ""}'
            f'{explanation}'
            f'</div>',
            unsafe_allow_html=True,
        )

    score    = st.session_state.game_score
    attempts = st.session_state.game_attempts
    st.markdown(
        f'<div style="font-family:var(--mono);font-size:12px;color:var(--text-2);margin-top:12px">'
        f'Score: {score}/{attempts}</div>',
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2)
    with c1:
        if st.button("⟳ Next Round", key=f"next_{game_id}", type="primary", use_container_width=True):
            sm.reset_game_round()
            st.rerun()
    with c2:
        if st.button("← Back to Games", key=f"exit_{game_id}", use_container_width=True):
            sm.exit_game()
            st.rerun()


# ── Main render ───────────────────────────────────────────────
def render():
    st.markdown('<div class="forge-editor-canvas">', unsafe_allow_html=True)

    active_game = st.session_state.get("active_game")

    if not active_game:
        render_lobby()
        st.markdown('</div>', unsafe_allow_html=True)
        return

    # Find game meta
    game_meta = next((g for g in GAMES if g["id"] == active_game), None)
    if not game_meta:
        sm.exit_game(); st.rerun()

    # Header
    score    = st.session_state.game_score
    attempts = st.session_state.game_attempts
    st.markdown(f"""
    <div style="display:flex;justify-content:space-between;align-items:center;
                margin-bottom:20px;padding-bottom:16px;border-bottom:1px solid var(--border)">
      <div>
        <span style="font-size:24px">{game_meta['icon']}</span>
        <span style="font-family:var(--mono);font-size:16px;font-weight:600;
                     color:var(--text-0);margin-left:8px">{game_meta['title']}</span>
        <span style="font-family:var(--mono);font-size:11px;color:var(--text-2);
                     margin-left:12px">📚 {game_meta['topic']}</span>
      </div>
      <div style="font-family:var(--mono);font-size:12px;color:var(--text-2)">
        Score: <span style="color:var(--accent)">{score}</span>/{attempts}
        &nbsp;·&nbsp;
        <span style="color:var(--green)">Groq-powered</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Load scenario if needed
    if st.session_state.game_scenario is None:
        with st.spinner(f"Generating new {game_meta['title']} scenario…"):
            scenario = groq_service.generate_scenario(active_game)

        if scenario is None:
            st.markdown("""
            <div class="explanation-box" style="border-left-color:var(--amber)">
              ⚠ Could not reach Groq API. Make sure your GROQ_API_KEY is set in
              Streamlit Secrets (.streamlit/secrets.toml).<br><br>
              Key: GROQ_API_KEY = "your-key-here"
            </div>
            """, unsafe_allow_html=True)
            if st.button("← Back to Games", key="back_no_api"):
                sm.exit_game(); st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
            return

        st.session_state.game_scenario = scenario
        st.rerun()

    scenario = st.session_state.game_scenario

    # Route to game renderer
    if active_game == "bug_hunter":
        render_bug_hunter()
    elif active_game == "git_rescue":
        render_git_rescue()
    elif active_game == "terminal_quest":
        render_terminal_quest()
    elif active_game in ("ml_academy", "dl_lab", "nlp_detective"):
        # All three use MCQ format
        context_key = {
            "ml_academy":   "scenario",
            "dl_lab":       "problem",
            "nlp_detective":"passage",
        }.get(active_game, "scenario")

        context_text = scenario.get(context_key, "")
        if context_text:
            st.markdown(
                f'<div class="game-scenario-box">{context_text}</div>',
                unsafe_allow_html=True,
            )
        render_mcq_game(active_game, scenario)

    # Post-answer explanation + next round
    render_post_answer(scenario, active_game)

    st.markdown('</div>', unsafe_allow_html=True)
