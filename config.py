"""Persona configuration for the AI Career Agent.

Everything person-specific lives here (or in environment variables), so the code
stays generic and the agent is trivially reusable / updatable.
"""
import os

# --- Persona ---------------------------------------------------------------
NAME = os.getenv("AGENT_NAME", "Shubham Singh")
TITLE = os.getenv("AGENT_TITLE", "Backend + AI Engineer")
TAGLINE = os.getenv(
    "AGENT_TAGLINE",
    "SDE II @ Reliance Jio — 4 yrs backend (Node, Kafka, K8s), now building AI/LLM systems.",
)

# --- Links (shown in the UI footer) ----------------------------------------
GITHUB_URL = os.getenv("AGENT_GITHUB", "https://github.com/ShubhamTheSingh")
LINKEDIN_URL = os.getenv("AGENT_LINKEDIN", "")  # fill when ready

# --- Model -----------------------------------------------------------------
MODEL = os.getenv("AGENT_MODEL", "gpt-4o-mini")  # cheap + capable default

# --- Knowledge base --------------------------------------------------------
SUMMARY_PATH = os.getenv("AGENT_SUMMARY_PATH", "me/summary.md")
LINKEDIN_PDF_PATH = os.getenv("AGENT_LINKEDIN_PDF", "me/linkedin.pdf")  # optional

# --- Lead capture ----------------------------------------------------------
# Optional free webhook (e.g. an ntfy.sh topic URL) to get pinged about leads /
# unanswered questions. Leave unset and everything is logged to local files.
NOTIFY_WEBHOOK_URL = os.getenv("NOTIFY_WEBHOOK_URL", "")
LEADS_FILE = os.getenv("LEADS_FILE", "leads.jsonl")
UNKNOWN_QUESTIONS_FILE = os.getenv("UNKNOWN_QUESTIONS_FILE", "unknown_questions.jsonl")
