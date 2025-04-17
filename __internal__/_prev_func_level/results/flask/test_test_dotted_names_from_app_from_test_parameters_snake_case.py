import flask
import pytest

@pytest.fixture
def session_app():
    app = flask.Flask(__name__)
    app.secret_key = 'test_secret'
    with app.test_request_context():
        flask.session['value'] = 'test_value'
    return app

def test_get_value_from_session(session_app, client):
    @session_app.route('/get')
    def get():
        v = flask.session.get('value', 'None')
        return v

    response = client.get('/get')
    assert response.data == b'test_value'

def test_get_value_not_set(session_app, client):
    @session_app.route('/get')
    def get():
        v = flask.session.get('non_existent_key', 'None')
        return v

    response = client.get('/get')
    assert response.data == b'None'