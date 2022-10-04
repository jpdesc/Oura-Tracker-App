from ouraapp.extensions import db


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
    template_id = db.Column(db.Integer, db.ForeignKey('template.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    base_id = db.Column(db.Integer, db.ForeignKey('base_workout.id'))
    exercises = db.relationship('Exercise', backref='weights')


class Exercise(db.Model):
    __tablename__ = 'exercise'
    id = db.Column(db.Integer, primary_key=True)
    day_id = db.Column(db.Integer)
    exercise_name = db.Column(db.String)
    sets = db.Column(db.Integer)
    rep_range = db.Column(db.String)
    reps = db.Column(db.Integer)
    reps_improve = db.Column(db.Boolean)
    weight = db.Column(db.Float)
    weight_improve = db.Column(db.Boolean)
    weights_id = db.Column(db.Integer, db.ForeignKey('weights.id'))

    def to_dict(self):
        return {
            'id': self.id,
            'exercise': self.exercise_name,
            'sets': self.sets,
            'rep_range': self.sets,
            'reps': self.reps,
            'weight': self.weight
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
