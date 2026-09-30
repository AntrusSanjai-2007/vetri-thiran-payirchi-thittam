import json
import pytest

from quiz_module import clean_json_block, _validate


def test_clean_json_block():
    raw = '```json\n[{"question":"Q","options":["A","B","C","D"],"correct_answer":"A","explanation":"E"}]\n```'
    cleaned = clean_json_block(raw)
    data = json.loads(cleaned)
    assert data[0]["correct_answer"] == "A"


def test_validate_quiz():
    data = [
        {
            "question": "2 + 2 = ?",
            "options": ["1", "2", "3", "4"],
            "correct_answer": "4",
            "explanation": "Adding two and two gives four.",
        }
    ]
    assert _validate(data, 1)[0]["question"] == "2 + 2 = ?"


def test_validate_rejects_wrong_answer():
    data = [{
        "question": "Q",
        "options": ["A", "B", "C", "D"],
        "correct_answer": "Z",
        "explanation": "E",
    }]
    with pytest.raises(ValueError):
        _validate(data, 1)
