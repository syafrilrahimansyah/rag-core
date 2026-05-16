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

2. Configure Environment Variables
Copy the template configuration file to create your local environment:

Bash
cp .env.example .env
Open .env and verify the values match your architecture parameters. Standard defaults:

Ini, TOML
# Milvus Configuration
MILVUS_HOST=localhost
MILVUS_PORT=19530
MILVUS_COLLECTION_NAME=knowledge_base
MILVUS_EMBEDDING_DIMENSION=384

# Ollama Configuration
OLLAMA_API_URL=http://localhost:11434
OLLAMA_EMBED_MODEL=all-minilm:latest
OLLAMA_GEN_MODEL=phi3:mini

# File Storage Configuration
FILES_STORAGE_PATH=files

3. Spin Up Infrastructure (Docker)
Launch Milvus Standalone alongside its dependencies (etcd and MinIO) by running:

Bash
docker compose up -d
Verify the health status of your containers inside your Docker dashboard or via terminal:

Bash
docker compose ps

4. Setup Ollama
If running Ollama via Docker or local runtime, you must pre-download the models designated in your .env configuration file before running the application logic:

Bash
# Pull the Embedding model (384 dimensions)
ollama pull all-minilm:latest

# Pull the Generation text model
ollama pull phi3:mini

5. Setup Python Virtual Environment
Initialize your environment wrapper and resolve project dependencies:

Bash
# Create environment
python -m venv venv

# Activate on Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# Activate on macOS/Linux
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
Usage Summary
Python
import os
from dotenv import load_dotenv
from manager.database_manager import DatabaseManager
from engine.rag_engine import RAGEngine

load_dotenv()

# Initialize Database Architecture
db_mgr = DatabaseManager(
    host=os.getenv("MILVUS_HOST"),
    port=os.getenv("MILVUS_PORT"),
    collection_name=os.getenv("MILVUS_COLLECTION_NAME"),
    dimension=int(os.getenv("MILVUS_EMBEDDING_DIMENSION"))
)

# Initialize RAG Engine Core
rag = RAGEngine(
    db_manager=db_mgr,
    embed_model=os.getenv("OLLAMA_EMBED_MODEL"),
    gen_model=os.getenv("OLLAMA_GEN_MODEL"),
    ollama_url=os.getenv("OLLAMA_API_URL")
)

# 1. Ingest context data
rag.ingest(
    text="Milvus standalone instances store cluster state and metadata within an isolated etcd cluster node.",
    source="architecture_docs.txt"
)

# 2. Ask questions against context
answer = rag.generate_answer("Where does Milvus standalone save its metadata?")
print(f"Answer: {answer}")
Troubleshooting Metadata Corruptions
If modifications are made directly to embedding structural dimensions (MILVUS_EMBEDDING_DIMENSION), Milvus internal etcd logs may conflict with fresh initialization. To reset tracking state completely:

Bash
docker compose down -v
docker compose up -d
(Warning: The -v flag flushes all underlying volumes, wiping previously indexed data).


---

### How to Push This to GitHub

Initialize your Git tree, staging updates, and routing directly to your newly created repository origin endpoint inside your terminal workspace:

```bash
# Initialize local git repository
git init

# Stage all project components
git add .

# Save snapshot state
git commit -m "feat: initial commit of core architectural code and docker configurations"

# Rename default branch to main
git branch -M main

# Link your local repo to your GitHub remote repository
git remote add origin https://github.com/YOUR_USERNAME/rag-engine.git

# Push changes up to GitHub
git push -u origin main
