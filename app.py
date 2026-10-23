"""Temporary team landing page for the Smart Teaching Assistant skeleton.

The previous prototype implementation was removed on purpose. This page explains
what is ready, what the team should build next, and how the preserved database
layer fits into the architecture.
"""

from __future__ import annotations

import streamlit as st

from config.settings import APP_NAME, APP_VERSION
from database.db import get_stats, init_db

APP_CSS = """
<style>
  [data-testid="stSidebar"], [data-testid="collapsedControl"] {display: none;}
  [data-testid="stHeader"] {background: transparent;}
  .block-container {max-width: 1180px; padding-top: 2.4rem; padding-bottom: 3rem;}

  .sta-hero {position: relative; overflow: hidden; border: 1px solid rgba(99, 102, 241, .35);
    border-radius: 28px; padding: clamp(2.2rem, 5vw, 4.2rem) 1.5rem; text-align: center;
    background:
      radial-gradient(circle at 18% 8%, rgba(99, 102, 241, .38), transparent 45%),
      radial-gradient(circle at 85% 88%, rgba(14, 165, 233, .24), transparent 42%),
      #0f172a;
    box-shadow: 0 30px 80px rgba(2, 6, 23, .55);}
  .sta-badge {display: inline-block; padding: .45rem .9rem; border-radius: 999px;
    border: 1px solid rgba(129, 140, 248, .4); background: rgba(99, 102, 241, .12);
    color: #c7d2fe; font-size: .78rem; letter-spacing: .03em; text-transform: uppercase;}
  .sta-hero h1 {font-size: clamp(2.3rem, 5.5vw, 4.2rem); line-height: 1.02;
    letter-spacing: -.045em; margin: .95rem 0 0; color: #f8fafc; font-weight: 800;}
  .sta-hero h1 span {background: linear-gradient(100deg, #818cf8, #22d3ee 58%, #a78bfa);
    -webkit-background-clip: text; background-clip: text; color: transparent;}
  .sta-sub {max-width: 760px; margin: 1.05rem auto 0; color: #cbd5e1;
    font-size: clamp(.95rem, 2vw, 1.06rem); line-height: 1.65;}
  .sta-tags {display: flex; flex-wrap: wrap; gap: .5rem; justify-content: center; margin-top: 1.4rem;}
  .sta-tag {padding: .38rem .78rem; border-radius: 999px; border: 1px solid #334155;
    background: rgba(15, 23, 42, .7); color: #cbd5e1; font-size: .76rem;}

  .sta-callout {margin: 1.1rem 0 0; padding: .95rem 1.1rem; border-radius: 14px;
    border: 1px solid rgba(245, 158, 11, .35); background: rgba(245, 158, 11, .08);
    color: #fcd34d; font-size: .88rem; line-height: 1.55;}
  .sta-callout strong {color: #fde68a;}

  .sta-section {margin: 2.6rem 0 .25rem; font-size: 1.35rem; font-weight: 700;
    letter-spacing: -.02em; color: #f1f5f9;}
  .sta-section-sub {margin: 0 0 1rem; color: #94a3b8; font-size: .9rem;}

  .sta-card {height: 100%; padding: 1.1rem 1.15rem; border-radius: 16px;
    background: linear-gradient(180deg, rgba(30, 41, 59, .92), rgba(15, 23, 42, .92));
    border: 1px solid #26334a; margin-bottom: .85rem;}
  .sta-card-icon {font-size: 1.4rem; line-height: 1;}
  .sta-card h3 {font-size: .98rem; margin: .55rem 0 .28rem; color: #f1f5f9;}
  .sta-card p {margin: 0; color: #94a3b8; font-size: .86rem; line-height: 1.5;}

  .sta-rule {display: flex; gap: .8rem; align-items: flex-start; padding: .7rem 0;
    border-bottom: 1px solid #1e293b; color: #cbd5e1; font-size: .9rem; line-height: 1.55;}
  .sta-rule:last-child {border-bottom: none;}
  .sta-rule-num {flex: 0 0 1.5rem; height: 1.5rem; border-radius: 50%; display: flex;
    align-items: center; justify-content: center; font-size: .72rem; font-weight: 700;
    background: rgba(99, 102, 241, .18); border: 1px solid rgba(99, 102, 241, .4);
    color: #c7d2fe;}

  div[data-testid="stMetric"] {background: rgba(30, 41, 59, .55); border: 1px solid #26334a;
    padding: .9rem 1rem; border-radius: 16px;}
  div[data-testid="stMetricLabel"] {color: #94a3b8;}

  .sta-footer {margin-top: 3rem; padding-top: 1.1rem; border-top: 1px solid #1e293b;
    text-align: center; color: #64748b; font-size: .78rem;}
</style>
"""

READY = [
    ("🗄️", "Database layer", "SQLite schema and CRUD helpers are preserved in database/db.py."),
    ("⚙️", "Configuration", "Settings from .env or st.secrets, data paths and constants are wired."),
    ("🧱", "Architecture", "pages/, components/, core/ and tests/ are ready for the team."),
    ("🏠", "Landing page", "This temporary page documents the starting point until features arrive."),
]

NEXT = [
    ("🧑‍🎓", "Student management", "Registration, editing, search and bulk import."),
    ("📸", "Attendance", "Capture or upload a photo, match a student, record the check-in."),
    ("📊", "Reports", "Daily registers, class summaries and CSV/Excel exports."),
    ("🔐", "Access control", "Instructor login and role-based access."),
]

TREE = """smart-teaching-assistant/
├── app.py                 ← temporary landing page (replace me)
├── database/
│   └── db.py              ← preserved SQLite layer
├── config/
│   ├── settings.py        ← env / st.secrets settings
│   └── constants.py
├── components/            ← reusable UI components
├── core/                  ← business logic and helpers
├── pages/                 ← numbered Streamlit feature pages
├── data/
│   └── faces/             ← runtime uploads (gitignored)
├── tests/
│   ├── unit/
│   └── integration/
├── requirements.txt
├── .env.example
└── README.md"""

DB_SNIPPET = """from database.db import init_db, add_student, get_stats

init_db()
add_student("STU-1001", "Sara Ahmad", grade="Grade 10")
print(get_stats())"""


def card(icon: str, title: str, text: str) -> str:
    return f"""
    <div class="sta-card">
      <div class="sta-card-icon">{icon}</div>
      <h3>{title}</h3>
      <p>{text}</p>
    </div>
    """


def render_cards(items: list[tuple[str, str, str]]) -> None:
    columns = st.columns(len(items), gap="medium")
    for column, (icon, title, text) in zip(columns, items):
        with column:
            st.markdown(card(icon, title, text), unsafe_allow_html=True)


def render_rules() -> None:
    rules = [
        "Keep every SQL query inside database/db.py. Pages call functions, never SQL.",
        "Give each feature its own page, for example pages/1_Register_Student.py.",
        "Put reusable UI in components/ and business logic in core/.",
        "Add tests under tests/unit or tests/integration before opening a pull request.",
    ]
    st.markdown(
        "".join(
            f'<div class="sta-rule"><div class="sta-rule-num">{number}</div>'
            f"<div>{rule}</div></div>"
            for number, rule in enumerate(rules, start=1)
        ),
        unsafe_allow_html=True,
    )


st.set_page_config(
    page_title=f"{APP_NAME} · Team scaffold",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)
st.markdown(APP_CSS, unsafe_allow_html=True)
init_db()
stats = get_stats()

st.markdown(
    f"""
    <div class="sta-hero">
      <div class="sta-badge">Temporary team scaffold · v{APP_VERSION}</div>
      <h1>Smart Teaching<br><span>Assistant</span></h1>
      <p class="sta-sub">
        A clean starting point for the team. The old prototype code was removed, the folder
        architecture stays, and the database layer plus configuration are ready for new work.
      </p>
      <div class="sta-tags">
        <span class="sta-tag">Database preserved</span>
        <span class="sta-tag">Landing page only</span>
        <span class="sta-tag">History reset</span>
      </div>
    </div>
    <div class="sta-callout">
      <strong>Temporary landing page.</strong> Replace this page as the first real feature
      lands. The project currently contains no attendance or recognition logic — only the
      architecture, configuration and SQLite layer.
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")
first, second, third, fourth = st.columns(4)
first.metric("Students", stats["students"])
second.metric("Check-ins", stats["attendance_total"])
third.metric("Unmatched faces", stats["unregistered"])
fourth.metric("Database tables", 3)

st.markdown('<div class="sta-section">What is already in place</div>', unsafe_allow_html=True)
st.markdown('<p class="sta-section-sub">The foundation the team should build on.</p>', unsafe_allow_html=True)
render_cards(READY)

st.markdown('<div class="sta-section">What the team builds next</div>', unsafe_allow_html=True)
st.markdown('<p class="sta-section-sub">Suggested first features. Replace these with your own roadmap.</p>', unsafe_allow_html=True)
render_cards(NEXT)

st.markdown('<div class="sta-section">Architecture and database contract</div>', unsafe_allow_html=True)
left, right = st.columns([1.15, 1], gap="large")

with left:
    st.caption("Folder structure")
    st.code(TREE, language="text")

with right:
    st.caption("Use the database layer, not raw SQL")
    st.markdown(
        "`database/db.py` already creates the tables and exposes helpers for students, "
        "attendance and unmatched faces."
    )
    st.code(DB_SNIPPET, language="python")
    st.caption("Tables: students · attendance · unregistered")

st.markdown('<div class="sta-section">How we work</div>', unsafe_allow_html=True)
st.markdown('<p class="sta-section-sub">Four rules that keep the project easy to merge.</p>', unsafe_allow_html=True)
render_rules()

with st.expander("Where is the previous prototype?"):
    st.markdown(
        "The previous working prototype was archived in the separate local folder "
        "`copy-of-smart-teaching-assistant` before this repository was reset. It keeps the "
        "old implementation and git history for reference, but it is not part of this "
        "repository. This repo is the clean team workspace."
    )

st.markdown(
    f'<div class="sta-footer">{APP_NAME} · v{APP_VERSION} · Team skeleton · Database preserved</div>',
    unsafe_allow_html=True,
)
