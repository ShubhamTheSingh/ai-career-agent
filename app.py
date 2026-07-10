"""Chat with Shubham — a live AI agent that answers questions about my
background, experience, and projects. Built with OpenAI tool-calling + Gradio.

Run locally:   python app.py
Deploy:        Hugging Face Spaces (Gradio SDK) — set OPENAI_API_KEY as a secret.
"""
import os

import gradio as gr
from dotenv import load_dotenv

import config

load_dotenv(override=True)


def _build_ui():
    from agent import CareerAgent
    agent = CareerAgent()

    description = (
        f"👋 Hi, I'm **{config.NAME}** — {config.TAGLINE}\n\n"
        "Ask me anything about my experience, projects, or tech stack. "
        "This assistant answers on my behalf and can put you in touch."
    )
    links = f"[GitHub]({config.GITHUB_URL})"
    if config.LINKEDIN_URL:
        links += f" · [LinkedIn]({config.LINKEDIN_URL})"

    with gr.Blocks(theme=gr.themes.Soft(primary_hue="indigo"), title=f"Chat with {config.NAME}") as demo:
        gr.Markdown(f"# 💬 Chat with {config.NAME}")
        gr.Markdown(description)
        gr.ChatInterface(
            agent.chat,
            type="messages",
            examples=[
                "What's your backend experience?",
                "Have you worked with LLMs or AI?",
                "Tell me about a hard bug you fixed.",
                "What kind of roles are you looking for?",
            ],
        )
        gr.Markdown(f"---\n{links}")
    return demo


if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit(
            "OPENAI_API_KEY is not set. Add it to a .env file (local) or as a "
            "Space secret (Hugging Face)."
        )
    # 0.0.0.0 so it's reachable when running inside Docker / on Spaces.
    _build_ui().launch(server_name="0.0.0.0", server_port=int(os.getenv("PORT", "7860")))
