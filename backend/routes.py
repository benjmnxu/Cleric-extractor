
from fastapi import APIRouter, HTTPException, BackgroundTasks

from utils.parser import parser
from utils.prompts import *
from utils.population import populate_facts

from utils.models import GetQuestionAndFactsResponse

router = APIRouter()
result = None

@router.post("/submit_question_and_documents")
async def submit(payload: dict, background_tasks: BackgroundTasks):
    global result
    question = payload.get("question")
    documents = payload.get("documents", [])
    try:
        result = GetQuestionAndFactsResponse(question=question, facts=[], status="processing")
        logs = [parser(document) for document in documents]
        background_tasks.add_task(populate_facts, result, logs)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/get_question_and_facts")
async def get():
    global result
    if result is None:
        raise HTTPException(status_code=404, detail="No result available")
    return result