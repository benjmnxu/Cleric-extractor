from pydantic import BaseModel
from typing import List

class GetQuestionAndFactsResponse(BaseModel):
    question: str
    facts: List[str]
    status: str