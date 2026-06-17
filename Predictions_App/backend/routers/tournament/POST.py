#Imports
from fastapi import APIRouter, Depends, HTTPException, status
from models.models import User, Tournament, Fixture, Results
from core.security import get_current_user
from core.database import get_db
from schemas.tournament import TournamentCreate
from schemas.fixture import FixtureCreate, FixtureUpdate
from schemas.result import ResultCreate
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from services.scoring import calculate_total

#Router
router = APIRouter()

#==Tournament Routes==#

@router.post("/tournaments")
def create_tournament(
    tournament: TournamentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admins only")

    db.add(Tournament(
        name=tournament.name,
        tournament_type=tournament.tournament_type,
        year=tournament.year,
        is_active=tournament.is_active
    ))
    db.commit()
    return {"message": f"Tournament {tournament.name} created"}


#==Fixture Routes==#

@router.post("/tournaments/{tournament_id}/fixtures")
def create_fixture(
    tournament_id: int,
    fixture: FixtureCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admins only")

    tournament = db.query(Tournament).filter(Tournament.id == tournament_id).first()
    if not tournament:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tournament not found")

    db_fixture = Fixture(
        tournament_id=tournament_id,
        fixture_number=fixture.fixture_number,
        group=fixture.group,
        team_1=fixture.team_1,
        team_2=fixture.team_2,
        fixture_time=fixture.fixture_time,
        stage=fixture.stage
    )
    db.add(db_fixture)
    db.commit()
    db.refresh(db_fixture)
    return db_fixture


@router.post("/tournaments/{tournament_id}/fixtures/{fixture_id}/update")
def update_fixture(
    tournament_id: int,
    fixture_id: int,
    updates: FixtureUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admins only")

    fixture = db.query(Fixture).filter(
        Fixture.id == fixture_id,
        Fixture.tournament_id == tournament_id
    ).first()
    if not fixture:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Fixture not found")

    # Enforce kickoff lock
    if fixture.fixture_time.replace(tzinfo=timezone.utc) <= datetime.now(timezone.utc):
        return "You're about to update a match that has already kicked off."

    if updates.team_1 is not None:
        fixture.team_1 = updates.team_1
    if updates.team_2 is not None:
        fixture.team_2 = updates.team_2
    if updates.fixture_time is not None:
        fixture.fixture_time = updates.fixture_time

    db.commit()
    db.refresh(fixture)
    return fixture


#==Result Routes==#

@router.post("/tournaments/{tournament_id}/fixtures/{fixture_id}/result")
def create_result(
    tournament_id: int,
    fixture_id: int,
    result: ResultCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admins only")

    fixture = db.query(Fixture).filter(
        Fixture.id == fixture_id,
        Fixture.tournament_id == tournament_id
    ).first()
    if not fixture:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Fixture not found")

    existing = db.query(Results).filter(Results.fixture_id == fixture_id).first()

    if existing:
        existing.score_1 = result.score_1
        existing.score_2 = result.score_2
        existing.pen_score_1 = result.pen_score_1
        existing.pen_score_2 = result.pen_score_2
        db.commit()
        db_result = existing
    else:
        db_result = Results(
            fixture_id=fixture_id,
            score_1=result.score_1,
            score_2=result.score_2,
            pen_score_1=result.pen_score_1,
            pen_score_2=result.pen_score_2
        )
        db.add(db_result)
        db.commit()
        db.refresh(db_result)

    users = db.query(User).all()
    for user in users:
        calculate_total(user.id, tournament_id, db)

    return db_result