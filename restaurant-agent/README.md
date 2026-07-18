# Restaurant Reservation Agent

An agentic AI assistant that handles restaurant operations end-to-end — answering menu and policy questions, checking real-time table availability, and completing reservations through natural conversation.

Unlike a typical retrieval-augmented chatbot that only answers questions from documents, this system takes real actions against live data: it checks availability and writes reservations, not just retrieves and summarizes.

---

## Overview

The assistant handles five categories of user intent through a single conversational interface:

- Menu browsing and pricing
- Table availability checks
- Reservation creation
- FAQs and restaurant policies (cancellation, refunds, etc.)
- Contact, address, and hours

It combines two distinct data strategies depending on what the question needs:

- **Semantic retrieval** (Pinecone) for anything fuzzy — menu descriptions, FAQs, policies
- **Structured queries** (SQL database) for anything exact and transactional — availability, bookings, prices

This split is deliberate: reservation accuracy requires exact, real-time database reads and writes, not vector similarity search. The agent routes each message to the right lane rather than treating everything as a document-retrieval problem.

---

## Agent workflow

```
                           START
                             │
                             ▼
                  Receive user message
                             │
                             ▼
                 Update conversation state
                             │
                             ▼
                   Intent classification
                             │
        ┌──────────────┬───────────────┬──────────────┐
        │              │               │              │
        ▼              ▼               ▼              ▼
     Menu         Reservation        FAQ          Contact
        │              │               │              │
        │              ▼               │              │
        │      Enough information?     │              │
        │              │               │              │
        │         ┌────┴────┐          │              │
        │        No        Yes         │              │
        │         │         │          │              │
        │         ▼         ▼          │              │
        │    Ask user   Call tool      │              │
        │                   │          │              │
        └───────────────────┼──────────┴──────────────┘
                             ▼
                    Receive tool output
                             │
                             ▼
                 Gemini generates response
                             │
                             ▼
                 Save conversation memory
                             │
                             ▼
                           END
```

Key design points:

- **Intent classification** routes each message to the right handler rather than treating every input the same way.
- **The "enough information?" check** is what makes the reservation path agentic rather than scripted — the agent recognizes missing slots (e.g. no time given) and asks a targeted follow-up instead of failing or guessing.
- **Conversation state persists across turns**, so information the user already gave (party size, preferred time) isn't re-requested later in the same conversation.
- **Tool output always passes through the LLM** before reaching the user, so responses stay conversational even when the underlying data came from a database or vector store.

---

## Architecture

```
Streamlit (chat UI)
      │
      ▼
FastAPI backend
      │
      ▼
LangGraph agent core (LangChain + Gemini + memory)
      │
      ├── Structured data tools ──► SQL database
      │   (menu, reservation, availability)
      │
      ├── Retrieval tools ─────────► Pinecone
      │   (FAQ, policy)
      │
      └── Contact tool ────────────► Config file
```

- **Streamlit** — chat interface
- **FastAPI** — REST backend, request/response layer
- **LangGraph** — orchestrates the workflow above: routing, state, conditional branching
- **LangChain** — connects the LLM to retrieval and prompt chains
- **Gemini** — reasoning and response generation
- **Pinecone** — vector store for FAQ and policy content
- **SQL database** — menu, table availability, and reservations

---

## Tech stack

- Python
- LangGraph
- LangChain
- Google Gemini (LLM + embeddings)
- Pinecone
- FastAPI
- Streamlit
- SQL (SQLite/Postgres)

---

## Key features

- Multi-step, stateful agent workflow (not single-turn Q&A)
- Intent-based routing across five task types
- Slot-filling before tool execution (asks for missing details instead of guessing)
- Dual data-lane design: semantic retrieval for unstructured content, structured queries for transactional data
- Persistent conversation memory within a session
- Modular tool layer, independently testable

---

## Why this project

This project was built to demonstrate practical agentic AI system design — not just prompting an LLM, but building a system that reasons about *what to do*, tracks state across a conversation, and acts on real data with real consequences. It reflects the kind of architecture used in production-style AI assistants: clear separation between orchestration, tools, and data, rather than a single monolithic prompt handling everything.

---

## Project structure

```
restaurant-agent/
├── app/
│   ├── main.py
│   ├── api/
│   ├── agent/
│   ├── tools/
│   ├── retrieval/
│   ├── db/
│   ├── core/
│   └── memory/
├── ui/
├── data/
├── scripts/
├── tests/
├── requirements.txt
└── README.md
```