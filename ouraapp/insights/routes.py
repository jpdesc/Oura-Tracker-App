from flask import render_template, request
from .helpers import get_overall_averages, get_filters, get_date_range, get_filtered_avgs
from flask_login import login_required, current_user
from .forms import FilterForm
from ouraapp.dashboard.models import Sleep
import logging
from ouraapp.insights import bp

logger = logging.getLogger("ouraapp")


@bp.route('/insights', methods=['GET', 'POST'])
@login_required
def insights():
    filter_form = FilterForm()
    averages = get_overall_averages()
    total_days = len(
        Sleep.query.filter(Sleep.user_id == current_user.id).order_by(
            Sleep.id).all())
    filter_objs, filter_avgs, filtered_days = None, None, None
    if request.method == "POST":
        print(filter_form)
        date_range = get_date_range(filter_form)
        filter_objs = get_filters(filter_form, date_range)
        print(f'filter_objs: {filter_objs}')
        filter_avgs = get_filtered_avgs(filter_objs)

        print(f'filter_avgs: {filter_avgs}')
        filtered_days = len(filter_objs)
    return render_template('insights.html',
                           averages=averages,
                           filter_form=filter_form,
                           filter_objs=filter_objs,
                           filter_avgs=filter_avgs,
                           filtered_days=filtered_days,
                           total_days=total_days)
