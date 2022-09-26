from ouraapp.extensions import db


class Weights(db.Model):
    __tablename__ = 'weights'
    id = db.Column(db.Integer, primary_key=True)
    exercises = db.Column(db.ARRAY(db.String))
    set_ranges = db.Column(db.ARRAY(db.String))
    reps = db.Column(db.ARRAY(db.String))
    weight = db.Column(db.ARRAY(db.String))
    subbed = db.Column(db.String)
    workout_id = db.Column(db.Integer)
    workout_week = db.Column(db.Integer)
    template_id = db.Column(db.Integer, db.ForeignKey("template.id"))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Template(db.Model):
    __tablename__ = 'template'
    id = db.Column(db.Integer, primary_key=True)
    start_id = db.Column(db.Integer)
    template_name = db.Column(db.String)
    num_days = db.Column(db.Integer)
    row_nums = db.Column(db.ARRAY(db.Integer))
    num_excs = db.Column(db.ARRAY(db.Integer))
    weights = db.relationship('Weights', backref='template')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
