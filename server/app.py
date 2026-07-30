#app.py imports
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from datetime import datetime

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

#WORKOUT ROUTES
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
        date=datetime.strptime(data["date"], "%Y-%m-%d").date(),
        duration_minutes=data["duration_minutes"],
        notes=data.get("notes"))
        
    db.session.add(workout)
    db.session.commit()
    return workout_schema.dump(workout), 201

# Route to update a workout
@app.patch("/workouts/<int:id>")
def update_workout(id):
    workout = Workout.query.get(id)
    if workout is None:
        return jsonify({"error": "Workout not found"}), 404

    data = request.get_json()
    if "name" in data:
        workout.name = data["name"]
    if "duration_minutes" in data:
        workout.duration_minutes = data["duration_minutes"]
    if "notes" in data:
        workout.notes = data["notes"]

    db.session.commit()
    return workout_schema.dump(workout), 200

# route to delete a workout
@app.delete("/workouts/<int:id>")
def delete_workout(id):
    workout = Workout.query.get(id)

    if workout is None:
        return jsonify({"error": "Workout not found"}), 404

    db.session.delete(workout)
    db.session.commit()
    return jsonify({"message": "Workout deleted successfully"}), 200

#EXERCISE ROUTES
#Route to get all exercises
@app.get("/exercises")
def get_exercises():
    exercises = Exercise.query.all()
    return exercises_schema.dump(exercises), 200

# Route to get one exercise
@app.get("/exercises/<int:id>")
def get_exercise(id):
    exercise = Exercise.query.get(id)

    if exercise is None:
        return jsonify({"error": "Exercise not found"}), 404
    return exercise_schema.dump(exercise), 200

# Route to create an exercise
@app.post("/exercises")
def create_exercise():
    data = request.get_json()

    exercise = Exercise(name=data["name"],
        category=data["category"],
        equipment_needed=data.get("equipment_needed", False)
    )

    db.session.add(exercise)
    db.session.commit()
    return exercise_schema.dump(exercise), 201

# Route to update an existing exercise
@app.patch("/exercises/<int:id>")
def update_exercise(id):
    exercise = Exercise.query.get(id)

    if exercise is None:
        return jsonify({"error": "Exercise not found"}), 404
    data = request.get_json()

    if "name" in data:
        exercise.name = data["name"]
    if "category" in data:
        exercise.category = data["category"]
    if "equipment_needed" in data:
        exercise.equipment_needed = data["equipment_needed"]

    db.session.commit()
    return exercise_schema.dump(exercise), 200