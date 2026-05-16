# RAG Core

A modular and lightweight **Retrieval-Augmented Generation (RAG)** framework written in Python.

This project integrates:

- **Milvus** for high-performance vector similarity search
- **SQLite** for relational metadata and document storage
- **Ollama** for running open-source LLMs and embedding models locally

Designed for simplicity, flexibility, and local-first AI development.

---

## Features

- 🚀 **Hybrid Storage Architecture**
  - Milvus for embeddings/vector search
  - SQLite for metadata and document management

- 🔒 **Thread-Safe Client Isolation**
  - Explicit Ollama SDK client routing for safe concurrent execution

- 🐳 **Dockerized Infrastructure**
  - Easy setup using Docker Compose

- 🧩 **Dynamic Milvus Schemas**
  - Flexible document structures using dynamic fields

- 🏠 **Fully Local AI Stack**
  - Run embeddings and generation models locally with Ollama

---

# Prerequisites

Make sure the following tools are installed on your machine:

- Python 3.11+
- Docker Desktop
- Git

## Recommended Downloads

- :contentReference[oaicite:0]{index=0}
- :contentReference[oaicite:1]{index=1}
- :contentReference[oaicite:2]{index=2}
- :contentReference[oaicite:3]{index=3}

---

# Installation & Setup

## 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/rag-engine.git
cd rag-engine
```

---

## 2. Configure Environment Variables

Copy the example environment file:

```bash
cp .env.example .env
```

Open `.env` and verify the configuration values.

### Example `.env`

```env
# =========================
# Milvus Configuration
# =========================
MILVUS_HOST=localhost
MILVUS_PORT=19530
MILVUS_COLLECTION_NAME=knowledge_base
MILVUS_EMBEDDING_DIMENSION=384

# =========================
# Ollama Configuration
# =========================
OLLAMA_API_URL=http://localhost:11434
OLLAMA_EMBED_MODEL=all-minilm:latest
OLLAMA_GEN_MODEL=phi3:mini

# =========================
# File Storage
# =========================
FILES_STORAGE_PATH=files
```

---

## 3. Start Infrastructure with Docker

Launch Milvus and its dependencies (`etcd` and `MinIO`):

```bash
docker compose up -d
```

Verify container status:

```bash
docker compose ps
```

---

## 4. Setup Ollama Models

Before running the application, pull the required Ollama models.

### Pull Embedding Model

```bash
ollama pull all-minilm:latest
```

### Pull Generation Model

```bash
ollama pull phi3:mini
```

Verify installed models:

```bash
ollama list
```

---

## 5. Setup Python Virtual Environment

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

#### Windows (PowerShell)

```powershell
.\venv\Scripts\Activate.ps1
```

#### macOS/Linux

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Usage Example

```python
import os
from dotenv import load_dotenv

from manager.database_manager import DatabaseManager
from engine.rag_engine import RAGEngine

# Load environment variables
load_dotenv()

# Initialize database manager
db_mgr = DatabaseManager(
    host=os.getenv("MILVUS_HOST"),
    port=os.getenv("MILVUS_PORT"),
    collection_name=os.getenv("MILVUS_COLLECTION_NAME"),
    dimension=int(os.getenv("MILVUS_EMBEDDING_DIMENSION"))
)

# Initialize RAG engine
rag = RAGEngine(
    db_manager=db_mgr,
    embed_model=os.getenv("OLLAMA_EMBED_MODEL"),
    gen_model=os.getenv("OLLAMA_GEN_MODEL"),
    ollama_url=os.getenv("OLLAMA_API_URL")
)

# Ingest knowledge
rag.ingest(
    text="Milvus standalone instances store cluster state and metadata within an isolated etcd cluster node.",
    source="architecture_docs.txt"
)

# Query knowledge
answer = rag.generate_answer(
    "Where does Milvus standalone save its metadata?"
)

print(f"Answer: {answer}")
```

---

# Project Structure

```text
rag-engine/
│
├── engine/
│   └── rag_engine.py
│
├── manager/
│   └── database_manager.py
│
├── files/
│
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

---

# Troubleshooting

## Reset Milvus Metadata State

If you change the embedding dimension (`MILVUS_EMBEDDING_DIMENSION`) after data has already been indexed, Milvus metadata may become inconsistent.

Reset the Docker volumes completely:

```bash
docker compose down -v
docker compose up -d
```

> ⚠️ Warning:
> The `-v` flag permanently removes all indexed vector data and metadata volumes.

---

# GitHub Setup

Initialize and push the repository to GitHub:

```bash
# Initialize repository
git init

# Stage files
git add .

# Commit changes
git commit -m "feat: initial commit"

# Rename branch
git branch -M main

# Add remote repository
git remote add origin https://github.com/YOUR_USERNAME/rag-engine.git

# Push to GitHub
git push -u origin main
```

---

# Recommended Improvements

Future enhancements you may consider:

- REST API integration with FastAPI
- PDF/DOCX ingestion pipeline
- Hybrid keyword + semantic search
- Multi-collection support
- Streaming response generation
- Chunking strategies
- Metadata filtering
- Authentication & RBAC

---

# License

MIT License

---

# Acknowledgements

Built with:

- :contentReference[oaicite:4]{index=4}
- :contentReference[oaicite:5]{index=5}
- :contentReference[oaicite:6]{index=6}
- :contentReference[oaicite:7]{index=7}
