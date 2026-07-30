#app.py imports
from flask import Flask, request, jsonify
from flask_migrate import Migrate

from models import db, Workout, Exercise, WorkoutExercise
from schemas import (workout_schema, workouts_schema,
    exercise_schema, exercises_schema,
    workout_exercise_schema
)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)

# Route to get all workouts
@app.get("/workouts")
def get_workouts():
    workouts = Workout.query.all()
    return workouts_schema.dump(workouts), 200

# Route to get a single workout 
@app.get("/workouts/<int:id>")
def get_workout(id):
    workout = Workout.query.get(id)
    if workout is None:
        return jsonify({"error": "Workout not found"}), 404

    return workout_schema.dump(workout), 200

# Route to create a workout
@app.post("/workouts")
def create_workout():
    data = request.get_json()

    workout = Workout(name=data["name"],
        date=data["date"], duration=data["duration"],
        notes=data["notes"] )
    

    db.session.add(workout)
    db.session.commit()
    return workout_schema.dump(workout), 201