"""
Structured JSON Logging
Writes one JSON object per line to logs/smart_toy.log
"""

import logging
import json
import os
from datetime import datetime

LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "smart_toy.log")


class _JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "message": record.getMessage(),
        }
        if hasattr(record, "extra"):
            payload.update(record.extra)
        return json.dumps(payload)


def _build_logger() -> logging.Logger:
    logger = logging.getLogger("smart_toy")
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        fh = logging.FileHandler(LOG_FILE, encoding="utf-8")
        fh.setFormatter(_JsonFormatter())
        logger.addHandler(fh)

        sh = logging.StreamHandler()
        sh.setFormatter(_JsonFormatter())
        logger.addHandler(sh)
    return logger


logger = _build_logger()


def log_request(query: str, intent: str, response: str, latency_ms: float) -> None:
    """Log a single chat request/response pair."""
    record = logger.makeRecord(
        "smart_toy", logging.INFO, "", 0,
        "chat_request", (), None,
    )
    record.extra = {
        "query": query,
        "intent": intent,
        "response_length": len(response),
        "latency_ms": round(latency_ms, 2),
    }
    logger.handle(record)
