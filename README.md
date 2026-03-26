# 🤖 Smart Toy — AI-Based Interactive Educational Toy

A kid-friendly AI web app that answers questions, tells jokes, teaches ABCs, and runs quizzes — powered by FastAPI, Web Speech API, and live internet APIs.

---

## Architecture

```
smart toy/
├── app.py                  ← FastAPI server (entry point)
├── database.py             ← SQLite conversation storage
├── logger.py               ← Structured JSON logging
├── requirements.txt        ← Python dependencies
│
├── services/
│   ├── intent.py           ← Intent classifier (keyword routing)
│   └── actions.py          ← Action handlers + dispatcher
│
├── templates/
│   └── index.html          ← HTML page (kid-friendly UI)
│
├── static/
│   ├── style.css           ← CSS — gradients, animations
│   └── script.js           ← Frontend: speech, fetch, history
│
├── smart_toy.db            ← SQLite DB (auto-created)
└── logs/
    └── smart_toy.log       ← JSON logs (auto-created)
```

### Data Flow
```
Child speaks/types
    → Web Speech API (Chrome)
    → script.js → POST /api/chat
    → FastAPI (app.py)
    → Intent Classifier (services/intent.py)
    → Action Handler (services/actions.py)
        → Joke API / Facts API / Wikipedia / built-in
    → Save to SQLite (database.py)
    → Log to JSON (logger.py)
    → JSON response → browser → display + speak
```

---

## Features

| Button | What it does |
|---|---|
| 🎤 Talk to Me | Listens via microphone, answers any question |
| ❓ Quiz Me! | Asks a question, evaluates your answer |
| 🔤 Learn ABCs | Recites the full alphabet |
| 🔢 Count! | Counts 1–10 |
| 💬 Type input | Type any question if mic isn't available |

**Intents recognised:** joke, fun fact, Wikipedia lookup, math, greeting, animals, space/planets, colors, alphabet, numbers

---

## Installation & Run

```powershell
# 1. Install dependencies
pip install fastapi "uvicorn[standard]" python-multipart pydantic requests wikipedia

# 2. Start the server
python -m uvicorn app:app --reload --port 5000

# 3. Open in Chrome
# http://localhost:5000
```

---

## API Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/` | Serves the web UI |
| POST | `/api/chat` | `{ feature, text }` → `{ reply, intent }` |
| GET | `/api/history` | Last 50 conversation turns |

---

## Libraries Used

| Library | Purpose |
|---|---|
| `fastapi` | Async web framework (replaces Flask) |
| `uvicorn` | ASGI server |
| `pydantic` | Request/response validation |
| `requests` | Calls external joke/fact APIs |
| `wikipedia` | Wikipedia summaries |
| Web Speech API | Browser-native voice (no install needed) |
