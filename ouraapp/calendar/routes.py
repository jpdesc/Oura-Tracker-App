from flask import render_template, session, redirect, url_for, request, Blueprint
from ouraapp.models import Day
from flask_login import login_required
from .helpers import get_db_events
import logging
from ouraapp.calendar import bp

logger = logging.getLogger("ouraapp")


@bp.route('/calendar', methods=['GET', 'POST'])
@login_required
def calendar():
    session['url'] = url_for('dashboard.log', page_id=None)
    return render_template('calendar.html', events=get_db_events())


@bp.route('/process', methods=['POST'])
@login_required
def process():
    ''' Used to process ajax call for calendar event clicks.
  Routes to the correct index page based on the page_id/dates.
  '''
    date_str = request.form.get('date_str')
    clicked_day_obj = Day.query.filter(Day.date_str == date_str).first()
    return redirect(url_for('dashboard.log', page_id=clicked_day_obj.id))
