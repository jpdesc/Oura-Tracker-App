import pytest
from ouraapp.calendar.helpers import get_db_events
from ouraapp.models import Day
from ouraapp.calendar.models import Events


def test_get_events(loaded_login):
    events = get_db_events()
    all_days = Day.query.order_by(Day.id).all()
    for day in all_days:
        day_events = Events.query.filter_by(id=day.id).all()
        assert len(day_events) <= 2  # Check for duplicate events
    assert events
    assert len(events) > 100
