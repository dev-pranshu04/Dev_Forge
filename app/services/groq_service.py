"""
GroqService — single point of entry for all Groq API calls.
Components never call Groq directly. This module handles:
- API key management
- In-session caching (explain buttons)
- No-cache for games (fresh scenario every round)
- Graceful fallback when API is unavailable
"""
import hashlib
import json
import streamlit as st

try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False

MODEL = "llama-3.3-70b-versatile"
MAX_TOKENS = 1024


def _get_client():
    if not GROQ_AVAILABLE:
        return None
    try:
        api_key = st.secrets.get("GROQ_API_KEY", "")
        if not api_key:
            return None
        return Groq(api_key=api_key)
    except Exception:
        return None


def _call(system: str, user: str, temperature: float = 0.7, max_tokens: int = MAX_TOKENS) -> str | None:
    client = _get_client()
    if not client:
        return None
    try:
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        return None


def _cache_key(prompt: str) -> str:
    return hashlib.md5(prompt.encode()).hexdigest()


def _cached_call(system: str, user: str) -> str:
    key = _cache_key(system + user)
    cached = st.session_state.get("groq_cache", {}).get(key)
    if cached:
        return cached
    result = _call(system, user)
    if result:
        if "groq_cache" not in st.session_state:
            st.session_state.groq_cache = {}
        st.session_state.groq_cache[key] = result
    return result


# ── Public API ──────────────────────────────────────────────────────────────

def explain_project(project: dict) -> str:
    system = (
        "You are a helpful assistant explaining Pranshu Kumar's portfolio projects "
        "to non-technical visitors. Be concise, clear, and avoid jargon. "
        "Explain in 3-4 sentences: what the project does, why it matters, and what's impressive about it."
    )
    user = f"Explain this project: {json.dumps(project, indent=2)}"
    result = _cached_call(system, user)
    return result or (
        f"{project.get('title', 'This project')} — {project.get('overview', 'details not available.')} "
        "For more details, check the GitHub link."
    )


def explain_research(research: dict) -> str:
    system = (
        "You are explaining academic research to a general audience. "
        "Avoid jargon. Use 3 sentences max. Explain: what question it answers, "
        "how it was studied, and why it matters in the real world."
    )
    title = research.get("meta", {}).get("title", "this research")
    body = research.get("body", "")[:800]
    user = f"Explain this research paper to a non-academic: Title: {title}\n\n{body}"
    result = _cached_call(system, user)
    return result or "This research investigates an important problem in the field. Explanation temporarily unavailable — please check back shortly."


def ai_recommend(active_file: str, project_ids: list) -> str:
    system = (
        "You are a helpful guide for Pranshu Kumar's portfolio workspace called Forge. "
        "Suggest the single best next thing to explore based on where the visitor currently is. "
        "Be specific and brief — one sentence."
    )
    user = f"Visitor is on: {active_file}. Available sections: projects ({', '.join(project_ids)}), research, skills, experience, playground. What should they explore next and why?"
    result = _cached_call(system, user)
    return result or "Explore the Projects section to see Pranshu's work in action."


# ── Game scenario generators (NO cache — fresh every round) ─────────────────

def generate_bug_scenario() -> dict | None:
    system = (
        "You generate coding challenge scenarios. Always respond with valid JSON only. "
        "No markdown, no explanation outside the JSON."
    )
    user = """Generate a Python code snippet (8-15 lines) with exactly ONE subtle bug.
The bug should be realistic — the kind a developer might actually write.
Vary: bug type (off-by-one, wrong operator, typo in variable name, 
missing return, incorrect comparison, wrong data structure method, 
scope error, mutation issue, type error).

Return ONLY this JSON (no markdown):
{
  "code": "def calculate_average(nums):\\n    total = 0\\n    for n in nums:\\n        total += n\\n    return total / len(nums)\\n\\nresult = calculate_average([])\\nprint(result)",
  "bug_line": 6,
  "bug_type": "ZeroDivisionError — no guard for empty list",
  "correct_fix": "return total / len(nums) if nums else 0",
  "explanation": "When nums is empty, len(nums) is 0, causing a ZeroDivisionError. Always guard division operations against zero denominators.",
  "difficulty": "medium"
}"""
    result = _call(system, user, temperature=1.0, max_tokens=600)
    if not result:
        return None
    try:
        clean = result.strip().lstrip("```json").lstrip("```").rstrip("```").strip()
        return json.loads(clean)
    except Exception:
        return None


def generate_git_scenario() -> dict | None:
    system = "You generate Git rescue challenge scenarios. Respond with valid JSON only."
    user = """Generate a Git repository crisis scenario.
Vary the crisis type: merge conflict, detached HEAD, accidentally deleted branch,
wrong commits on wrong branch, need to undo a push, stash emergency.

Return ONLY this JSON:
{
  "situation": "Brief description of what went wrong (2 sentences)",
  "repo_state": "What git status / git log would show right now",
  "goal": "What the developer needs to achieve",
  "solution_commands": ["git command 1", "git command 2"],
  "explanation": "Why these commands fix it",
  "difficulty": "medium"
}"""
    result = _call(system, user, temperature=1.0, max_tokens=500)
    if not result:
        return None
    try:
        clean = result.strip().lstrip("```json").lstrip("```").rstrip("```").strip()
        return json.loads(clean)
    except Exception:
        return None


def generate_terminal_scenario() -> dict | None:
    system = "You generate Linux terminal puzzle scenarios. Respond with valid JSON only."
    user = """Generate a Linux terminal puzzle.
Vary the type: find a file by content, fix permissions, chain pipes to extract data,
write a one-liner to process text, navigate and count files, use grep/awk/sed.

Return ONLY this JSON:
{
  "context": "You are in a Linux server. Brief scenario setup.",
  "task": "Specific thing to accomplish with one or two commands",
  "hint": "The key command or flag to use (vague)",
  "solution": "The exact command(s)",
  "explanation": "What each part of the command does",
  "difficulty": "medium"
}"""
    result = _call(system, user, temperature=1.0, max_tokens=500)
    if not result:
        return None
    try:
        clean = result.strip().lstrip("```json").lstrip("```").rstrip("```").strip()
        return json.loads(clean)
    except Exception:
        return None


def generate_ml_scenario() -> dict | None:
    system = "You generate ML concept challenge scenarios. Respond with valid JSON only."
    user = """Generate a Machine Learning scenario where the learner must choose the right approach.
Vary topics: model selection, overfitting diagnosis, feature engineering decision,
evaluation metric choice, handling class imbalance, train/val/test split strategy,
regularisation choice, data leakage identification.

Return ONLY this JSON:
{
  "scenario": "Describe a real-world ML problem with specific details (dataset, goal, observations)",
  "question": "What should the ML engineer do next?",
  "options": ["Option A", "Option B", "Option C", "Option D"],
  "correct": 1,
  "explanation": "Why this option is correct and why others are wrong. Teach the concept.",
  "concept": "Name of the ML concept this illustrates",
  "difficulty": "medium"
}"""
    result = _call(system, user, temperature=1.0, max_tokens=700)
    if not result:
        return None
    try:
        clean = result.strip().lstrip("```json").lstrip("```").rstrip("```").strip()
        return json.loads(clean)
    except Exception:
        return None


def generate_dl_scenario() -> dict | None:
    system = "You generate Deep Learning architecture challenge scenarios. Respond with valid JSON only."
    user = """Generate a Deep Learning architecture decision challenge.
Vary: CNN vs RNN choice, when to use attention, dropout placement,
activation function selection, batch normalisation timing,
transformer vs LSTM for sequence tasks, skip connections purpose.

Return ONLY this JSON:
{
  "problem": "A specific task description with input/output format",
  "proposed_architecture": "An architecture description with a flaw or suboptimal choice",
  "question": "What is wrong or what should be improved?",
  "options": ["Option A", "Option B", "Option C", "Option D"],
  "correct": 0,
  "explanation": "Deep explanation of the correct architectural choice and why it matters.",
  "concept": "DL concept illustrated",
  "difficulty": "hard"
}"""
    result = _call(system, user, temperature=1.0, max_tokens=700)
    if not result:
        return None
    try:
        clean = result.strip().lstrip("```json").lstrip("```").rstrip("```").strip()
        return json.loads(clean)
    except Exception:
        return None


def generate_nlp_scenario() -> dict | None:
    system = "You generate NLP/LLM concept challenge scenarios. Respond with valid JSON only."
    user = """Generate an NLP detective challenge using a fresh text passage.
Vary: identify the tokenisation issue, spot the prompt injection, 
find the retrieval failure, diagnose the hallucination, 
identify embedding space problem, detect context window issue,
spot the fine-tuning catastrophic forgetting sign.

IMPORTANT: Write a completely new, unique text passage every time.

Return ONLY this JSON:
{
  "passage": "A realistic text passage (could be a prompt, model output, retrieved chunk, or user message) that contains an NLP problem",
  "question": "What NLP problem does this passage demonstrate?",
  "options": ["Option A", "Option B", "Option C", "Option D"],
  "correct": 2,
  "highlighted_span": "The specific words or phrase that are the clue",
  "explanation": "Explain the NLP concept, why this is a problem, and how to fix it.",
  "concept": "NLP concept illustrated",
  "difficulty": "hard"
}"""
    result = _call(system, user, temperature=1.0, max_tokens=700)
    if not result:
        return None
    try:
        clean = result.strip().lstrip("```json").lstrip("```").rstrip("```").strip()
        return json.loads(clean)
    except Exception:
        return None


GAME_GENERATORS = {
    "bug_hunter": generate_bug_scenario,
    "git_rescue": generate_git_scenario,
    "terminal_quest": generate_terminal_scenario,
    "ml_academy": generate_ml_scenario,
    "dl_lab": generate_dl_scenario,
    "nlp_detective": generate_nlp_scenario,
}


def generate_scenario(game_id: str) -> dict | None:
    fn = GAME_GENERATORS.get(game_id)
    return fn() if fn else None
