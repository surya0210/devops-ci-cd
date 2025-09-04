from app.models import Workout

def test_workout_model_persists(db):
    w = Workout(workout="Cycling", duration=30)
    db.session.add(w)
    db.session.commit()

    assert w.id is not None
    found = Workout.query.first()
    assert found.workout == "Cycling"
    assert found.duration == 30
