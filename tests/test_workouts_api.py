import pytest
from app.models import Workout

# ---------- Health ----------
def test_health(client):
    r = client.get("/api/health")
    assert r.status_code == 200
    assert r.get_json()["status"] == "ok"

# ---------- Create Workout ----------
def test_create_workout_success(client):
    r = client.post("/api/workouts", json={"workout": "Running", "duration": 45})
    assert r.status_code == 201
    data = r.get_json()
    assert data["workout"] == "Running"
    assert data["duration"] == 45

def test_create_workout_missing_name(client):
    r = client.post("/api/workouts", json={"duration": 30})
    assert r.status_code == 400
    assert "workout" in r.get_json()["errors"]

def test_create_workout_blank_name(client):
    r = client.post("/api/workouts", json={"workout": "   ", "duration": 30})
    assert r.status_code == 400
    assert "workout" in r.get_json()["errors"]

def test_create_workout_invalid_duration(client):
    r = client.post("/api/workouts", json={"workout": "Yoga", "duration": "abc"})
    assert r.status_code == 400
    assert "duration" in r.get_json()["errors"]

def test_create_workout_negative_duration(client):
    r = client.post("/api/workouts", json={"workout": "Yoga", "duration": -10})
    assert r.status_code == 400
    assert "duration" in r.get_json()["errors"]

def test_create_workout_zero_duration(client):
    r = client.post("/api/workouts", json={"workout": "Yoga", "duration": 0})
    assert r.status_code == 400
    assert "duration" in r.get_json()["errors"]

def test_create_workout_large_duration(client):
    r = client.post("/api/workouts", json={"workout": "Marathon", "duration": 1000})
    assert r.status_code == 201
    assert r.get_json()["duration"] == 1000

def test_create_workout_trims_whitespace(client):
    r = client.post("/api/workouts", json={"workout": "   Swim  ", "duration": 25})
    assert r.status_code == 201
    assert r.get_json()["workout"] == "Swim"

def test_create_workout_extra_fields_ignored(client):
    r = client.post("/api/workouts", json={"workout": "Rowing", "duration": 40, "foo": "bar"})
    assert r.status_code == 201
    assert "foo" not in r.get_json()

# ---------- List Workouts ----------
def test_list_workouts_returns_array(client):
    client.post("/api/workouts", json={"workout": "Cycling", "duration": 60})
    r = client.get("/api/workouts")
    assert r.status_code == 200
    data = r.get_json()
    assert isinstance(data, list)
    assert all("id" in item for item in data)

def test_list_workouts_order(client):
    client.post("/api/workouts", json={"workout": "A", "duration": 10})
    client.post("/api/workouts", json={"workout": "B", "duration": 20})
    r = client.get("/api/workouts")
    ids = [item["id"] for item in r.get_json()]
    assert ids == sorted(ids)  # ascending order

# ---------- Get by ID ----------
def test_get_workout_valid(client):
    created = client.post("/api/workouts", json={"workout": "Dance", "duration": 30}).get_json()
    w_id = created["id"]
    r = client.get(f"/api/workouts/{w_id}")
    assert r.status_code == 200
    assert r.get_json()["workout"] == "Dance"

def test_get_workout_not_found(client):
    r = client.get("/api/workouts/9999")
    assert r.status_code == 404

# ---------- Delete ----------
def test_delete_workout_valid(client):
    created = client.post("/api/workouts", json={"workout": "Boxing", "duration": 20}).get_json()
    w_id = created["id"]
    r = client.delete(f"/api/workouts/{w_id}")
    assert r.status_code == 204
    r2 = client.get(f"/api/workouts/{w_id}")
    assert r2.status_code == 404

def test_delete_workout_not_found(client):
    r = client.delete("/api/workouts/9999")
    assert r.status_code == 404

# ---------- Model-level Tests ----------
def test_workout_model_to_dict(db):
    w = Workout(workout="Pilates", duration=50)
    db.session.add(w)
    db.session.commit()
    d = w.to_dict()
    assert d["workout"] == "Pilates"
    assert isinstance(d["created_at"], str)
    assert "id" in d
