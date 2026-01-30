from pydantic import BaseModel, Field
from typing import List

class QuestionnaireCreate(BaseModel):
    child_id: int
    answers: List[int] = Field(..., min_length=10, max_length=10)
