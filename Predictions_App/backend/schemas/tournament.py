from pydantic import BaseModel

class TournamentCreate(BaseModel):
    name: str
    tournament_type: str
    year: int

class Tournaments(BaseModel):
    id: int
    name: str
    tournament_type: str
    year: str
    is_active: bool
