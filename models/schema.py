from typing import List
from pydantic import BaseModel

class AnswerItem(BaseModel):
    answer: str


class QueryResponse(BaseModel):
    answers: List[AnswerItem]

class QueryRequest(BaseModel):
    documents: str
    questions: List[str]
