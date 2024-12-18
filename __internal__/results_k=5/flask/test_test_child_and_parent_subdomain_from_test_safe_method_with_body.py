import flask
import pytest

@pytest.fixture
def app():
    app = flask.Flask(__name__)
    app.secret_key = 'test_secret'
    return app

def test_get_value_from_session(app, client):
    with app.test_request_context():
        flask.session['value'] = 'test_value'
        response = client.get('/get')
        assert response.data.decode() == 'test_value'

def test_get_value_not_set(app, client):
    with app.test_request_context():
        response = client.get('/get')
        assert response.data.decode() == 'None'

def test_get_value_after_clear_session(app, client):
    with app.test_request_context():
        flask.session['value'] = 'test_value'
        flask.session.clear()
        response = client.get('/get')
        assert response.data.decode() == 'None'