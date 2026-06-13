from pydantic import BaseModel

class FixturePredictionCreate(BaseModel):
    fixture_id: int
    predicted_score_1: int
    predicted_score_2: int
    predicted_pen_score_1: int | None = None
    predicted_pen_score_2: int | None = None

class GroupPredictionCreate(BaseModel):
    tournament_id: int
    group: str
    first: str
    second: str
    third: str

class BonusPredictionCreate(BaseModel):
    tournament_id: int
    predicted_winner: str
    predicted_top_scorer: str