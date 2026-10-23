# Smart Teaching Assistant — Team Skeleton

> [!TIP]
> **LIVE APP — OPEN IT HERE:** <https://smart-teaching-assistant.streamlit.app/>
>
> This is the deployed version. Open the link in a browser to see it without installing anything.

> Temporary team scaffold for building the Smart Teaching Assistant together.

This repository was intentionally reset to a **clean first commit**. The old prototype
feature code was removed, while the folder architecture, configuration and SQLite database
layer were preserved. The landing page now explains the starting point and is meant to be
replaced as features are added.

The full working prototype was archived locally in `copy-of-smart-teaching-assistant`
(including its git history) before the reset. It is **not** part of this repository.

---

> [!IMPORTANT]
> **START HERE — RUN THE PROJECT**
>
> **Windows 10/11 · Command Prompt (`cmd`)**
>
> **Step 1 — Open Command Prompt**
> Press `Win + R`, type `cmd`, then press Enter.
>
> **Step 2 — Install Python and Git (first time only, if missing)**
> ```bat
> winget install --id Python.Python.3.13 -e --accept-source-agreements --accept-package-agreements
> winget install --id Git.Git -e --accept-source-agreements --accept-package-agreements
> ```
> Close and reopen Command Prompt after this step.
>
> **Step 3 — Check the tools**
> ```bat
> python --version
> git --version
> ```
>
> **Step 4 — Clone the project**
> ```bat
> cd /d "%USERPROFILE%\Desktop"
> git clone https://github.com/Mohammad-jneid/smart-teaching-assistant.git
> cd smart-teaching-assistant
> ```
>
> **Step 5 — Create the virtual environment (first time only)**
> ```bat
> python -m venv .venv
> ```
>
> **Step 6 — Activate it**
> ```bat
> .venv\Scripts\activate.bat
> ```
> The prompt changes to `(.venv)`.
>
> **Step 7 — Install every library from the command line**
> ```bat
> python -m pip install --upgrade pip
> python -m pip install -r requirements.txt
> ```
>
> **Step 8 — Create the local settings file**
> ```bat
> copy /Y .env.example .env
> ```
>
> **Step 9 — Start the app**
> ```bat
> python -m streamlit run app.py
> ```
>
> **Step 10 — Open it**
> Open <http://localhost:8501>. Stop with `Ctrl + C`.
>
> **After the first time (no full reinstall needed)**
> ```bat
> cd /d "%USERPROFILE%\Desktop\smart-teaching-assistant"
> .venv\Scripts\activate.bat
> git pull
> python -m pip install -r requirements.txt
> python -m streamlit run app.py
> ```
> `pip install` is safe to run again: it only installs missing or changed packages.
>
> **Reinstall only if the environment is broken**
> ```bat
> rmdir /s /q .venv
> python -m venv .venv
> .venv\Scripts\activate.bat
> python -m pip install -r requirements.txt
> ```
>
> More detail: [START — How to run locally](#start--how-to-run-locally-on-windows-command-prompt)
>
> **END — RUN THE PROJECT**

---

## What is included

- **Architecture only** — `pages/`, `components/`, `core/` and `tests/` are ready to fill.
- **Database layer** — `database/db.py` with schema and helpers for students, attendance
  and unmatched faces.
- **Configuration** — `.env` / `st.secrets` support, paths and constants.
- **Temporary landing page** — `app.py` explains the project and shows live database counts.
- **Streamlit setup** — theme, upload limits, requirements and deployment notes.
- **No old features** — no recognition, attendance or CRUD pages were carried over.

The database is the one part that should stay stable. Everyone should use it through
`database/db.py` instead of writing SQL in pages.

---

## Project structure

```text
smart-teaching-assistant/
├── app.py                 # Temporary landing page (replace me)
├── requirements.txt
├── pytest.ini
├── .env                   # Local settings (gitignored)
├── .env.example
├── .gitignore
├── README.md
├── .streamlit/
│   └── config.toml
│
├── pages/                 # Team feature pages (empty for now)
│   └── __init__.py
│
├── components/            # Reusable UI components (empty for now)
│   └── __init__.py
│
├── core/                  # Business logic and helpers (empty for now)
│   └── __init__.py
│
├── database/
│   ├── __init__.py
│   └── db.py              # Preserved SQLite layer
│
├── config/
│   ├── __init__.py
│   ├── constants.py
│   └── settings.py
│
├── data/
│   ├── faces/             # Runtime uploads (gitignored)
│   └── teaching_assistant.db
│
└── tests/
    ├── unit/
    └── integration/
```

---

<!-- ==================== START: HOW TO RUN ==================== -->

## START — How to run locally on Windows (Command Prompt)

> This guide is **Windows-only** and uses **Command Prompt (`cmd`)**.
> Every command below is safe to copy-paste into `cmd`.

### Requirements

- Windows 10 or 11
- **Python 3.10 or newer** (tested with Python 3.13). Install it from the command line:
  ```bat
  winget install --id Python.Python.3.13 -e --accept-source-agreements --accept-package-agreements
  ```
- **Git** (needed to clone the repository). Install it from the command line:
  ```bat
  winget install --id Git.Git -e --accept-source-agreements --accept-package-agreements
  ```
- Close and reopen Command Prompt after installing Python or Git.
- Internet access for the first dependency install
- Any code editor (VS Code recommended, but optional)

If `winget` is not available, use an already installed Python 3.10+ and Git, or install
them with your normal Windows installer. The rest of the setup is still done from `cmd`.

### Step 1 — Open Command Prompt

Press `Win + R`, type `cmd`, then press Enter.

Alternatives:

- **Windows Terminal** → open a **Command Prompt** tab.
- **VS Code** → `Terminal` → `New Terminal`, then choose **Command Prompt** from the
  terminal dropdown.

Check Python:

```bat
python --version
```

You should see `Python 3.10` or newer. If `python` is not recognized, try:

```bat
py --version
```

If `py` works, use `py` instead of `python` in the commands below. If neither works,
reinstall Python and tick **Add python.exe to PATH**.

### Step 2 — Get the project

```bat
cd /d "%USERPROFILE%\Desktop"
git clone https://github.com/Mohammad-jneid/smart-teaching-assistant.git
cd smart-teaching-assistant
```

Without Git: open the GitHub page, click **Code → Download ZIP**, extract it, then:

```bat
cd /d "C:\path\to\smart-teaching-assistant"
```

### Step 3 — Create the virtual environment (first time only)

```bat
python -m venv .venv
```

No output is normal. Wait until the prompt returns, then verify:

```bat
dir .venv\Scripts
```

You must see `activate.bat`, `python.exe` and `pip.exe`.

If the folder is missing or incomplete:

```bat
rmdir /s /q .venv
python -m venv .venv
```

### Step 4 — Activate the virtual environment

```bat
.venv\Scripts\activate.bat
```

The prompt changes to `(.venv)`. You must activate it **every time** you open a new
Command Prompt.

### Step 5 — Install the libraries (first time only)

```bat
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

This installs Streamlit, NumPy, Pandas, Pillow, python-dotenv and pytest. Re-running the
command later is safe: pip only installs what is missing or changed.

### Step 6 — Create your local settings (first time only)

```bat
copy .env.example .env
```

The app also runs without `.env` because every value has a default. The file is gitignored,
so local secrets are never committed.

### Step 7 — Start the app

```bat
python -m streamlit run app.py
```

Open <http://localhost:8501>. On the first run the app creates
`data/teaching_assistant.db` automatically.

Stop the app with `Ctrl + C`.

If the port is already in use:

```bat
python -m streamlit run app.py --server.port 8502
```

Then open <http://localhost:8502>.

### Next time (short version)

You do not need to recreate the virtual environment. Open `cmd` and run:

```bat
cd /d "%USERPROFILE%\Desktop\smart-teaching-assistant"
.venv\Scripts\activate.bat
git pull
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

`git pull` gets the latest team code, and `pip install -r requirements.txt` makes sure any
new dependency is installed. It is safe to run every time: pip skips packages that are
already present and unchanged.

### When should I reinstall the requirements?

Run this only when:

- `requirements.txt` changed after a `git pull`, or
- a package is missing / imports fail, or
- the virtual environment is broken.

```bat
.venv\Scripts\activate.bat
python -m pip install -r requirements.txt
```

Do not delete `.venv` or reinstall everything every time. Full recreation is a last resort:

```bat
rmdir /s /q .venv
python -m venv .venv
.venv\Scripts\activate.bat
python -m pip install -r requirements.txt
```

### Running the archived copy

The full old prototype in `copy-of-smart-teaching-assistant` uses the exact same steps.
Use its own folder and its own `.venv`:

```bat
cd /d "C:\Users\<your-name>\Desktop\copy-of-smart-teaching-assistant"
python -m venv .venv
.venv\Scripts\activate.bat
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

### Which editor should I use?

**Recommended: Visual Studio Code (VS Code)** — free, works well with Python and Streamlit.

1. Install from <https://code.visualstudio.com/>
2. Install the **Python** extension from the Extensions panel.
3. `File → Open Folder` and select `smart-teaching-assistant`.
4. Open `Terminal → New Terminal` and choose **Command Prompt**.
5. Run the commands from this guide inside that terminal.

VS Code does **not** replace the command line — it simply gives you a terminal inside the
editor. The commands remain the same.

Alternatives:

- **Windows Terminal** — a modern tabbed terminal; use a Command Prompt tab.
- **PyCharm Community** — open the project folder and use its terminal.
- **Notepad++ / any editor** — edit files there, then run the commands in `cmd`.
- **No editor at all** — Command Prompt alone is enough to run the project.

### Troubleshooting (Windows / cmd)

| Problem | Fix |
| --- | --- |
| `'.venv\Scripts\activate.bat' is not recognized` | You are in the wrong folder, or `.venv` is incomplete. Run `cd /d "C:\path\to\smart-teaching-assistant"` then `dir .venv\Scripts`. If files are missing, `rmdir /s /q .venv` and recreate it. |
| `python` is not recognized | Reinstall Python and tick **Add python.exe to PATH**, or try `py` instead. |
| `pip` is not recognized | Use `python -m pip install -r requirements.txt` instead. |
| `streamlit` is not recognized | Use `python -m streamlit run app.py` instead. |
| `ModuleNotFoundError` | The venv is not active. Run `.venv\Scripts\activate.bat`, then install the requirements again. |
| Port 8501 already in use | `python -m streamlit run app.py --server.port 8502` |
| Upload rejected | Images must be JPG, PNG or WEBP and no larger than 10 MB. |
| PowerShell says execution is disabled | Do not use PowerShell; use `cmd` and `activate.bat` as shown above. |

<!-- ==================== END: HOW TO RUN ==================== -->

## END — How to run locally

---

## Database contract

`database/db.py` creates three tables:

| Table | Purpose |
| --- | --- |
| `students` | Student code, name, grade, phone, notes, face path and encoding |
| `attendance` | Check-ins linked to a student, with status, distance and time |
| `unregistered` | Unmatched faces waiting for review or promotion |

Useful functions:

| Area | Functions |
| --- | --- |
| Setup | `init_db`, `get_connection` |
| Students | `add_student`, `get_students`, `get_student`, `delete_student`, `student_code_exists` |
| Attendance | `add_attendance`, `get_attendance`, `has_attendance_today`, `clear_attendance` |
| Unmatched | `add_unregistered`, `get_unregistered`, `delete_unregistered`, `clear_unregistered`, `promote_unregistered` |
| Reporting | `get_stats`, `export_all_data` |

Example:

```python
from database.db import init_db, add_student, get_students

init_db()
add_student("STU-1001", "Sara Ahmad", grade="Grade 10")
print(get_students())
```

**Team rule:** keep every SQL query in `database/db.py`. Feature pages should call these
functions, never touch SQLite directly. This keeps schema changes in one reviewable place.

---

## How to add a feature

1. Pull the latest `main` and create a branch: `git checkout -b feature/student-registration`.
2. Add a page: `pages/1_Register_Student.py`.
3. Put reusable UI in `components/` and business logic in `core/`.
4. Use `database/db.py` for all persistence. Extend it there if a new query is needed.
5. Add tests under `tests/unit` or `tests/integration`.
6. Run `python -m pytest`, then open a pull request.

Streamlit automatically lists numbered files in `pages/` in the sidebar.

### Suggested first features

- Student registration and editing
- Attendance capture and matching
- Daily and class attendance reports
- Instructor authentication and roles
- Export to CSV / Excel / PDF

---

## Tests

From Command Prompt, with the virtual environment active:

```bat
.venv\Scripts\activate.bat
python -m pytest
```

The folders `tests/unit` and `tests/integration` are ready but intentionally empty. Add the
first test together with the first feature.

---

## Deploy to Streamlit Community Cloud

**Current live app:** <https://smart-teaching-assistant.streamlit.app/>

1. Push `main` to GitHub.
2. Open <https://share.streamlit.io> and choose **New app**.
3. Select `Mohammad-jneid/smart-teaching-assistant`, branch `main`, main file `app.py`.
4. Add configuration under **Advanced settings → Secrets**, for example:

   ```toml
   APP_NAME = "Smart Teaching Assistant"
   APP_VERSION = "0.1.0"
   ```

5. Deploy. Streamlit installs `requirements.txt` automatically.

**Storage warning:** the Streamlit Cloud filesystem is ephemeral. The SQLite database and
`data/faces/` uploads can disappear when the app rebuilds or wakes from sleep. For a real
deployment, move persistence to a managed database and object storage.

---

## Configuration

| Variable | Default | Purpose |
| --- | --- | --- |
| `APP_NAME` | `Smart Teaching Assistant` | Displayed in the UI |
| `APP_VERSION` | `0.1.0` | Version shown in the landing page |
| `APP_TAGLINE` | see `.env.example` | Reserved for branding |
| `DEMO_MODE` | `true` | Reserved for the future face engine |
| `ATTENDANCE_THRESHOLD` | `0.60` | Reserved for future matching logic |
| `DATA_DIR` | `data` | Local data directory |
| `DATABASE_PATH` | `data/teaching_assistant.db` | SQLite file |
| `FACES_DIR` | `data/faces` | Upload directory |

---

Built with [Streamlit](https://streamlit.io), Python and SQLite.
