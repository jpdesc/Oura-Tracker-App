from ouraapp.api import bp
from flask import request, abort
from ouraapp.weights.models import Weights, Exercise
from ouraapp.extensions import db
from flask_login import current_user


@bp.route('/api/data/<page_id>')
def data(page_id):
    query = Weights.query.filter_by(user_id=current_user.id,
                                    day_id=page_id).first()

    # # search filter
    # search = request.args.get('search')
    # if search:
    #     query = query.filter(
    #         db.or_(User.name.like(f'%{search}%'),
    #                User.email.like(f'%{search}%')))
    # total = query.count()

    # # sorting
    # sort = request.args.get('sort')
    # if sort:
    #     order = []
    #     for s in sort.split(','):
    #         direction = s[0]
    #         name = s[1:]
    #         if name not in ['name', 'age', 'email']:
    #             name = 'name'
    #         col = getattr(User, name)
    #         if direction == '-':
    #             col = col.desc()
    #         order.append(col)
    #     if order:
    #         query = query.order_by(*order)

    # # pagination
    # start = request.args.get('start', type=int, default=-1)
    # length = request.args.get('length', type=int, default=-1)
    # if start != -1 and length != -1:
    #     query = query.offset(start).limit(length)

    # response
    return {
        'data': [exercise.to_dict() for exercise in query.exercises],
    }


@bp.route('/api/data/<page_id>', methods=['POST'])
def update(page_id):
    data = request.get_json()
    print(f'data = {data}')
    if 'id' not in data:
        abort(400)
    exercise = Exercise.query.get(data['id'])
    print(f'exercise {exercise.exercise_name}')
    for field in ['exercise', 'sets', 'rep_range', 'reps', 'weight']:
        if field in data:
            print(f'field= {field}')
            print(data[field])
            setattr(exercise, field, data[field])
    db.session.commit()
    print()
    return '', 204
