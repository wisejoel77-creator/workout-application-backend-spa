#app.py imports
from flask import Flask, request, jsonify
from flask_migrate import Migrate

from models import db, Workout, Excercise, WorkoutExercise
from schemas import (workout_schema, workouts_schema,
    exercise_schema, exercises_schema,
    workout_exercise_schema
)

app = Flask(__name__)
 