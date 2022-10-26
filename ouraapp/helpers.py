from .models import db, Day
from datetime import date, timedelta
from sqlalchemy import func
# from run import app


def update_days_db():
    last_id = db.session.query(func.max(Day.id)).scalar()
    if last_id:
        next_id = last_id + 1
        last_day_obj = Day.query.filter(Day.id == last_id).first()
        start_date = last_day_obj.date + timedelta(days=1)
    else:
        next_id = 0
        start_date = date(2022, 1, 1)
    added_days = [
        start_date + timedelta(days=x)
        for x in range((date.today() - start_date).days + 5)
    ]
    for i, day in enumerate(added_days, start=next_id):
        day_obj = Day()
        day_obj.id = i
        day_obj.date = day
        day_obj.date_str = day.strftime('%Y-%m-%d')
        db.session.add(day_obj)
    db.session.commit()


def get_page_id():
    # with app.app_context():
    today = date.today()
    db_obj = Day.query.filter_by(date=today).first()
    return db_obj.id


def get_date(page_id):
    day = Day.query.filter_by(day_id=page_id).first()
    return day.date
