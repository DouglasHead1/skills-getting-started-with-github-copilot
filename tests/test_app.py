from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_signup_and_unregister_participant():
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 200
    assert email in response.json()["participants"] or email in client.get("/activities").json()[activity_name]["participants"]

    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
    assert response.status_code == 200
    assert email not in client.get("/activities").json()[activity_name]["participants"]


def test_unregister_missing_participant_returns_404_or_400():
    missing_email = "missing@mergington.edu"
    response = client.delete(f"/activities/Chess Club/unregister?email={missing_email}")
    assert response.status_code in {400, 404}
