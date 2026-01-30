from pydantic import BaseModel, Field
from typing import List

class PredictionRequest(BaseModel):
    answers: List[int] = Field(..., min_length=10, max_length=10)
