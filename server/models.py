from config import db
from sqlalchemy.orm import validates

# Exercise model
class Exercise(db.Model):
    __tablename__ = "exercises"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    category = db.Column(db.String(100), nullable=False)
    equipment_needed = db.Column(db.Boolean, default=False)

    workout_exercises = db.relationship("WorkoutExercise", back_populates="exercise", cascade="all, delete-orphan")
# overlaps  tells SQLAlchemy that two relationships share some of the same columns so it shouldn't issue warnings about them.
    workout = db.relationship("Workout",secondary="workout_exercises", back_populates="exercises", overlaps="workout_exercises,workout")

    @validates("name")
    def validate_name(self, key, value):
        if len(value) < 3:
            raise ValueError("Exercise name must be at least 3 characters.")
        return value

# workout model
class Workout(db.Model):

    __tablename__ = "workouts"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)

    workout_exercises = db.relationship("WorkoutExercise", back_populates="workout",cascade="all, delete-orphan")
    exercises = db.relationship("Exercise", secondary="workout_exercises", back_populates="workouts", overlaps="workout_exercises,exercise")

    @validates("duration_minutes")
    def validate_duration(self, key, value):
        if value <= 0:
            raise ValueError("Workout duration must be greater than zero.")
        return value

# workout excercise model
class WorkoutExercise(db.Model):

    __tablename__ = "workout_exercises"

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column( db.Integer,db.ForeignKey("workouts.id"),nullable=False)
    exercise_id = db.Column(db.Integer,db.ForeignKey("exercises.id"),nullable=False)

    reps = db.Column(db.Integer, nullable=False)
    sets = db.Column(db.Integer, nullable=False)
    duration_seconds = db.Column(db.Integer, nullable=False)

    workout = db.relationship("Workout",back_populates="workout_exercises")
    exercise = db.relationship("Exercise",back_populates="workout_exercises")

    @validates("sets")
    def validate_sets(self, key, value):
        if value is not None and value < 1:
            raise ValueError("Sets must be at least 1.")
        return value

    @validates("reps")
    def validate_reps(self, key, value):
        if value is not None and value < 1:
            raise ValueError("Reps must be at least 1.")
        return value