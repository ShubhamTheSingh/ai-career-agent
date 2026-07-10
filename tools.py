"""Agent tools (function-calling) — free, no paid services.

Two tools:
  - record_user_details: capture an interested visitor's contact info.
  - record_unknown_question: log anything the agent couldn't answer.

Both append to local JSONL files and, if a webhook is configured, send a ping.
"""
import json
import datetime
import requests

import config


def _notify(text: str) -> None:
    """Best-effort ping to an optional webhook (e.g. ntfy.sh). Never raises."""
    if not config.NOTIFY_WEBHOOK_URL:
        return
    try:
        requests.post(config.NOTIFY_WEBHOOK_URL, data=text.encode("utf-8"), timeout=5)
    except Exception:
        pass  # notifications are best-effort; don't break the chat


def _append_jsonl(path: str, record: dict) -> None:
    record["timestamp"] = datetime.datetime.utcnow().isoformat() + "Z"
    try:
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    except Exception:
        pass  # ephemeral FS on some hosts; the webhook is the durable path


def record_user_details(email, name="Name not provided", notes="not provided"):
    """Record that a visitor wants to get in touch."""
    _append_jsonl(config.LEADS_FILE, {"name": name, "email": email, "notes": notes})
    _notify(f"📬 New lead: {name} <{email}> — {notes}")
    return {"recorded": "ok"}


def record_unknown_question(question):
    """Record a question the agent could not answer from the knowledge base."""
    _append_jsonl(config.UNKNOWN_QUESTIONS_FILE, {"question": question})
    _notify(f"❓ Unanswered question: {question}")
    return {"recorded": "ok"}


# --- OpenAI tool schemas ---------------------------------------------------
record_user_details_json = {
    "name": "record_user_details",
    "description": "Record that a visitor is interested in getting in touch and shared their email.",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {"type": "string", "description": "The visitor's email address"},
            "name": {"type": "string", "description": "The visitor's name, if given"},
            "notes": {"type": "string", "description": "Any useful context from the conversation"},
        },
        "required": ["email"],
        "additionalProperties": False,
    },
}

record_unknown_question_json = {
    "name": "record_unknown_question",
    "description": "Record any question that couldn't be answered from the knowledge base.",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {"type": "string", "description": "The question that couldn't be answered"},
        },
        "required": ["question"],
        "additionalProperties": False,
    },
}

TOOLS = [
    {"type": "function", "function": record_user_details_json},
    {"type": "function", "function": record_unknown_question_json},
]

# Registry so the agent can dispatch by name.
TOOL_FUNCTIONS = {
    "record_user_details": record_user_details,
    "record_unknown_question": record_unknown_question,
}
