# About Shubham Singh

> This is the knowledge base my AI agent uses to answer questions about me.
> Editable, single source of truth — update this file as I grow and the agent stays current.

## Who I am
I'm **Shubham Singh**, a backend engineer with ~4 years of experience, currently a
**Software Development Engineer II at Reliance Jio** (since June 2022). I'm now expanding
into **AI / LLM engineering**, building production-style GenAI systems on top of strong
backend fundamentals. My focus: **Backend + AI** — engineers who can both *build the AI*
and *ship it as real, scalable software*.

## Current role — SDE II, Reliance Jio (Jun 2022 – present)
I work on the **backend of PeopleFirst**, Reliance's internal HR platform used across the
group. It digitizes the entire **employee lifecycle** — from onboarding, through everyday
work-life (attendance, leave, payroll-related flows), all the way to resignation — so the
experience is smooth and automated at enterprise scale.

I sit on a team of ~50 that owns the platform's backend. Day to day I mix **hands-on coding,
system design, and some technical leadership**, with a focus on systems that are
**scalable, secure, and fast**.

### Things I'm proud of solving (real engineering, not tutorials)
- **Cross-user financial data corruption:** a claim-check **key collision under concurrent
  load** was letting one user's data bleed into another's. I root-caused it and fixed it with
  **UUID-based keying**, eliminating the collision.
- **Silent data loss in a cron job:** a **non-sargable JOIN** plus unstable **LIMIT/OFFSET
  pagination** was silently dropping rows on each run. I redesigned the pagination and used an
  **in-memory Set** to guarantee complete, correct processing.

*(Detailed scale/impact metrics available on request and in my resume.)*

## Technical skills
- **Backend:** Node.js, Express, JavaScript
- **Data:** MySQL, MongoDB, Redis, Kafka
- **Infra / DevOps:** Docker, Kubernetes
- **Foundations:** Data Structures & Algorithms, System Design
- **AI / LLM (actively building):** Python, OpenAI API, prompt engineering, tool/function
  calling, RAG, autonomous agents

## AI / LLM projects (this portfolio — growing weekly)
- **This AI Career Agent** — the assistant you're chatting with: OpenAI + tool-calling +
  Gradio, deployed live.
- *More landing soon:* a Retrieval-Augmented Generation (RAG) knowledge assistant, and
  multi-agent systems. *(Links added as each ships.)*

## What I'm looking for
**Backend + AI Engineer roles** where I can combine solid backend engineering with modern
LLM/agentic systems. Open to strong teams building real AI products.

## Contact
- GitHub: https://github.com/ShubhamTheSingh
- Prefer to connect? Share your email in the chat and I'll get back to you.
