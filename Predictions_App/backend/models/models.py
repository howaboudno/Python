#==Create Base Model==#
from sqlalchemy import Column, DateTime, Integer, String, Boolean, ForeignKey

from backend.core.database import Base

#==Define User Model==#
class User(Base):
    __tablename__ = 'users' 
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False)

#==Define Tournament, Fixture, Results==#
class Tournament(Base):
    __tablename__ = 'tournaments'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    tournament_type = Column(String(50), nullable=False)
    year = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True)

class Fixture(Base):
    __tablename__ = 'fixtures'
    id = Column(Integer, primary_key=True)
    tournament_id = Column(Integer, ForeignKey('tournaments.id'), nullable=False)
    fixture_number = Column(String(50), unique=True, nullable=False)
    group = Column(String(50), nullable=True)
    team_1 = Column(String(50), nullable=False)
    team_2 = Column(String(50), nullable=False)
    fixture_time = Column(DateTime, nullable=False)
    stage = Column(String(50), nullable=False)

class Results(Base):
    __tablename__ = 'results'
    id = Column(Integer, primary_key=True)
    fixture_id = Column(Integer, ForeignKey('fixtures.id'), nullable=False)
    score_1 = Column(Integer, nullable=False)
    score_2 = Column(Integer, nullable=False)
    pen_score_1 = Column(Integer, nullable=True)
    pen_score_2 = Column(Integer, nullable=True)


#==Define Prediction Models==#

class FixturePrediction(Base):
    __tablename__ = 'fixture_predictions'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    fixture_id = Column(Integer, ForeignKey('fixtures.id'), nullable=False)
    predicted_score_1 = Column(Integer, nullable=False)
    predicted_score_2 = Column(Integer, nullable=False)
    predicted_pen_score_1 = Column(Integer, nullable=True)
    predicted_pen_score_2 = Column(Integer, nullable=True)

class GroupPrediction(Base):
    __tablename__ = 'group_predictions'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    tournament_id = Column(Integer, ForeignKey('tournaments.id'), nullable=False)
    group_id = Column(String(50), ForeignKey('fixtures.group'), nullable=False)
    first_place = Column(String(50), nullable=False)
    second_place = Column(String(50), nullable=False)
    third_place = Column(String(50), nullable=False)

class BonusPredictions(Base):
    __tablename__ = 'bonus_predictions'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    tournament_id = Column(Integer, ForeignKey('tournaments.id'), nullable=False)
    predicted_winner = Column(String(50), nullable=False)
    predicted_top_scorer = Column(String(50), nullable=False)

