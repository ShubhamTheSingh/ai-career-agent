# Concepts — how this AI agent actually works

Study notes for explaining this project in an interview. Every claim maps to code in
this repo.

## The mental model
An "AI agent" here is just **5 ingredients**:
1. **An LLM** (`gpt-4o-mini`) — generates text.
2. **Instructions** (the *system prompt*) — who to be + the rules.
3. **Knowledge** (`me/summary.md`) — facts injected so it answers about *me*, not the world.
4. **Tools** (functions it can call) — lets it *do things*, not just talk.
5. **A loop** — keeps calling the LLM (running any tools it asks for) until it's done.

Wrap it in a UI (Gradio) and deploy → an agent.

## 1. Messages & roles
Every chat call sends a list of messages, each with a `role`:
- `system` — the instructions (sent once, first).
- `user` — what the visitor typed.
- `assistant` — the model's past replies (the "history").
- `tool` — the result of a tool the model asked us to run.

The LLM is **stateless** — it remembers nothing between calls. We resend the whole
conversation every time (see how `agent.py` builds `messages = [system] + history + [user]`).
> Interview line: *"A chatbot doesn't 'remember' — you replay the message history on every call."*

## 2. Grounding (why it doesn't make things up about me)
The model has no idea who I am, so we **inject `me/summary.md` into the system prompt**.
Now it answers from my facts. This is the seed of RAG — RAG just fetches relevant docs
*dynamically* instead of stuffing one fixed file.

## 3. Function / tool calling (the key concept)
1. We describe our tools to the model as **JSON schemas** (`tools.py`) — name, description, params.
2. The model **can't run code**. When it wants a tool, it returns a message: *"call
   `record_user_details` with these arguments."*
3. **Our code** executes the real function, then sends the **result back** as a `tool` message.
4. The model uses that result to write its final answer.
> The LLM *decides*; your code *executes*. That's the whole trick.

## 4. The agentic loop (why the `while` loop exists)
```
while True:
    response = llm.create(messages, tools)
    if finish_reason == "tool_calls":   # model wants a tool
        run tool(s), append results, loop again
    else:
        return final answer             # model is done
```
The model might need several rounds (call a tool → see result → maybe call another →
then answer). The loop runs until the model stops asking for tools. **That loop is what
makes it "agentic"** — the model drives its own multi-step process. CrewAI, LangGraph,
etc. are more sophisticated versions of this same handoff.

## Backend analogy (for a backend engineer)
| Backend | This project |
|---|---|
| `app.js` (entry/server) | `app.py` (Gradio server) |
| Controller | `agent.py` (`CareerAgent`) |
| Service layer | `tools.py` |
| Config | `config.py` |
| DB seed / content | `me/summary.md` |

**The one twist:** in a normal backend *you* route requests to handlers. Here the **LLM
decides** which tool to call. Control flow is driven by the model; your code provides the
capabilities.

## Likely interview questions
- *How does the chatbot keep context?* → Resend full message history each call; the model is stateless.
- *How does tool calling work?* → Model returns a structured tool request; your code runs it and returns the result; model continues.
- *How do you stop hallucination?* → Ground answers in a provided context and instruct the model to defer when it doesn't know (and here, log the unknown question).
- *What makes it "agentic"?* → The loop where the model autonomously decides to call tools across multiple steps before answering.
