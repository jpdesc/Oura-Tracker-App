from tkinter import W
from app import Weights, Workout, db
from datetime import date, datetime
from weights_data import get_weights_data


# one = Workout(id=100, type="Weights", workout_id = 2, workout_week=1)
# two = Workout(id=102, type="Weights", workout_id = 3, workout_week=1)
# three = Workout(id=103, type="Weights", workout_id = 4, workout_week=1)
# # four = Workout(id=104, type="Weights", workout_id = 1, workout_week=2)
# # five = Workout(id=107, type="Weights", workout_id = 2, workout_week=2)
# # six = Workout(id=100, type="Weights", workout_id = 3, workout_week=2)



# for i in range(114,131):
#     weights = Weights.query.order_by(Weights.id).all()
#     db.session.add(weights)
# db.session.commit()


weights = Weights.query.order_by(Weights.id).all()
# # print(weights)
for weight in weights:
# weights.exercises[1] = "BB Incline Bench"
# db.session.add(weights)
# db.session.commit()
# for weight in weights:
    # print(weight.exercises==None)
    # print(type(weight.exercises))
    # for entry in weight.exercises:
    #     print(entry==None)
    #     print(entry)
    # print(weight.id, weight.workout_id, weight.workout_week, weight.exercises, weight.weight)
#     weight.exercises = []
#     weight.set_ranges = []
#     weight.reps = []
#     weight.weight = []
#     db.session.add(weight)
# db.session.commit()
    get_weights_data(weight.workout_id, weight.workout_week, weight.id)

# deleted_objects = Weights.__table__.delete().where(Weights.id.in_([114, 115, 116, 117, 118, 119, 120]))
# db.session.execute(deleted_objects)
# db.session.commit()
#     get_weights_data(workout.workout_id, workout.workout_week)
# for workout in workouts:
#     weights = Weights(id = workout.id, workout_id = workout.workout_id, workout_week = workout.workout_week)
#     db.session.add(weights)
# db.session.commit()

