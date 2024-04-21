
from fastapi import APIRouter, Body, Depends, Request, Response, HTTPException, BackgroundTasks
from starlette.responses import FileResponse

from utils.agents import Extractor, Merger
from utils.parser import parser
from utils.prompts import *
from models import GetQuestionAndFactsResponse

router = APIRouter()
result = None

extractor = Extractor()
merger = Merger()

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


def populate_facts(model_instance: GetQuestionAndFactsResponse, logs: list):
    previous_message = ""
    current_message = ""
    for i, log in enumerate(logs):
        if i == 0:
            previous_message = extractor.extract(model_instance.question, log)
        else:
            current_message = extractor.extract(model_instance.question, log)
            print(f"previous: {previous_message}")
            print(f"current: {current_message}")
            previous_message = merger.merge(current_message, previous_message)
            print(f"merge: {previous_message}")
    
    model_instance.status = "done"
    model_instance.facts = previous_message