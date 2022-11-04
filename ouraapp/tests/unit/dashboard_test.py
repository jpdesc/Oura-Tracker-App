from ouraapp.dashboard.helpers import get_tags
import pytest


def test_get_tags():
    added_tags = 'alcohol'
    assert get_tags(added_tags, '') == ['alcohol']
    added_tags = 'Alcohol, COld, heat'
    assert get_tags(added_tags, '') == ['alcohol', 'cold', 'heat']
    selected_tags = ''
    added_tags = 'alcohol, cold, heat'
    assert get_tags(added_tags, selected_tags) == ['alcohol', 'cold', 'heat']
    added_tags = 'early rise'
    selected_tags = ''
    assert get_tags(added_tags, selected_tags) == ['early rise']
    selected_tags = ['hot dogs', 'bananas', 'strawbeRRies']
    added_tags = 'early rise'
    assert get_tags(added_tags, selected_tags) == [
        'early rise', 'hot dogs', 'bananas', 'strawbeRRies'
    ]
    selected_tags = ['dogs']
    added_tags = None
    assert get_tags(added_tags, selected_tags) == ['dogs']
