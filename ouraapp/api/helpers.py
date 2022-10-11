# from ouraapp.weights.models import Weights, Exercise
# from ouraapp.extensions import db
# from flask_login import current_user

# def add_row(page_id):
#     query = Weights.query.filter_by(day_id=page_id,
#                                     user_id=current_user.id).first()
#     blank_excs = Exercise(weights_id=query.id)
#     db.session.add(blank_excs)
#     db.session.commit()
#     print('add_row')

# def remove_row(page_id):
#     query = Weights.query.filter_by(day_id=page_id,
#                                     user_id=current_user.id).first()
#     blanks = Exercise.query.filter_by(weights_id=query.id,
#                                       exercise_name=None).all()
#     if blanks:
#         print('remove_row')
#         db.session.delete(blanks[-1])
#         db.session.commit()
