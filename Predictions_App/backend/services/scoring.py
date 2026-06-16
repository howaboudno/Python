#Imports
from sqlalchemy.orm import Session
from backend.models.models import FixturePrediction, Results, Fixture, GroupPrediction, GroupResults, BonusPredictions, Tournament, FixturePrediction
#==Dictionaries==#

GROUP_STAGE_POINTS = {
    "exact": 6,
    "result": 3,
    "wrong": 0
}

KO_STAGE_POINTS = {
    "R32": {"exact": 6,  "gd": 4,  "result": 3,  "penalty": 1},
    "R16": {"exact": 12, "gd": 8,  "result": 6,  "penalty": 1},
    "QF":  {"exact": 24, "gd": 16, "result": 12, "penalty": 1},
    "SF":  {"exact": 48, "gd": 32, "result": 24, "penalty": 1},
    "F":   {"exact": 96, "gd": 64, "result": 48, "penalty": 1},
}

#==Determine match result helper==#
def get_result(score_1: int, score_2: int) -> str:
    if score_1 > score_2:
        return "home"
    if score_1 == score_2:
        return "draw"
    if score_1 < score_2:
        return "away"
#==Determine pen result helper==#
def get_pen_result(pscore_1: int, pscore_2: int) -> str:
    if pscore_1 > pscore_2:
        return "home"
    if pscore_1 == pscore_2:
        return "draw"
    if pscore_1 < pscore_2:
        return "away"

#==Scoring engine==#

#--Points for group matches--#
def score_group_match(
    p: FixturePrediction,
    r: Results
) -> int:
    if p.predicted_score_1 == r.score_1 and p.predicted_score_2 == r.score_2:
        return  GROUP_STAGE_POINTS['exact']
    if get_result(r.score_1, r.score_2) == get_result(p.predicted_score_1,p.predicted_score_2):
            return GROUP_STAGE_POINTS['result']
    else:
        return GROUP_STAGE_POINTS['wrong']

#--Points for KO matches--#    
def score_ko_match(
    p: FixturePrediction,
    r: Results,
    s: Fixture
) -> int:
    base_points = 0
    if p.predicted_score_1 == r.score_1 and p.predicted_score_2 == r.score_2:
        base_points =  KO_STAGE_POINTS[s.stage]['exact']
    elif get_result(r.score_1, r.score_2) == get_result(p.predicted_score_1,p.predicted_score_2) and p.predicted_score_1 - p.predicted_score_2 == r.score_1 - r.score_2:
        base_points = KO_STAGE_POINTS[s.stage]['gd']
    elif get_result(r.score_1, r.score_2) == get_result(p.predicted_score_1,p.predicted_score_2):
        base_points = KO_STAGE_POINTS[s.stage]['result']
    if  r.pen_score_1 is not None and get_pen_result(r.pen_score_1, r.pen_score_2) == get_pen_result(p.predicted_pen_score_1, p.predicted_pen_score_2):
        base_points += KO_STAGE_POINTS[s.stage]['penalty']
    return base_points

#--Points for group result predictions--#
def score_group_rankings(
    user_id: int,
    tournament_id: int,
    db: Session,
) -> int:
    group_prediction_points = 0
    predictions = db.query(GroupPrediction).filter(
        GroupPrediction.user_id == user_id,
        GroupPrediction.tournament_id == tournament_id
    ).all()
    results = db.query(GroupResults).filter(
        GroupResults.tournament_id == tournament_id,
    ).all()
    for prediction in predictions:
        result = next((x for x in results if x.group_id == prediction.group_id), None)
        if result is None:
            continue
        if prediction.first_place == result.first_place:
            group_prediction_points += 20
        if prediction.second_place == result.second_place:
            group_prediction_points += 12
        if prediction.third_place == result.third_place:
            group_prediction_points += 8
        if prediction.first_place == result.first_place and prediction.second_place == result.second_place and prediction.third_place == result.third_place:
            group_prediction_points += 8
    return group_prediction_points

#--Points for winner, topscorer==#
def score_bonus(
    user_id: int,
    tournament_id: int,
    db: Session
) -> int:
    bonus_points = 0
    bonus = db.query(BonusPredictions).filter(
        BonusPredictions.user_id == user_id,
        BonusPredictions.tournament_id == tournament_id
    ).first()
    if bonus is None:
        return 0
    results = db.query(Tournament).filter(
        Tournament.id == tournament_id
    ).first()
    if results is None:
        return 0
    if bonus.predicted_top_scorer == results.top_scorer:
        bonus_points += 50
    if bonus.predicted_winner == results.winner:
        bonus_points += 50
    return bonus_points

#--Combine all scores for total points--#
def calculate_total(
    user_id: int,
    tournament_id: int,
    db: Session
) -> dict:
    fixture_points = 0
    fixtures = db.query(FixturePrediction).join(
        Fixture, Fixture.id == FixturePrediction.fixture_id).filter(
            FixturePrediction.user_id == user_id,
            Fixture.tournament_id == tournament_id).all()
    for fixture in fixtures:
        #Check result
        result = db.query(Results).filter(
            Results.fixture_id == fixture.fixture_id).first()
        if result is None:
            continue
        #Check stage (group or KO)
        fixture_data = db.query(Fixture).filter(
            Fixture.id == fixture.fixture_id
        ).first()
        if fixture_data.stage == "Group":
            fixture_points += score_group_match(fixture, result)
        elif fixture_data.stage != "Group":
            fixture_points += score_ko_match(fixture, result, fixture_data)
    #Add bonus points
    ranking_points = score_group_rankings(user_id, tournament_id, db)
    bonus_points = score_bonus(user_id, tournament_id, db)
    return {
            "total": fixture_points + ranking_points + bonus_points,
        "fixture_points": fixture_points,
        "ranking_points": ranking_points,
        "bonus_points": bonus_points
        }