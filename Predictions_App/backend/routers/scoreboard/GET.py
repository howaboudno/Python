from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.core.database import get_db
from backend.models.models import User, Tournament
from backend.services.scoring import calculate_total

router = APIRouter()


#Live scoreboard, ranked by total points
@router.get("/tournaments/{tournament_id}/scoreboard")
def get_scoreboard(tournament_id: int, db: Session = Depends(get_db)):
    tournament = db.query(Tournament).filter(Tournament.id == tournament_id).first()
    if not tournament:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tournament not found")

    users = db.query(User).all()

    scoreboard = []
    for user in users:
        breakdown = calculate_total(user.id, tournament_id, db)
        scoreboard.append({
            "user_id": user.id,
            "username": user.username,
            "total": breakdown["total"],
            "fixture_points": breakdown["fixture_points"],
            "ranking_points": breakdown["ranking_points"],
            "bonus_points": breakdown["bonus_points"],
        })

    #Sort by total points, highest first
    scoreboard.sort(key=lambda entry: entry["total"], reverse=True)

    return {"results": scoreboard}


#Single player breakdown (same data as one row above, but standalone)
@router.get("/tournaments/{tournament_id}/scoreboard/{user_id}")
def get_player_breakdown(tournament_id: int, user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    breakdown = calculate_total(user_id, tournament_id, db)

    return {
        "user_id": user.id,
        "username": user.username,
        **breakdown
    }