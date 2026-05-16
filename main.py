import os
import shutil
from pathlib import Path
from typing import List
from fastapi import FastAPI, UploadFile, File, HTTPException
from dotenv import load_dotenv

from manager.database_manager import DatabaseManager
from engine.rag_engine import RAGEngine
from helper.utils import extract_text_from_file

load_dotenv()

app = FastAPI(title="Product Browser RAG API")

storage_path_str = os.getenv("FILES_STORAGE_PATH", "files")
FILES_DIR = Path(storage_path_str)
FILES_DIR.mkdir(parents=True, exist_ok=True)

db_mgr = DatabaseManager(
    host=os.getenv("MILVUS_HOST"),
    port=os.getenv("MILVUS_PORT"),
    collection_name=os.getenv("MILVUS_COLLECTION_NAME"),
    dimension=int(os.getenv("MILVUS_EMBEDDING_DIMENSION"))
)

rag = RAGEngine(
    db_manager=db_mgr,
    embed_model=os.getenv("OLLAMA_EMBED_MODEL"),
    gen_model=os.getenv("OLLAMA_GEN_MODEL"),
    ollama_url=os.getenv("OLLAMA_API_URL")
)

@app.post("/ingest")
async def ingest_knowledge(file: UploadFile = File(...)):
    """Saves file to disk, extracts text, and embeds into Milvus."""
    
    file_path = FILES_DIR / file.filename
    
    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")

    file.file.seek(0)
    content = await file.read()
    text = extract_text_from_file(content, file.filename)
    
    if not text.strip():
        if file_path.exists():
            os.remove(file_path)
        raise HTTPException(status_code=400, detail="Could not extract text from file.")
    
    rag.ingest(text, file.filename)
    
    return {
        "status": "success", 
        "filename": file.filename, 
        "storage_path": str(file_path)
    }

@app.delete("/knowledge/{doc_id}")
def delete_knowledge(doc_id: int):
    """Deletes record from Milvus, SQLite, and removes the physical file."""
    
    cursor = db_mgr.sql_conn.cursor()
    cursor.execute("SELECT source FROM docs WHERE id = ?", (doc_id,))
    row = cursor.fetchone()
    
    if not row:
        raise HTTPException(status_code=404, detail="Knowledge ID not found.")
    
    filename = row[0]
    file_path = FILES_DIR / filename

    try:
        db_mgr.milvus_client.delete(
            collection_name=db_mgr.collection_name,
            ids=[doc_id]
        )
    except Exception as e:
        print(f"Milvus delete error (might be empty): {e}")

    cursor.execute("DELETE FROM docs WHERE id = ?", (doc_id,))
    db_mgr.sql_conn.commit()

    if file_path.exists():
        os.remove(file_path)
        file_status = "Physical file deleted."
    else:
        file_status = "File not found on disk, but database record cleared."
    
    return {
        "status": "success", 
        "message": f"Document {doc_id} removed.",
        "file_cleanup": file_status
    }

@app.get("/knowledge")
def get_knowledge_list():
    cursor = db_mgr.sql_conn.cursor()
    cursor.execute("SELECT id, source, created_at FROM docs")
    rows = cursor.fetchall()
    
    return [
        {"id": r[0], "filename": r[1], "date": r[2]} 
        for r in rows
    ]

@app.get("/browse")
def browse(query: str):
    answer = rag.generate_answer(query)
    return {"query": query, "response": answer}

@app.post("/cleanup")
async def cleanup_all_knowledge():
    try:
        # 1. Clear Milvus
        db_mgr.milvus_client.drop_collection(db_mgr.collection_name)
        
        # Pull dimension as INT to prevent Param errors
        dim = int(os.getenv("MILVUS_EMBEDDING_DIMENSION", 768))
        db_mgr._prepare_milvus(dim)

        # 2. Clear SQLite
        cursor = db_mgr.sql_conn.cursor()
        cursor.execute("DELETE FROM docs")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='docs'")
        db_mgr.sql_conn.commit()

        # 3. Clear Files
        if FILES_DIR.exists():
            for file in FILES_DIR.iterdir():
                if file.is_file():
                    file.unlink()

        return {"status": "success", "message": "System reset successfully."}
    except Exception as e:
        # Log the full error to console for debugging
        print(f"Cleanup Error: {e}")
        raise HTTPException(status_code=500, detail=f"Cleanup failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)