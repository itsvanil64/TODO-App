# Tasky — A Clean Python To-Do App

A lightweight, modern to-do list application built with **Flask** (Python) and plain HTML/CSS/JS. No database, no auth, no frameworks — just clean, beginner-friendly code.

---

## Project Structure

```
todo-app/
├── app/
│   ├── app.py                   # Flask backend
│   ├── templates/
│   │   └── index.html           # Main UI template
│   └── static/
│       └── css/
│           ├── style.css        # Styling
│           └── app.js           # Frontend logic
├── .github/
│   └── workflows/
│       └── ci.yml               # GitHub Actions CI
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## Features

- ✅ Add tasks (press Enter or click Add)
- ✅ Mark tasks complete / incomplete
- ✅ Delete tasks with a smooth animation
- ✅ Live task count and done count
- ✅ In-memory storage (resets on restart)
- ✅ Modern, clean UI with subtle animations

---

## Run Locally (Python)

### Prerequisites
- Python 3.10+

### Steps

```bash
# 1. Clone the repo
git clone <your-repo-url>
cd todo-app

# 2. Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start the app
python app/app.py
```

Open **http://localhost:5000** in your browser.

---

## Run with Docker

### Prerequisites
- Docker installed

### Option A — Docker only

```bash
# Build the image
docker build -t tasky-app .

# Run the container
docker run -p 5000:5000 tasky-app
```

### Option B — Docker Compose (recommended)

```bash
docker-compose up --build
```

Open **http://localhost:5000** in your browser.

To stop:
```bash
docker-compose down
```

---

## GitHub Actions CI

The pipeline at `.github/workflows/ci.yml` runs on every push / PR to `main`:

| Job     | What it does                                              |
|---------|-----------------------------------------------------------|
| `test`  | Installs deps, starts Flask, smoke-tests `/` and the API |
| `docker`| Builds the Docker image, runs it, hits the health check  |

No secrets or environment variables are required.

---

## API Reference

| Method | Endpoint             | Body                    | Description          |
|--------|----------------------|-------------------------|----------------------|
| GET    | `/api/tasks`         | —                       | List all tasks       |
| POST   | `/api/tasks`         | `{"title": "..."}` | Create a task        |
| PATCH  | `/api/tasks/<id>`    | —                       | Toggle complete      |
| DELETE | `/api/tasks/<id>`    | —                       | Delete a task        |

---

## Tech Stack

| Layer     | Technology                    |
|-----------|-------------------------------|
| Backend   | Python 3.12 + Flask 3         |
| Frontend  | HTML5, CSS3, Vanilla JS       |
| Fonts     | Google Fonts (Playfair + DM Sans) |
| Container | Docker + Docker Compose       |
| CI/CD     | GitHub Actions                |

---

## Notes

- Tasks are stored in memory — they reset when the server restarts. Swap the `tasks` dict for SQLite or Redis for persistence.
- No authentication is included by design (beginner-friendly scope).
