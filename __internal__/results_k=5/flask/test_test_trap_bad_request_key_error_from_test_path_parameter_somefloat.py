import pytest
import flask
from werkzeug.exceptions import BadRequest

@pytest.mark.parametrize('session_value, expected_response', [
    (None, b'None'),
    ('test_value', b'test_value'),
    ('', b''),
])
def test_get_value_from_session(app, client, session_value, expected_response):
    with app.app_context():
        flask.session['value'] = session_value
    rv = client.get('/get')
    assert rv.data == expected_response

def test_get_value_from_session_no_value(app, client):
    with app.app_context():
        flask.session.clear()
    rv = client.get('/get')
    assert rv.data == b'None'