"""
StateManager — owns every session_state key in Forge.
No other file reads or writes session_state directly.
"""
import streamlit as st


DEFAULTS = {
    # Navigation
    "active_file": "about",
    "open_tabs": ["about"],
    "active_project": "resumeiq",
    "active_research_tab": "under_review",
    "boot_done": False,
    # UI overlays
    "palette_open": False,
    "terminal_open": False,
    "search_open": False,
    "palette_query": "",
    "terminal_history": [],
    "sidebar_collapsed": False,
    # Games
    "active_game": None,
    "game_scenario": None,
    "game_score": 0,
    "game_attempts": 0,
    "game_answered": False,
    "game_explained": False,
    "game_user_answer": None,
    # Groq cache (in-session, avoids repeat API calls for same content)
    "groq_cache": {},
    # Skills
    "active_skill": None,
    # Search
    "search_query": "",
    "search_results": [],
}


def init():
    """Call once at the top of main.py. Sets all keys that don't yet exist."""
    for key, value in DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = value


# ── Navigation ─────────────────────────────────────────────────────────────

def navigate(file: str):
    """Open a file in the editor and add it to open tabs."""
    st.session_state.active_file = file
    if file not in st.session_state.open_tabs:
        st.session_state.open_tabs.append(file)


def close_tab(file: str):
    """Close a tab. If it was active, open the previous one."""
    tabs = st.session_state.open_tabs
    if file in tabs:
        idx = tabs.index(file)
        tabs.remove(file)
        if st.session_state.active_file == file:
            if tabs:
                st.session_state.active_file = tabs[max(0, idx - 1)]
            else:
                navigate("about")
    st.session_state.open_tabs = tabs


def get_active() -> str:
    return st.session_state.active_file


def get_tabs() -> list:
    return st.session_state.open_tabs


# ── Games ───────────────────────────────────────────────────────────────────

def start_game(game_id: str):
    st.session_state.active_game = game_id
    st.session_state.game_scenario = None
    st.session_state.game_score = 0
    st.session_state.game_attempts = 0
    st.session_state.game_answered = False
    st.session_state.game_explained = False
    st.session_state.game_user_answer = None


def reset_game_round():
    st.session_state.game_scenario = None
    st.session_state.game_answered = False
    st.session_state.game_explained = False
    st.session_state.game_user_answer = None


def exit_game():
    st.session_state.active_game = None
    st.session_state.game_scenario = None


# ── Groq cache ──────────────────────────────────────────────────────────────

def groq_cache_get(key: str):
    return st.session_state.groq_cache.get(key)


def groq_cache_set(key: str, value: str):
    st.session_state.groq_cache[key] = value
