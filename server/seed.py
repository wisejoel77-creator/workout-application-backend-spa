from datetime import date

from app import app
from config import db
from models import Workout, Exercise, WorkoutExercise

with app.app_context():

    # Clear existing data
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()

    # Exercises
    pushups = Exercise(name="Push Ups",
        category="Chest", equipment_needed=False)

    squats = Exercise(name="Squats",
        category="Legs",equipment_needed=False)

    pullups = Exercise(name="Pull Ups",
        category="Back",equipment_needed=True)

    db.session.add_all([pushups, squats,pullups])
    db.session.commit()

    # Workouts
    workout1 = Workout(date=date(2026, 7, 30),
        duration_minutes=60,
        notes="Upper body strength")

    workout2 = Workout(date=date(2026, 7, 31),
        duration_minutes=45,notes="Leg day" )

    db.session.add_all([ workout1,workout2])
    db.session.commit()

    # workout exercises
    we1 = WorkoutExercise(workout=workout1,
        exercise=pushups,sets=4,reps=15,
        duration_seconds=60)

    we2 = WorkoutExercise(workout=workout1,
        exercise=pullups,sets=3,reps=10,
        duration_seconds=90)

    we3 = WorkoutExercise(workout=workout2,
        exercise=squats,sets=5,reps=12,
        duration_seconds=75)

    db.session.add_all([we1,we2, we3])
    db.session.commit()

    print("Database seeded successfully!")