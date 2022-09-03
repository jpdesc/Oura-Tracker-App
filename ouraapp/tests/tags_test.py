from ouraapp import app
import pytest


def test_get_tags():
    added_tags = 'alcohol'
    assert app.get_tags(added_tags, '') == ['alcohol']
    added_tags = 'Alcohol, COld, heat'
    assert app.get_tags(added_tags, '') == ['alcohol', 'cold', 'heat']
    selected_tags = ''
    added_tags = 'alcohol, cold, heat'
    assert app.get_tags(added_tags,
                        selected_tags) == ['alcohol', 'cold', 'heat']
    added_tags = 'early rise'
    selected_tags = ''
    assert app.get_tags(added_tags, selected_tags) == ['early rise']
    selected_tags = ['hot dogs', 'bananas', 'strawbeRRies']
    added_tags = 'early rise'
    assert app.get_tags(added_tags, selected_tags) == [
        'early rise', 'hot dogs', 'bananas', 'strawbeRRies'
    ]
    selected_tags = ['dogs']
    added_tags = None
    assert app.get_tags(added_tags, selected_tags) == ['dogs']
