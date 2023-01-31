from ouraapp.extensions import db
from flask_login import current_user

class Weights(db.Model):
    __tablename__ = 'weights'
    id = db.Column(db.Integer, primary_key=True)
    day_id = db.Column(db.Integer)
    exercises = db.Column(db.ARRAY(db.String))
    set_ranges = db.Column(db.ARRAY(db.String))
    reps = db.Column(db.ARRAY(db.String))
    weight = db.Column(db.ARRAY(db.String))
    subbed = db.Column(db.String)
    workout_id = db.Column(db.Integer)
    workout_week = db.Column(db.Integer)
    og_workout_id = db.Column(db.Integer)
    og_workout_week = db.Column(db.Integer)
    template_id = db.Column(db.Integer, db.ForeignKey('template.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    base_id = db.Column(db.Integer, db.ForeignKey('base_workout.id'))
    exercise_objs = db.relationship('Exercise', backref='weights')
    from_base = db.Column(db.Boolean)

    def get_workout_num(self):
        return self.get_num_days() * (self.workout_week - 1) + self.workout_id

    def get_og_workout_num(self):
        return self.get_num_days() * (self.og_workout_week - 1) + self.og_workout_id

    def get_max_workout_num(self):
        return self.get_og_workout_num() + self.get_num_days() - 1

    def get_num_days(self):
        template = Template.query.filter_by(user_id=current_user.id).order_by(
                    Template.id.desc()).first()
        return template.num_days



def check_last_week_excs(exercise_name, last_week_id):
    exercise_prev = Exercise.query.filter_by(exercise_name=exercise_name,
                                             weights_id=last_week_id).first()
    return exercise_prev


def get_last_week_excs(weights_id, exercise_name):
    this_week = Weights.query.filter_by(id=weights_id).first()
    last_week = Weights.query.filter_by(
        workout_week=this_week.workout_week - 1,
        workout_id=this_week.workout_id,
        template_id=this_week.template_id).first()
    if last_week:
        exercise_prev = check_last_week_excs(exercise_name, last_week.id)
        weeks_subtract = 2
        while not exercise_prev and last_week.workout_week > 1:
            last_week = Weights.query.filter_by(
                workout_week=this_week.workout_week - weeks_subtract,
                workout_id=this_week.workout_id,
                template_id=this_week.template_id).first()
            exercise_prev = check_last_week_excs(exercise_name, last_week.id)
            weeks_subtract += 1
        return exercise_prev
    return None


def prev_excs_data(excs_obj):
    weights = Weights.query.filter_by(id=excs_obj.weights_id).first()
    if weights.from_base == True:
        exercise_prev = get_last_week_excs(excs_obj.weights_id,
                                       excs_obj.exercise_name)
        if exercise_prev:
            return f'{exercise_prev.reps} x {exercise_prev.weight}'

    return 'No previous data.'


#


class Exercise(db.Model):
    __tablename__ = 'exercise'
    id = db.Column(db.Integer, primary_key=True)
    day_id = db.Column(db.Integer)
    exercise_name = db.Column(db.String)
    sets = db.Column(db.String)
    rep_range = db.Column(db.String)
    reps = db.Column(db.String)
    reps_improve = db.Column(db.Boolean)
    weight = db.Column(db.String)
    weight_improve = db.Column(db.Boolean)
    weights_id = db.Column(db.Integer, db.ForeignKey('weights.id'))

    def to_dict(self):
        return {
            'id': self.id,
            'exercise_name': self.exercise_name,
            'sets': self.sets,
            'rep_range': self.rep_range,
            'reps': self.reps,
            'weight': self.weight,
            'last_week': prev_excs_data(self)
        }


class Template(db.Model):
    __tablename__ = 'template'
    id = db.Column(db.Integer, primary_key=True)
    start_id = db.Column(db.Integer)
    template_name = db.Column(db.String)
    num_days = db.Column(db.Integer)
    row_nums = db.Column(db.ARRAY(db.Integer))
    num_excs = db.Column(db.ARRAY(db.Integer))
    starting_prs = db.Column(db.JSON)
    current_prs = db.Column(db.JSON)
    weights = db.relationship('Weights', backref='template')
    base_workouts = db.relationship('BaseWorkout', backref='template')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class BaseWorkout(db.Model):
    __tablename__ = 'base_workout'
    id = db.Column(db.Integer, primary_key=True)
    day_num = db.Column(db.Integer)
    template_id = db.Column(db.Integer, db.ForeignKey('template.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    workout_params = db.Column(db.JSON)
    workouts = db.relationship('Weights', backref='base_workout')
