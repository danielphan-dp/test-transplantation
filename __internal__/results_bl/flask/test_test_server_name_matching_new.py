import flask
import pytest

@pytest.mark.parametrize(('session_value', 'expected'), [
    (None, 'None'),
    ('test_value', 'test_value'),
    ('', ''),
])
def test_get(session_value, expected):
    app = flask.Flask(__name__)
    with app.test_request_context():
        flask.session['value'] = session_value
        assert app.view_functions['get']() == expected

def test_get_no_session_value():
    app = flask.Flask(__name__)
    with app.test_request_context():
        assert app.view_functions['get']() == 'None'