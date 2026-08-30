from uuid import uuid4

from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_signup_and_unregister_participant():
    # Arrange
    activity_name = "Chess Club"
    email = f"newstudent-{uuid4()}@mergington.edu"

    # Act: sign up the participant
    signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    activities_after_signup = client.get("/activities").json()

    # Assert: the signup response and persisted activity list reflect the new participant
    assert signup_response.status_code == 200
    assert signup_response.json()["message"] == f"Signed up {email} for {activity_name}"
    assert email in signup_response.json()["participants"]
    assert email in activities_after_signup[activity_name]["participants"]

    # Act: unregister the participant
    unregister_response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
    activities_after_unregister = client.get("/activities").json()

    # Assert: the unregister response and persisted activity list no longer include the participant
    assert unregister_response.status_code == 200
    assert unregister_response.json()["message"] == f"Unregistered {email} from {activity_name}"
    assert email not in unregister_response.json()["participants"]
    assert email not in activities_after_unregister[activity_name]["participants"]


def test_unregister_missing_participant_returns_404_or_400():
    # Arrange
    missing_email = f"missing-{uuid4()}@mergington.edu"

    # Act
    response = client.delete(f"/activities/Chess Club/unregister?email={missing_email}")
    response_json = response.json()

    # Assert
    assert response.status_code in {400, 404}
    assert "detail" in response_json
