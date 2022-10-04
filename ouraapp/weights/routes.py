from flask import render_template, redirect, url_for, request, flash
from .helpers import get_weights_data, get_current_template, check_improvement, get_next_base_workout
from .models import Weights, Template, BaseWorkout, Exercise
from flask_login import login_required, current_user
from .forms import TemplateForm, WorkoutForm, InitWorkoutForm
import json
from ouraapp.extensions import db
import logging
from ouraapp.weights import bp

logger = logging.getLogger("ouraapp")

#TODO: Edit weights so that it works with new base templates.
#TODO: Make page editable.
#TODO: Set up so old data is integrated with new system.
# @bp.route('/weights/<page_id>')
# @login_required
# def weights(page_id):
#     this_week = Weights.query.filter_by(day_id=page_id,
#                                         user_id=current_user.id).first()
#     try:
#         last_week = Weights.query.filter_by(
#             workout_id=this_week.workout_id,
#             template_id=this_week.template.id,
#             workout_week=(this_week.workout_week - 1)).first()
#         reps_improve, weight_improve = check_improvement(this_week, last_week)
#     except (AttributeError):
#         reps_improve, weight_improve = None, None
#     return render_template('workout.html',
#                            page_id=page_id,
#                            weights=this_week,
#                            reps_improve=reps_improve,
#                            weight_improve=weight_improve)


@bp.route('/weights/<page_id>')
@login_required
def weights(page_id):

    weights = Weights.query.filter_by(user_id=current_user.id,
                                      day_id=page_id).first()
    if not weights:
        init_weights = Weights(day_id=page_id, user_id=current_user.id)
        db.session.add(init_weights)
        db.session.commit()
        base = get_next_base_workout()
        workout_params = json.loads(base.workout_params)
        for entry in workout_params.values():
            exercise = Exercise(exercise_name=entry[0],
                                sets=entry[1],
                                rep_range=f'{entry[2]} - {entry[3]}',
                                weights_id=init_weights.id)
            db.session.add(exercise)
        db.session.commit()
    return render_template('edit_workout.html', page_id=page_id)


@bp.route('/template/<page_id>', methods=['GET', 'POST'])
@login_required
def template(page_id):
    template_form = TemplateForm()

    if request.method == "POST":
        rows = [
            template_form.day_one.data, template_form.day_two.data,
            template_form.day_three.data, template_form.day_four.data
        ]
        excs = [
            template_form.one_excs.data, template_form.two_excs.data,
            template_form.three_excs.data, template_form.four_excs.data
        ]
        template_data = Template(
            start_id=page_id,
            template_name=template_form.template_name.data,
            row_nums=rows,
            num_excs=excs,
            num_days=template_form.total_days.data,
            user_id=current_user.id)
        db.session.add(template_data)
        db.session.commit()
        current_template = get_current_template()
        get_weights_data(1, 1, page_id, current_template)
        return redirect(url_for('dashboard.log', page_id=page_id))
    return render_template('update_template.html', template_form=template_form)


@bp.route('/create_template/<template_name>/<day>/<page_id>',
          methods=['GET', 'POST'])
@login_required
def create_template(template_name, day, page_id):
    template = Template.query.filter_by(template_name=template_name,
                                        user_id=current_user.id).first()
    workout_params = {}
    workout_form = WorkoutForm()
    if workout_form.validate_on_submit():
        for i, field in enumerate(workout_form.exercise_params):
            workout_params[i + 1] = [
                field.excs.data, field.sets.data, field.reps1.data,
                field.reps2.data
            ]
        workout_template = BaseWorkout(
            workout_params=json.dumps(workout_params),
            day_num=day,
            template_id=template.id)
        db.session.add(workout_template)
        db.session.commit()
        print(template.num_days)
        if int(day) != template.num_days:
            return redirect(
                url_for('weights.create_template',
                        day=int(day) + 1,
                        template_name=template_name,
                        page_id=page_id))
        flash('You have created a new workout template: {template.name}')
        return redirect(url_for('dashboard.log', page_id=page_id))
    return render_template('create_template.html', form=workout_form)


@bp.route('/init_template/<page_id>', methods=['GET', 'POST'])
@login_required
def init_template(page_id):
    init_form = InitWorkoutForm()
    if init_form.validate_on_submit():
        name = init_form.name_workout_plan.data
        create_base = init_form.set_base.data
        days = init_form.days.data
        starting_prs = {
            'Squat': init_form.squat_pr.data,
            'Deadlift': init_form.deadlift_pr.data,
            'Bench': init_form.bench_pr.data,
            'Overhead Press': init_form.ohp_pr.data
        }
        if init_form.custom_prs:
            for field in init_form.custom_prs:
                starting_prs[
                    field.custom_pr_name.data] = field.custom_pr_weight.data
        workout_plan = Template(template_name=name,
                                num_days=days,
                                start_id=page_id,
                                starting_prs=starting_prs,
                                user_id=current_user.id)
        db.session.add(workout_plan)
        db.session.commit()
        if create_base is True:
            return redirect(
                url_for('weights.create_template',
                        day=1,
                        template_name=name,
                        page_id=page_id))
        return redirect(url_for('dashboard.log', page_id=page_id))
    return render_template('init_template.html', init_form=init_form)
