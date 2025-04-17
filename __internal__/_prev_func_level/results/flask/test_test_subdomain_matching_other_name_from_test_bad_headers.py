import flask
import pytest

@pytest.mark.parametrize('session_value, expected', [
    (None, 'None'),
    ('test_value', 'test_value'),
    ('', ''),
])
def test_get_session_value(session_value, expected):
    app = flask.Flask(__name__)
    with app.test_request_context():
        flask.session['value'] = session_value
        assert flask.session.get('value', 'None') == expected

def test_get_session_value_default():
    app = flask.Flask(__name__)
    with app.test_request_context():
        assert flask.session.get('non_existent_key', 'default_value') == 'default_value'