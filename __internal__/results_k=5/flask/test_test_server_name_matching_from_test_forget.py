import flask
import pytest

@pytest.mark.parametrize("session_value, expected", [
    (None, 'None'),
    ('test_value', 'test_value'),
    ('', ''),
])
def test_get_session_value(session_value, expected):
    app = flask.Flask(__name__)
    app.secret_key = 'test_secret'
    
    with app.test_request_context():
        flask.session['value'] = session_value
        response = app.test_client().get('/get')
        assert response.data.decode() == expected

@pytest.mark.parametrize("session_value, expected", [
    ('another_value', 'another_value'),
    ('', ''),
])
def test_get_session_value_with_different_value(session_value, expected):
    app = flask.Flask(__name__)
    app.secret_key = 'test_secret'
    
    with app.test_request_context():
        flask.session['value'] = session_value
        response = app.test_client().get('/get')
        assert response.data.decode() == expected

def test_get_session_value_no_session():
    app = flask.Flask(__name__)
    app.secret_key = 'test_secret'
    
    with app.test_request_context():
        response = app.test_client().get('/get')
        assert response.data.decode() == 'None'