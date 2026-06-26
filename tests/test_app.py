from fastapi.testclient import TestClient

from src.app import app


def test_root_redirects_to_static_index():
    # Arrange
    client = TestClient(app)

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_all_activities():
    # Arrange
    client = TestClient(app)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    activities = response.json()
    assert isinstance(activities, dict)
    assert "Chess Club" in activities


def test_signup_for_activity_success():
    # Arrange
    client = TestClient(app)
    activity_name = "Chess Club"
    email = "tester@example.com"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}


def test_signup_for_activity_unknown_returns_404():
    # Arrange
    client = TestClient(app)

    # Act
    response = client.post(
        "/activities/Nonexistent/signup",
        params={"email": "tester2@example.com"}
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_for_activity_duplicate_returns_400():
    # Arrange
    client = TestClient(app)
    activity_name = "Programming Class"
    existing_email = "emma@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": existing_email}
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_remove_participant_success():
    # Arrange
    client = TestClient(app)
    activity_name = "Gym Class"
    email = "john@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Removed {email} from {activity_name}"}


def test_remove_participant_unknown_activity_returns_404():
    # Arrange
    client = TestClient(app)

    # Act
    response = client.delete(
        "/activities/Nonexistent/participants",
        params={"email": "tester3@example.com"}
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_remove_participant_not_enrolled_returns_404():
    # Arrange
    client = TestClient(app)
    activity_name = "Basketball Club"
    email = "not-found@example.com"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in this activity"
