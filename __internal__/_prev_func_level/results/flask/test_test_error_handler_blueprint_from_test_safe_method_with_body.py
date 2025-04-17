import flask
import pytest

@pytest.fixture
def app():
    app = flask.Flask(__name__)
    app.secret_key = 'test_secret'
    with app.app_context():
        yield app

@app.route('/set/<value>')
def set_value(value):
    flask.session['value'] = value
    return "Value set"

def test_get_value_from_session(app):
    client = app.test_client()
    client.get('/set/test_value')
    response = client.get('/get')
    assert response.data == b'test_value'

def test_get_value_not_set(app):
    client = app.test_client()
    response = client.get('/get')
    assert response.data == b'None'

def test_get_value_after_clear(app):
    client = app.test_client()
    client.get('/set/test_value')
    with client.session_transaction() as session:
        session.clear()
    response = client.get('/get')
    assert response.data == b'None'