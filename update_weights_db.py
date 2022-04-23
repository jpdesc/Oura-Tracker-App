from app import Workout, db
from datetime import date, datetime


# one = Workout(id=100, type="Weights", workout_id = 2, workout_week=1)
# two = Workout(id=102, type="Weights", workout_id = 3, workout_week=1)
# three = Workout(id=103, type="Weights", workout_id = 4, workout_week=1)
# # four = Workout(id=104, type="Weights", workout_id = 1, workout_week=2)
# # five = Workout(id=107, type="Weights", workout_id = 2, workout_week=2)
# # six = Workout(id=100, type="Weights", workout_id = 3, workout_week=2)

# weights = one, two, three
# # , four, five, six
# for elem in weights:
#     db.session.add(elem)
# db.session.commit()

workouts = Workout.query.filter(Workout.type=='Weights', Workout.date==None).all()
for workout in workouts:
    if workout.id == 100:
        workout.date = datetime.strptime("2022-04-11", '%Y-%m-%d')
    elif workout.id == 102:
        workout.date = datetime.strptime("2022-04-13", '%Y-%m-%d')
    else:
        workout.date = datetime.strptime("2022-04-14", '%Y-%m-%d')
    db.session.add(workout)
db.session.commit()
