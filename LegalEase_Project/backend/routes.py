from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from ai_core.gemini_generator import GeminiDocumentGenerator

router = APIRouter()
generator = GeminiDocumentGenerator()

class DocumentRequest(BaseModel):
    document_type: str = Field(..., min_length=2)
    parties: str = Field(..., min_length=2)
    terms: str = Field(..., min_length=2)
    dates: str = Field(..., min_length=2)

@router.post("/generate")
def generate_document(request: DocumentRequest):
    try:
        text = generator.generate_document(
            document_type=request.document_type,
            parties=request.parties,
            terms=request.terms,
            dates=request.dates,
        )
        return {"success": True, "document": text}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
