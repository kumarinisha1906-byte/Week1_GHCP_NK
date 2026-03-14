import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# Test GET /activities
def test_get_activities():
    # Arrange: nothing to set up
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

# Test POST /activities/{activity_name}/signup
def test_signup_for_activity():
    # Arrange
    activity = "Math Olympiad"
    email = "testuser@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json()["message"]
    # Cleanup: remove test user
    client.post(f"/activities/{activity}/unregister?email={email}")

# Test POST /activities/{activity_name}/unregister
def test_unregister_from_activity():
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert response.status_code == 200
    assert f"Unregistered {email}" in response.json()["message"]
    # Cleanup: re-add user
    client.post(f"/activities/{activity}/signup?email={email}")

# Edge case: invalid activity
def test_signup_invalid_activity():
    # Arrange
    activity = "Nonexistent Activity"
    email = "testuser@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"

# Edge case: duplicate signup
def test_signup_duplicate():
    # Arrange
    activity = "Programming Class"
    email = "emma@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"

# Edge case: unregister non-existent participant
def test_unregister_nonexistent():
    # Arrange
    activity = "Art Club"
    email = "notregistered@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student not registered"
