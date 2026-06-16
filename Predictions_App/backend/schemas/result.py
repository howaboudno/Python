from pydantic import BaseModel

class ResultCreate(BaseModel):
    fixture_id: int
    score_1: int
    score_2: int
    pen_score_1: int | None = None
    pen_score_2: int | None = None
