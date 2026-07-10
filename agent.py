"""CareerAgent — an LLM that answers questions as a specific person, using a
knowledge base (markdown summary + optional LinkedIn PDF) and function-calling
tools for lead capture.
"""
import json
import os

from openai import OpenAI

import config
from tools import TOOLS, TOOL_FUNCTIONS


def _load_knowledge_base() -> str:
    """Load the markdown summary and (optionally) a LinkedIn PDF."""
    parts = []

    if os.path.exists(config.SUMMARY_PATH):
        with open(config.SUMMARY_PATH, "r", encoding="utf-8") as f:
            parts.append("## Summary\n" + f.read())

    if os.path.exists(config.LINKEDIN_PDF_PATH):
        try:
            from pypdf import PdfReader
            reader = PdfReader(config.LINKEDIN_PDF_PATH)
            text = "\n".join(page.extract_text() or "" for page in reader.pages)
            if text.strip():
                parts.append("## LinkedIn Profile\n" + text)
        except Exception:
            pass  # PDF is optional; carry on with the summary

    if not parts:
        raise FileNotFoundError(
            f"No knowledge base found. Add your story to '{config.SUMMARY_PATH}'."
        )
    return "\n\n".join(parts)


class CareerAgent:
    def __init__(self):
        self.client = OpenAI()
        self.knowledge = _load_knowledge_base()

    def system_prompt(self) -> str:
        return f"""You are acting as {config.NAME} ({config.TITLE}), answering questions on \
{config.NAME}'s portfolio website — from recruiters, hiring managers, and fellow engineers. \
Speak in the first person, as {config.NAME}. Be professional, warm, and concise (a few tight \
sentences, not walls of text).

Ground rules:
- Answer ONLY from the knowledge base below. Never invent facts, numbers, employers, or dates.
- If you don't know something, say so briefly and call `record_unknown_question` to log it.
- If the visitor seems interested or wants to connect, encourage them to share their email and \
call `record_user_details` to record it.
- Represent {config.NAME} faithfully and put his best (truthful) foot forward.

Knowledge base:
{self.knowledge}

Stay in character as {config.NAME} at all times."""

    def _dispatch_tools(self, tool_calls):
        results = []
        for call in tool_calls:
            fn = TOOL_FUNCTIONS.get(call.function.name)
            args = json.loads(call.function.arguments or "{}")
            output = fn(**args) if fn else {"error": "unknown tool"}
            results.append({
                "role": "tool",
                "tool_call_id": call.id,
                "content": json.dumps(output),
            })
        return results

    def chat(self, message, history):
        messages = (
            [{"role": "system", "content": self.system_prompt()}]
            + history
            + [{"role": "user", "content": message}]
        )
        while True:
            response = self.client.chat.completions.create(
                model=config.MODEL, messages=messages, tools=TOOLS
            )
            choice = response.choices[0]
            if choice.finish_reason == "tool_calls":
                messages.append(choice.message)
                messages.extend(self._dispatch_tools(choice.message.tool_calls))
                continue
            return choice.message.content
