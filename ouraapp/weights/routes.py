from flask import render_template, redirect, url_for, request, flash
from .helpers import check_improvement, get_next_base_workout, clear_exercises, \
ensure_workout_log_exists, get_current_template, get_workout_id, \
get_workout_week_num, get_weights_obj, apply_toggle, delete_exercises, \
    allow_toggle_check
from .models import Weights, Template, BaseWorkout, Exercise
from ouraapp.dashboard.models import Workout
from flask_login import login_required, current_user
from .forms import TemplateForm, WorkoutForm, InitWorkoutForm, WeightsForm
import json
from ouraapp.extensions import db
import logging
from ouraapp.weights import bp

logger = logging.getLogger("ouraapp")


#TODO: Select template from past templates.
#TODO: Improve init_workout and template layouts.
#TODO: Set up so old data is integrated with new system.
#TODO: Improve layout.
@bp.route('/weights/<page_id>')
@login_required
def weights(page_id):
    this_week = Weights.query.filter_by(day_id=page_id,
                                        user_id=current_user.id).first()

    # logger.debug(f'this_week= {this_week}')
    if this_week:
        this_week_excs = Exercise.query.filter(
            Exercise.weights_id == this_week.id,
            Exercise.exercise_name != None).all()

        # logger.debug(f'this_week_excs = {this_week_excs}')

    else:
        this_week_excs = []

    empty_rows = Exercise.query.filter(Exercise.weights_id == this_week.id,
                                       Exercise.exercise_name == None).all()

    # logger.debug(f'empty_rows = {empty_rows}')

    if empty_rows:
        for row in empty_rows:
            db.session.delete(row)
        db.session.commit()

    try:
        last_week = Weights.query.filter_by(
            workout_id=this_week.workout_id,
            template_id=this_week.template.id,
            workout_week=(int(this_week.workout_week) - 1)).first()
        exercise_list = check_improvement(this_week_excs, last_week.id)
    except (AttributeError, TypeError):
        exercise_list = this_week_excs
    # for exercise in exercise_list:
    # logger.debug(f'exercise_name = {exercise.exercise_name}')

    return render_template('workout.html',
                           page_id=page_id,
                           exercise_list=exercise_list)


@bp.route('/toggle_workout/<page_id>/<toggle>',
          methods=['GET', 'POST'])
@login_required
def toggle_workout(page_id, toggle):
    weights = get_weights_obj(page_id)
    delete_exercises(weights.id)
    apply_toggle(weights, int(toggle))

    return redirect(url_for('weights.edit_weights', page_id=page_id, from_base='True'))


# @bp.route('/edit_weights', defaults={'toggle': None}, methods=['GET', 'POST'])
@bp.route('/edit_weights/from_base:<from_base>/<page_id>',
          methods=['GET', 'POST'])
@login_required
def edit_weights(page_id, from_base):
    # logger.debug(f'page_id = {page_id}')
    template = get_current_template()

    if from_base == 'True':
        from_base = True
    else:
        from_base = False

    weights = get_weights_obj(page_id)

    if weights:
        if from_base != weights.from_base:
            from_base = weights.from_base
            db.session.add(weights)
            db.session.commit()

    show_rep_range = False
    # logger.debug(f'weights_obj = {weights}')
    if not weights:
        if from_base == True:
            workout_id = get_workout_id()
            workout_week=get_workout_week_num()
            weights = Weights(day_id=page_id,
                          user_id=current_user.id,
                          template_id=template.id,
                          workout_id=workout_id,
                          workout_week=workout_week,
                          og_workout_id=workout_id,
                          og_workout_week=workout_week,
                          from_base=True)
        else:
            weights = Weights(day_id=page_id,
                                user_id=current_user.id,
                                from_base=False)
        db.session.add(weights)
        db.session.commit()

    if not weights.exercise_objs and from_base is True:
        if not weights.template_id:
            weights.template_id = template.id
            db.session.add(weights)
            db.session.commit()
        # logger.debug(
        #     f'weights.workout_id = {weights.workout_id}, weights.template_id= {weights.template_id}'
        # )
        base = get_next_base_workout(weights.workout_id, weights.template_id)
        print(base.day_num)
        # logger.debug(f'base = {base}')
        try:
            workout_params = json.loads(base.workout_params)
        except AttributeError:
            flash('You must create a base template to load from.')
            return redirect(url_for('weights.init_template', page_id=page_id))

        for entry in workout_params.values():
            if entry[0]:
                exercise = Exercise(exercise_name=entry[0],
                                    sets=entry[1],
                                    rep_range=f'{entry[2]} - {entry[3]}',
                                    weights_id=weights.id,
                                    reps='',
                                    weight='',
                                    day_id=page_id)
                db.session.add(exercise)
            if entry[2] or entry[3]:
                show_rep_range = True
            db.session.commit()

    # clear_exercises(page_id)
    workout = ensure_workout_log_exists(page_id)
    form = WeightsForm(soreness=workout.soreness, grade=workout.grade)

    return render_template('edit_workout.html',
                           form=form,
                           page_id=page_id,
                           from_base=from_base,
                           weights=weights,
                           show_rep_range=show_rep_range,
                           allow_toggle=allow_toggle_check(weights)
                           )


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
            template_id=template.id,
            user_id=current_user.id)
        db.session.add(workout_template)
        db.session.commit()
        if int(day) != template.num_days:
            return redirect(
                url_for('weights.create_template',
                        day=int(day) + 1,
                        template_name=template_name,
                        page_id=page_id))
        flash('You have created a new workout template: {template.name}')
        return redirect(url_for('dashboard.log', page_id=page_id))
    return render_template('create_template.html', form=workout_form, day=day)


@bp.route('/init_template/<page_id>', methods=['GET', 'POST'])
@login_required
def init_template(page_id):
    init_form = InitWorkoutForm()
    if init_form.validate_on_submit():
        name = init_form.name_workout_plan.data
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
        return redirect(url_for('weights.create_template', page_id=page_id, day=1,template_name=name))
    return render_template('init_template.html', init_form=init_form)
