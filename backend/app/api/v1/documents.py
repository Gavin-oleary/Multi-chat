from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import io
import json

from app.database import get_db
from app.schemas.document import DocumentCreate, DocumentResponse, SimilaritySearchRequest, SimilaritySearchResult
from app.services import document_service

# Import text extraction libraries
try:
    from pypdf import PdfReader
    PYPDF_AVAILABLE = True
except ImportError:
    try:
        import PyPDF2
        PdfReader = PyPDF2.PdfReader
        PYPDF_AVAILABLE = True
    except ImportError:
        PYPDF_AVAILABLE = False

try:
    from docx import Document as DocxDocument
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False

import chardet

router = APIRouter()


def extract_text_from_pdf(content: bytes) -> str:
    """Extract text from PDF file."""
    if not PYPDF_AVAILABLE:
        raise HTTPException(
            status_code=500,
            detail="PDF support not installed. Run: pip install pypdf"
        )
    
    pdf_file = io.BytesIO(content)
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text


def extract_text_from_docx(content: bytes) -> str:
    """Extract text from DOCX file."""
    if not DOCX_AVAILABLE:
        raise HTTPException(
            status_code=500,
            detail="DOCX support not installed. Run: pip install python-docx"
        )
    
    docx_file = io.BytesIO(content)
    doc = DocxDocument(docx_file)
    text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
    return text


def detect_encoding(content: bytes) -> str:
    """Detect the encoding of a text file."""
    result = chardet.detect(content)
    return result['encoding'] or 'utf-8'


@router.post("/", response_model=DocumentResponse)
async def create_document(
    document: DocumentCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a document and generate embeddings."""
    return await document_service.create_document_with_embeddings(
        content=document.content,
        metadata=document.doc_metadata,
        db=db
    )


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    """Upload a document and create embeddings from its text content."""
    try:
        content = await file.read()
        filename = file.filename.lower()
        text_content = None
        
        # Provide progress feedback for different file types
        file_size_mb = len(content) / (1024 * 1024)
        
        # Check file type and extract text accordingly
        if filename.endswith('.pdf'):
            if file_size_mb > 5:
                # For large PDFs, warn user it might take time
                print(f"Processing large PDF ({file_size_mb:.2f} MB): {file.filename}")
            text_content = extract_text_from_pdf(content)
            
        elif filename.endswith(('.doc', '.docx')):
            text_content = extract_text_from_docx(content)
            
        else:
            # Try to decode as text with various encodings
            encodings = ['utf-8', 'latin-1', 'windows-1252', 'iso-8859-1']
            
            # Use chardet for better encoding detection
            detected_encoding = detect_encoding(content)
            if detected_encoding and detected_encoding not in encodings:
                encodings.insert(0, detected_encoding)
            
            for encoding in encodings:
                try:
                    text_content = content.decode(encoding)
                    break
                except (UnicodeDecodeError, LookupError):
                    continue
            
            if text_content is None:
                raise HTTPException(
                    status_code=415,
                    detail=f"Unable to read file '{file.filename}'. Supported formats: TXT, MD, CSV, JSON, PDF, DOC, DOCX"
                )
        
        # Check if we got any content
        if not text_content or not text_content.strip():
            raise HTTPException(
                status_code=400,
                detail="The uploaded file appears to be empty or contains no extractable text."
            )
        
        # Provide feedback about processing embeddings
        print(f"Creating embeddings for document with {len(text_content)} characters...")
        
        # Create document with embeddings
        document = await document_service.create_document_with_embeddings(
            content=text_content,
            metadata={
                "filename": file.filename,
                "content_type": file.content_type,
                "file_size": len(content),
                "char_count": len(text_content)
            },
            db=db
        )
        
        return {
            "id": document.id,
            "message": f"Document '{file.filename}' uploaded successfully",
            "char_count": len(text_content),
            "status": "complete"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error processing upload: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing file: {str(e)}"
        )


@router.get("/", response_model=List[DocumentResponse])
async def list_documents(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """List all documents."""
    return await document_service.list_documents(db, skip, limit)


@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get a specific document."""
    document = await document_service.get_document(document_id, db)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document


@router.delete("/{document_id}")
async def delete_document(
    document_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete a document."""
    success = await document_service.delete_document(document_id, db)
    if not success:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"message": "Document deleted successfully"}


@router.post("/search", response_model=List[SimilaritySearchResult])
async def search_documents(
    search_request: SimilaritySearchRequest,
    db: AsyncSession = Depends(get_db)
):
    """Perform semantic similarity search."""
    results = await document_service.similarity_search(
        query=search_request.query,
        db=db,
        top_k=search_request.top_k
    )
    return results