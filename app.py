"""
Smart Toy — FastAPI Backend
Replaces Flask with FastAPI for async support and cleaner APIs.
"""

import time
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from services.intent import classify_intent
from services.actions import dispatch
from database import init_db, save_conversation, get_history
from logger import log_request

# ─── App Setup ───────────────────────────────────────────────────────────────

app = FastAPI(title="Smart Toy API", version="2.0")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Initialise DB on startup
@app.on_event("startup")
def on_startup():
    init_db()


# ─── Request / Response Models ───────────────────────────────────────────────

class ChatRequest(BaseModel):
    feature: str
    text: str | None = None


class ChatResponse(BaseModel):
    reply: str
    intent: str = "unknown"


# ─── Routes ──────────────────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/history")
async def history():
    """Return last 50 conversation turns from the database."""
    return {"history": get_history(50)}


@app.post("/api/chat", response_model=ChatResponse)
async def chat(payload: ChatRequest):
    """Main chat endpoint — classifies intent and dispatches to handler."""
    feature = payload.feature
    raw_text = payload.text or ""
    text = raw_text.lower().strip()

    intent = "unknown"
    reply = ""

    t0 = time.perf_counter()

    if feature == "talk":
        if not text:
            reply = "I am listening! Try saying hello, or ask me a question! 👂"
            intent = "prompt"
        else:
            intent = classify_intent(text)
            reply = dispatch(intent, text)

    elif feature == "quiz":
        if not text:
            reply = "Let's play a quiz! 🎉 What color is a banana?"
            intent = "quiz_start"
        else:
            low = text.lower()
            if "yellow" in low:
                reply = "Wow! Great job! 🎉 You are incredibly smart!"
            else:
                reply = "Nice try! But the correct answer is Yellow 🍌. Keep going! 🌟"
            intent = "quiz_answer"

    elif feature == "abc":
        reply = "Let's say the alphabet together! 🔤 A, B, C, D, E, F, G... H, I, J, K, L, M, N, O, P... Q, R, S, T, U, V... W, X, Y, and Z! 🎵 Now you know your ABCs!"
        intent = "abc"

    elif feature == "numbers":
        reply = "Let's count out loud! 🔢 1... 2... 3... 4... 5... 6... 7... 8... 9... 10! Wow! You are amazing at counting! ✋"
        intent = "numbers"

    else:
        reply = "Let's play! Pick a game below! 🎮"
        intent = "menu"

    latency_ms = (time.perf_counter() - t0) * 1000

    # Persist & log every turn
    save_conversation(raw_text, intent, reply)
    log_request(raw_text, intent, reply, latency_ms)

    return ChatResponse(reply=reply, intent=intent)
