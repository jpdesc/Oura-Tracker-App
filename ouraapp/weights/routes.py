from flask import render_template, redirect, url_for, request
from .helpers import get_weights_data, get_current_template, check_improvement
from .models import Weights, Template
from flask_login import login_required, current_user
from .forms import TemplateForm
from ouraapp.extensions import db
import logging
from ouraapp.weights import bp

logger = logging.getLogger("ouraapp")


@bp.route('/weights/<page_id>')
@login_required
def weights(page_id):
    this_week = Weights.query.filter_by(id=page_id,
                                        user_id=current_user.id).first()
    try:
        last_week = Weights.query.filter_by(
            workout_id=this_week.workout_id,
            template_id=this_week.template.id,
            workout_week=(this_week.workout_week - 1)).first()
        reps_improve, weight_improve = check_improvement(this_week, last_week)
    except (AttributeError):
        reps_improve, weight_improve = None, None
    return render_template('workout.html',
                           page_id=page_id,
                           weights=this_week,
                           reps_improve=reps_improve,
                           weight_improve=weight_improve)


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
