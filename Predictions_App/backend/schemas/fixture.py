from pydantic import BaseModel
from datetime import datetime

class FixtureCreate(BaseModel):
    tournament_id: int
    fixture_number: int
    group: str | None = None
    team_1: str
    team_2: str
    fixture_time: datetime
    stage: str

class FixtureUpdate(BaseModel):
    team_1: str | None = None
    team_2: str | None = None
    fixture_time: datetime | None = None