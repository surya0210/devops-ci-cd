from datetime import datetime
from app import db

class Workout(db.Model):
    __tablename__ = "workouts"

    id = db.Column(db.Integer, primary_key=True)
    workout = db.Column(db.String(120), nullable=False)
    duration = db.Column(db.Integer, nullable=False)  # minutes
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "workout": self.workout,
            "duration": self.duration,
            "created_at": self.created_at.isoformat()
        }
