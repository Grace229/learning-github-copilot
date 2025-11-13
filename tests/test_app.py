import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Basketball Team" in data
    assert "participants" in data["Basketball Team"]


def test_signup_for_activity_success():
    activity = "Basketball Team"
    email = "newstudent@mergington.edu"
    # Ensure not already signed up
    client.get("/activities")  # warm up
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert f"Signed up {email} for {activity}" in response.json()["message"]
    # Check participant added
    activities = client.get("/activities").json()
    assert email in activities[activity]["participants"]


def test_signup_for_activity_duplicate():
    activity = "Basketball Team"
    email = "alex@mergington.edu"  # already signed up
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
    assert "Student already signed up" in response.json()["detail"]


def test_signup_for_activity_not_found():
    response = client.post("/activities/Nonexistent/signup?email=test@mergington.edu")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_root_redirect():
    response = client.get("/")
    assert response.status_code == 200
    assert "<!DOCTYPE html>" in response.text
