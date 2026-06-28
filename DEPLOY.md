# Forge — Deployment Guide

## Local development

```bash
pip install -r requirements.txt
streamlit run main.py
```

## Add Groq API key (required for games + AI features)

Create `.streamlit/secrets.toml`:

```toml
GROQ_API_KEY = "gsk_your_key_here"
```

Get a free key at: https://console.groq.com

## Deploy to Streamlit Community Cloud (free)

1. Push this folder to a GitHub repository
2. Go to share.streamlit.io
3. Connect your GitHub repo
4. Set main file: `main.py`
5. Add secret: GROQ_API_KEY = your key
6. Deploy → your portfolio is live at `yourname.streamlit.app`

## Update your content (no code changes needed)

| What to update | File to edit |
|---|---|
| Bio / philosophy | `content/about.md` |
| Your name, email, links | `content/config.json` |
| Add/edit a job | `content/experience.json` |
| Add/edit a project | `content/projects/yourproject.json` |
| Update research | `content/research/published.md` etc |
| Add a skill | `content/skills.json` → add to categories array |
| Education | `content/education.json` |
| Achievements | `content/achievements.json` |
| Replace resume | Drop PDF at `assets/resume.pdf` |
| Add profile photo | Drop image at `assets/images/avatar.jpg` |

## Add a new project

1. Copy `content/projects/cardiorisk.json`
2. Rename to `content/projects/yourproject.json`
3. Edit the fields
4. Push to GitHub
5. Done — it auto-appears in Explorer and Projects page

## Photo update

When ready, replace `assets/images/avatar.jpg` with your photo.
The `profile-avatar` component checks for this file automatically.
If missing → shows "PK" initials. No code change needed.
