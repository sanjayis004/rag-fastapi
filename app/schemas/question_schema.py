from pydantic import BaseModel
from typing import List

class QuestionRequest(BaseModel):
    questions: List[str]
