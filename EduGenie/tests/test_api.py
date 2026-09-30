from fastapi.testclient import TestClient
import main

client = TestClient(main.app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert "EduGenie" in response.text


def test_qa_without_real_api_key(monkeypatch):
    monkeypatch.setattr(main, "answer_question", lambda question: "Test answer")
    response = client.post("/qa", json={"question": "What is Python?"})
    assert response.status_code == 200
    assert response.json()["answer"] == "Test answer"


def test_explain_without_real_api_key(monkeypatch):
    monkeypatch.setattr(main, "explain_topic", lambda text: "Simple explanation")
    response = client.post("/explain", json={"text": "Photosynthesis"})
    assert response.status_code == 200
    assert response.json()["explanation"] == "Simple explanation"


def test_summarize_without_real_api_key(monkeypatch):
    monkeypatch.setattr(main, "summarize_text", lambda text: "Short summary")
    response = client.post("/summarize", json={"text": "Long passage"})
    assert response.status_code == 200
    assert response.json()["summary"] == "Short summary"


def test_learning_path_without_real_api_key(monkeypatch):
    monkeypatch.setattr(main, "get_learning_recommendations", lambda topic, level: "Plan")
    response = client.post(
        "/learn/recommendations",
        json={"topic": "SQL", "level": "Beginner"},
    )
    assert response.status_code == 200
    assert response.json()["recommendations"] == "Plan"


def test_quiz_without_real_api_key(monkeypatch):
    sample = [{
        "question": "2+2?",
        "options": ["1", "2", "3", "4"],
        "correct_answer": "4",
        "explanation": "Four.",
    }]
    monkeypatch.setattr(main, "generate_quiz", lambda text, count: sample)
    response = client.post("/quiz", json={"text": "Math", "count": 1})
    assert response.status_code == 200
    assert response.json()["quiz"][0]["correct_answer"] == "4"
