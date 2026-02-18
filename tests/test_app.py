import sys
sys.path.append('/workspaces/getting-started-with-github-copilot/src')
from app import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_for_activity():
    # Test successful signup
    response = client.post("/activities/Chess%20Club/signup", json={"email": "test_signup@mergington.edu"})
    assert response.status_code == 200
    data = response.json()
    assert "Signed up" in data["message"]

    # Verify participant added
    response = client.get("/activities")
    data = response.json()
    assert "test_signup@mergington.edu" in data["Chess Club"]["participants"]

def test_signup_duplicate():
    # First signup
    client.post("/activities/Chess%20Club/signup", json={"email": "test_duplicate@mergington.edu"})
    # Second signup should fail
    response = client.post("/activities/Chess%20Club/signup", json={"email": "test_duplicate@mergington.edu"})
    assert response.status_code == 400
    data = response.json()
    assert "already signed up" in data["detail"]

def test_signup_invalid_activity():
    response = client.post("/activities/Invalid%20Activity/signup", json={"email": "test_invalid@mergington.edu"})
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]

def test_unregister_from_activity():
    # First signup
    client.post("/activities/Programming%20Class/signup", json={"email": "test_unregister@mergington.edu"})
    # Then unregister
    response = client.delete("/activities/Programming%20Class/signup/test_unregister@mergington.edu")
    assert response.status_code == 200
    data = response.json()
    assert "Unregistered" in data["message"]

    # Verify removed
    response = client.get("/activities")
    data = response.json()
    assert "test_unregister@mergington.edu" not in data["Programming Class"]["participants"]

def test_unregister_not_signed_up():
    response = client.delete("/activities/Chess%20Club/signup/test_not_signed@mergington.edu")
    assert response.status_code == 400
    data = response.json()
    assert "not signed up" in data["detail"]

def test_unregister_invalid_activity():
    response = client.delete("/activities/Invalid%20Activity/signup/test_unregister_invalid@mergington.edu")
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]