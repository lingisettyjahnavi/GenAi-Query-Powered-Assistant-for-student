from pathlib import Path  # Added missing import
from studentapp.rag.extractor import extract_text_from_pdf
from studentapp.rag.chunker import split_text
from studentapp.rag.embeddings import embed_texts
from studentapp.rag.vector_store import (
    store_chunks,
    delete_document_chunks
)

def ingest_document(document):
    # Changed path() to Path()
    file_path = Path(document.file.path)
    
    if file_path.suffix.lower() != ".pdf":
        return {
            "status": "skipped",
            "message": "only pdf files are supported currently"
        }
        
    # Match your import name: extractor_text_from_pdf
    text = extract_text_from_pdf(file_path)
    
    if not text.strip():
        return {
            "status": "failed",
            "message": "no text could be extracted from the pdf"
        }
        
    chunks = split_text(text)
    if not chunks:
        return {
            "status": "failed",
            "message": "no chunks created"
        }

    try:
        # Match your import name: embed_texts
        embeddings = embed_texts(chunks)
    except Exception as e:
        return {
            "status": "failed",
            "message": f"Embedding failed: {str(e)}"
        }
        
    if len(embeddings) != len(chunks):
        return {
            "status": "failed",
            "message": "number of embeddings does not match number of chunks."
        }
        
    try:
        delete_document_chunks(document.id)
    except Exception as e:
        return {
            "status": "failed",
            "message": f"could not delete old chunks: {str(e)}"
        }
        
    try:
        store_chunks(
            chunks=chunks,
            embeddings=embeddings,
            student_id=document.student_id,
            document_id=document.id,
            source=document.title
        )
    except Exception as e:
        return {
            "status": "failed",
            "message": f"chromadb storage failed: {str(e)}"
        }
        
    return {
        "status": "success",
        "document_id": document.id,
        "student_id": document.student.id,
        "chunks": len(chunks)
    }
