# Offline AI Research Assistant 🕵️‍♂️

A privacy-first, 100% offline, multi-agent AI research orchestration system built with **LangGraph**, **Ollama**, and **Streamlit**.

## Overview
This application provides a completely local Retrieval-Augmented Generation (RAG) pipeline designed for deep research. By utilizing open-weight LLMs (`llama3.2`) running locally on your hardware, your data and queries never leave your machine.

You simply drop PDF documents into the `data/` directory, and a team of specialized AI agents will autonomously read, synthesize, and review the information to generate a comprehensive markdown report.

### The Agent Workflow:
1. **🔍 Research Agent:** Ingests local PDFs via a ChromaDB vector database and extracts highly relevant snippets based on your topic.
2. **✍️ Writer Agent:** Takes the raw structured data and drafts a polished markdown report.
3. **🧐 Critic Agent:** Reviews the draft against strict quality constraints (Accuracy, Completeness, Clarity). If the draft fails, it sends actionable feedback back to the Writer Agent for a mandatory revision.

### Tech Stack
* **UI:** Streamlit (with dynamic Glassmorphism telemetry dashboard)
* **Orchestration:** LangGraph & LangChain
* **Local LLM Engine:** Ollama (`llama3.2`)
* **Vector Database:** ChromaDB
* **Embeddings:** `nomic-embed-text`