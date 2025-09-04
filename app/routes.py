from flask import Blueprint, jsonify, request
from app import db
from app.models import Workout

api_bp = Blueprint("api", __name__)

@api_bp.get("/health")
def health():
    return {"status": "ok"}, 200

@api_bp.post("/workouts")
def create_workout():
    data = request.get_json(silent=True) or {}
    workout = (data.get("workout") or "").strip()
    duration = data.get("duration")

    errors = {}
    if not workout:
        errors["workout"] = "Workout name is required."
    try:
        duration = int(duration)
        if duration <= 0:
            raise ValueError
    except Exception:
        errors["duration"] = "Duration must be a positive integer (minutes)."

    if errors:
        return jsonify({"errors": errors}), 400

    w = Workout(workout=workout, duration=duration)
    db.session.add(w)
    db.session.commit()
    return jsonify(w.to_dict()), 201

@api_bp.get("/workouts")
def list_workouts():
    items = Workout.query.order_by(Workout.id.asc()).all()
    return jsonify([w.to_dict() for w in items]), 200

@api_bp.get("/workouts/<int:workout_id>")
def get_workout(workout_id: int):
    w = Workout.query.get_or_404(workout_id)
    return jsonify(w.to_dict()), 200

@api_bp.delete("/workouts/<int:workout_id>")
def delete_workout(workout_id: int):
    w = Workout.query.get_or_404(workout_id)
    db.session.delete(w)
    db.session.commit()
    return "", 204
