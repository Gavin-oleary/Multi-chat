from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_db
import io
import chardet
try:
    import PyPDF2
except ImportError:
    PyPDF2 = None
try:
    from docx import Document as DocxDocument
except ImportError:
    DocxDocument = None
from app.schemas.document import (
    DocumentCreate,
    DocumentResponse,
    DocumentWithChunks,
    SimilaritySearchRequest,
    SimilaritySearchResult
)
from app.services import document_service

router = APIRouter()


def extract_text_from_pdf(content: bytes) -> str:
    """Extract text from PDF file content."""
    if PyPDF2 is None:
        raise HTTPException(
            status_code=500,
            detail="PDF support is not installed. Please install PyPDF2."
        )
    
    try:
        pdf_file = io.BytesIO(content)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        text_content = []
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text = page.extract_text()
            if text.strip():
                text_content.append(text)
        
        if not text_content:
            raise ValueError("No text content found in PDF")
            
        return "\n\n".join(text_content)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to extract text from PDF: {str(e)}"
        )


def extract_text_from_docx(content: bytes) -> str:
    """Extract text from Word document."""
    if DocxDocument is None:
        raise HTTPException(
            status_code=500,
            detail="Word document support is not installed. Please install python-docx."
        )
    
    try:
        docx_file = io.BytesIO(content)
        doc = DocxDocument(docx_file)
        
        text_content = []
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():
                text_content.append(paragraph.text)
        
        # Also extract text from tables
        for table in doc.tables:
            for row in table.rows:
                row_text = []
                for cell in row.cells:
                    if cell.text.strip():
                        row_text.append(cell.text)
                if row_text:
                    text_content.append(" | ".join(row_text))
        
        if not text_content:
            raise ValueError("No text content found in document")
            
        return "\n\n".join(text_content)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to extract text from Word document: {str(e)}"
        )


def detect_encoding(content: bytes) -> str:
    """Detect encoding of text content."""
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
    content = await file.read()
    filename = file.filename.lower()
    text_content = None
    
    # Check file type and extract text accordingly
    if filename.endswith('.pdf'):
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
        "char_count": len(text_content)
    }


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


@router.get("/{document_id}", response_model=DocumentWithChunks)
async def get_document(
    document_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get a document with all its chunks."""
    # Implementation here
    pass