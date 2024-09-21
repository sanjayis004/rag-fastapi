from fastapi import APIRouter, File, UploadFile
from app.services.question_service import answer_from_document

router = APIRouter()

@router.post("/answer/")
async def answer_from_document_route(file: UploadFile = File(...), questions: UploadFile = File(...)):
    return await answer_from_document(file, questions)
