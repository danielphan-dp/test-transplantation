import pytest
import flask
from flask import session

@pytest.mark.parametrize(('value', 'expected'), [
    ('test_value', 'test_value'),
    (None, 'None'),
    ('', ''),
])
def test_get_value(app, client, value, expected):
    with app.app_context():
        session['value'] = value
    response = client.get('/get')
    assert response.data.decode() == expected

def test_get_value_no_session(app, client):
    response = client.get('/get')
    assert response.data.decode() == 'None'