import flask
import pytest

@pytest.fixture
def app():
    app = flask.Flask(__name__)
    app.secret_key = 'test_secret'
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@app.route('/set')
def set_value():
    flask.session['value'] = 'test_value'
    return 'Value set'

def test_get_value_from_session(client):
    client.get('/set')
    response = client.get('/get')
    assert response.data == b'test_value'

def test_get_value_not_set(client):
    response = client.get('/get')
    assert response.data == b'None'

def test_get_value_after_clear(client):
    client.get('/set')
    with client.session_transaction() as session:
        session.clear()
    response = client.get('/get')
    assert response.data == b'None'