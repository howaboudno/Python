# routers/predictions/GET.py

#Imports
from fastapi import APIRouter, Depends
from backend.models.models import User, FixturePrediction, GroupPrediction, BonusPredictions
from backend.core.security import get_current_user
from backend.core.database import get_db
from sqlalchemy.orm import Session

#Router
router = APIRouter()

#==Prediction Routes==#

@router.get("/predictions/me/{tournament_id}")
def get_my_predictions(
    tournament_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    fixture_predictions = db.query(FixturePrediction).filter(
        FixturePrediction.user_id == current_user.id
    ).all()

    group_predictions = db.query(GroupPrediction).filter(
        GroupPrediction.user_id == current_user.id,
        GroupPrediction.tournament_id == tournament_id
    ).all()

    bonus_prediction = db.query(BonusPredictions).filter(
        BonusPredictions.user_id == current_user.id,
        BonusPredictions.tournament_id == tournament_id
    ).first()

    return {
        "fixture_predictions": fixture_predictions,
        "group_predictions": group_predictions,
        "bonus_prediction": bonus_prediction
    }