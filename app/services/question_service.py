from fastapi import HTTPException, UploadFile
import pdfplumber
import json
from transformers import pipeline

qa_pipeline = pipeline("question-answering", model="deepset/roberta-base-squad2")

async def answer_from_document(file, questions):
    try:
        questions_bytes = await questions.read()
        questions_content = json.loads(questions_bytes.decode('ISO-8859-1'))
        questions_list = questions_content.get('questions', [])
        if not questions_list:
            raise HTTPException(status_code=400, detail="No questions provided in the JSON file.")
        if file.filename.endswith(".pdf"):
            document_text = process_pdf(file)
            if not document_text:
                raise HTTPException(status_code=400, detail="No text found in the PDF.")
        elif file.filename.endswith(".json"):
            document_content = json.loads(await file.read())
            document_text = document_content.get('content', '')
            if not document_text:
                raise HTTPException(status_code=400, detail="No content found in the JSON file.")
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type. Only PDF and JSON are allowed.")
        answers = answer_questions(questions_list, document_text)
        return answers
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format in the questions or document file.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

def process_pdf(file: UploadFile):
    text = ""
    with pdfplumber.open(file.file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    return text

def answer_questions(questions, context):
    results = {}
    for question in questions:
        if not question.strip():
            results[question] = "Question is empty."
            continue
        result = qa_pipeline(question=question, context=context)
        results[question] = result.get('answer', "No answer found.")
    return results
