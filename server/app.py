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