# Agentic RAG Assistant (LangGraph + Pinecone + Gemini)

This project is a full Agentic AI system built using LangGraph, Retrieval-Augmented Generation (RAG), and LLM-based reasoning. It supports intelligent routing between simple and complex queries using a graph-based workflow.

Developed by **Muhammad Atif**

---

# Project Overview

This system simulates a real-world Agentic AI pipeline that:

- Accepts user questions
- Classifies query complexity (Simple vs Complex)
- Routes execution dynamically using LangGraph
- Retrieves relevant context from Pinecone vector database
- Uses a Planner Agent for complex reasoning
- Uses a Verification Agent to validate intermediate outputs
- Uses LLM to generate final responses
- Produces structured, context-aware, and accurate answers

---

# gentic Workflow (CORE LOGIC)

```text
START
  ↓
Question Classifier
  ↓
+----------------------+
|                      |
v                      v
Simple Path        Complex Path
|                      |
v                      v
Retriever        Planner Agent
|                      |
+----------+-----------+
           |
           v
   Verification Agent
           |
           v
   Answer Generator
           |
           v
          END
```

---

# System Architecture Pipeline

## 1. Data Pipeline (Ingestion Flow)

Website / PDF / DOCX / TXT  
↓  
Load Document  
↓  
Clean Text  
↓  
Split into Chunks  
↓  
Generate Embeddings (Gemini)  
↓  
Store in Pinecone Vector DB  

---

## 2. Query Execution Flow (Runtime)

User Question  
↓  
Question Classifier  
↓  
IF Simple → Retriever → Verification Agent → Answer Generator  
IF Complex → Planner Agent → Verification Agent → Answer Generator  
↓  
Final Response Returned to User  


---

# Key Features

- Agentic AI workflow using LangGraph
- Query classification (Simple vs Complex)
- Planner + Retriever + Verification + Generator pipeline
- Retrieval-Augmented Generation (RAG)
- Pinecone vector database integration
- Gemini embeddings + LLM responses
- Modular production-ready architecture
- FastAPI backend support
- Streamlit frontend support

---

# Tech Stack

- Python
- LangGraph
- LangChain
- Google Gemini (LLM + Embeddings)
- Pinecone Vector Database
- FastAPI
- Streamlit

---

# Purpose of This Project

This project demonstrates:

- Real-world Agentic AI system design
- Advanced RAG architecture
- Multi-step reasoning pipelines
- Production-level AI engineering practices
- Scalable LLM application architecture
- End-to-end AI system development

---

# Author

**Muhammad Atif**

AI/ML Engineer focused on:

- Agentic AI Systems
- Retrieval-Augmented Generation (RAG)
- LangGraph Workflows
- LLM Application Development
- AI Engineering & Data Systems