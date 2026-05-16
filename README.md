# RAG Core

A modular, lightweight Retrieval-Augmented Generation (RAG) framework written in Python. This engine leverages **Milvus** as a vector database for high-performance semantic search, **SQLite** for relational document metadata management, and **Ollama** for running open-source LLMs and embedding models locally.

## Features
- **Hybrid Storage:** Combines Milvus (vectors) and SQLite (text content & structural metadata).
- **Isolated Client State:** Thread-safe execution using explicit Ollama SDK Client routing.
- **Dockerized Infrastructure:** Zero-configuration orchestration for backend services.
- **Dynamic Schemas:** Fully utilizes Milvus dynamic field schemas for flexibility.

---

## Prerequisites
Ensure your local machine has the following tools installed:
- [Python 3.11 or higher](https://www.python.org/downloads/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)

---

## Installation & Setup from Zero

### 1. Clone the Repository
```bash
git clone [https://github.com/YOUR_USERNAME/rag-engine.git](https://github.com/YOUR_USERNAME/rag-engine.git)
cd rag-engine
