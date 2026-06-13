# routers/predictions/POST.py

#Imports
from fastapi import APIRouter, Depends, HTTPException, status
from backend.models.models import User, Fixture, FixturePrediction, GroupPrediction, BonusPredictions
from backend.core.security import get_current_user
from backend.core.database import get_db
from backend.schemas.prediction import FixturePredictionCreate, GroupPredictionCreate, BonusPredictionCreate
from sqlalchemy.orm import Session
from datetime import datetime, timezone

#Router
router = APIRouter()

#==Prediction Routes==#

@router.post("/predictions/fixture")
def predict_fixture(
    prediction: FixturePredictionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    fixture = db.query(Fixture).filter(Fixture.id == prediction.fixture_id).first()
    if not fixture:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Fixture not found")

    # Enforce match lock
    if fixture.fixture_time.replace(tzinfo=timezone.utc) <= datetime.now(timezone.utc):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Predictions are locked after kickoff")

    existing = db.query(FixturePrediction).filter(
        FixturePrediction.user_id == current_user.id,
        FixturePrediction.fixture_id == prediction.fixture_id
    ).first()

    if existing:
        existing.predicted_score_1 = prediction.predicted_score_1
        existing.predicted_score_2 = prediction.predicted_score_2
        existing.predicted_pen_score_1 = prediction.predicted_pen_score_1
        existing.predicted_pen_score_2 = prediction.predicted_pen_score_2
    else:
        db.add(FixturePrediction(
            user_id=current_user.id,
            fixture_id=prediction.fixture_id,
            predicted_score_1=prediction.predicted_score_1,
            predicted_score_2=prediction.predicted_score_2,
            predicted_pen_score_1=prediction.predicted_pen_score_1,
            predicted_pen_score_2=prediction.predicted_pen_score_2
        ))

    db.commit()
    return {"message": "Prediction saved"}


@router.post("/predictions/group")
def predict_group(
    prediction: GroupPredictionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    existing = db.query(GroupPrediction).filter(
        GroupPrediction.user_id == current_user.id,
        GroupPrediction.tournament_id == prediction.tournament_id,
        GroupPrediction.group == prediction.group
    ).first()

    if existing:
        existing.first = prediction.first
        existing.second = prediction.second
        existing.third = prediction.third
    else:
        db.add(GroupPrediction(
            user_id=current_user.id,
            tournament_id=prediction.tournament_id,
            group=prediction.group,
            first=prediction.first,
            second=prediction.second,
            third=prediction.third
        ))

    db.commit()
    return {"message": "Group prediction saved"}


@router.post("/predictions/bonus")
def predict_bonus(
    prediction: BonusPredictionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    existing = db.query(BonusPredictions).filter(
        BonusPredictions.user_id == current_user.id,
        BonusPredictions.tournament_id == prediction.tournament_id
    ).first()

    if existing:
        existing.predicted_winner = prediction.predicted_winner
        existing.predicted_top_scorer = prediction.predicted_top_scorer
    else:
        db.add(BonusPredictions(
            user_id=current_user.id,
            tournament_id=prediction.tournament_id,
            predicted_winner=prediction.predicted_winner,
            predicted_top_scorer=prediction.predicted_top_scorer
        ))

    db.commit()
    return {"message": "Bonus prediction saved"}