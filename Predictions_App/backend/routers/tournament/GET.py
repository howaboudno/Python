#Imports
from fastapi import APIRouter, Depends, HTTPException, status
from models.models import User, Tournament, Fixture
from core.security import get_current_user
from core.database import get_db
from sqlalchemy.orm import Session

#Router
router = APIRouter()

#==Tournament Routes==#

@router.get("/tournaments")
def get_tournaments(db: Session = Depends(get_db)):
    results = db.query(Tournament).all()
    return {"results": results}


@router.get("/tournaments/{tournament_id}")
def get_tournament_by_id(tournament_id: int, db: Session = Depends(get_db)):
    result = db.query(Tournament).filter(Tournament.id == tournament_id).first()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No tournament found for the given ID")
    return result


#==Fixture Routes==#

@router.get("/tournaments/{tournament_id}/fixtures")
def get_fixtures(tournament_id: int, db: Session = Depends(get_db)):
    fixtures = db.query(Fixture).filter(Fixture.tournament_id == tournament_id).all()
    if not fixtures:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No fixtures found for the given tournament")
    return {"results": fixtures}


@router.get("/tournaments/{tournament_id}/fixtures/{fixture_id}")
def get_fixture_by_id(tournament_id: int, fixture_id: int, db: Session = Depends(get_db)):
    fixture = db.query(Fixture).filter(
        Fixture.id == fixture_id,
        Fixture.tournament_id == tournament_id
    ).first()
    if not fixture:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fixture not found")
    return fixture

@router.get("/tournaments/{tournament_id}/fixtures/{fixture_id}/result")
def get_result(tournament_id: int, fixture_id: int, db: Session = Depends(get_db)):
    result = db.query(Results).filter(Results.fixture_id == fixture_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="No result found")
    return result
