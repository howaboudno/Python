#Imports
from types import SimpleNamespace
from backend.services.scoring import score_group_match, score_ko_match

#==Group Match tests==#

#Exact Score
def test_group_match_exact():
    prediction = SimpleNamespace(predicted_score_1=2, predicted_score_2=1)
    result = SimpleNamespace(score_1=2, score_2=1)
    assert score_group_match(prediction, result) == 6

#Correct result, but not exact score
def test_group_match_correct():
    prediction = SimpleNamespace(predicted_score_1=2, predicted_score_2=1)
    result = SimpleNamespace(score_1=4, score_2=1)
    assert score_group_match(prediction, result) == 3

#Wrong result
def test_group_match_wrong():
    prediction = SimpleNamespace(predicted_score_1=2, predicted_score_2=1)
    result = SimpleNamespace(score_1=1, score_2=2)
    assert score_group_match(prediction, result) == 0
    

#==KO stage tests==#
def test_R16_match_exact():
    prediction = SimpleNamespace(predicted_score_1=2, predicted_score_2=1, predicted_pen_score_1 =None, predicted_pen_score_2=None)
    result = SimpleNamespace(score_1=2, score_2=1, pen_score_1=None, pen_score_2=None)
    stage = SimpleNamespace(stage='R16')
    assert score_ko_match(prediction, result, stage) == 12

def test_QF_match_GD():
    prediction = SimpleNamespace(predicted_score_1=2, predicted_score_2=1, predicted_pen_score_1 =None, predicted_pen_score_2=None)
    result = SimpleNamespace(score_1=3, score_2=2, pen_score_1=None, pen_score_2=None)
    stage = SimpleNamespace(stage='QF')
    assert score_ko_match(prediction, result, stage) == 16
    
def test_R16_match_exact_pen():
    prediction = SimpleNamespace(predicted_score_1=1, predicted_score_2=1, predicted_pen_score_1 =4, predicted_pen_score_2=5)
    result = SimpleNamespace(score_1=1, score_2=1, pen_score_1=4, pen_score_2=5)
    stage = SimpleNamespace(stage='R16')
    assert score_ko_match(prediction, result, stage) == 13

def test_R16_match_wrongresult_pen():
    prediction = SimpleNamespace(predicted_score_1=2, predicted_score_2=1, predicted_pen_score_1 =4, predicted_pen_score_2=5)
    result = SimpleNamespace(score_1=1, score_2=1, pen_score_1=4, pen_score_2=5)
    stage = SimpleNamespace(stage='R16')
    assert score_ko_match(prediction, result, stage) == 1

def test_R16_match_result_pen():
    prediction = SimpleNamespace(predicted_score_1=2, predicted_score_2=2, predicted_pen_score_1 =4, predicted_pen_score_2=5)
    result = SimpleNamespace(score_1=1, score_2=1, pen_score_1=4, pen_score_2=5)
    stage = SimpleNamespace(stage='R16')
    assert score_ko_match(prediction, result, stage) == 9