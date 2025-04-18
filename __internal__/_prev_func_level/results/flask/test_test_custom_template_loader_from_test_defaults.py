import flask
import pytest

@pytest.fixture
def client():
    app = flask.Flask(__name__)
    app.secret_key = 'test_secret'
    
    @app.route('/get')
    def get():
        v = flask.session.get('value', 'None')
        return v

    with app.test_client() as client:
        yield client

def test_get_value_none(client):
    response = client.get('/get')
    assert response.data == b'None'

def test_get_value_set(client):
    with client.session_transaction() as session:
        session['value'] = 'test_value'
    response = client.get('/get')
    assert response.data == b'test_value'

def test_get_value_empty(client):
    with client.session_transaction() as session:
        session['value'] = ''
    response = client.get('/get')
    assert response.data == b''

def test_get_value_nonexistent(client):
    response = client.get('/get')
    assert response.data == b'None'  # Ensure it defaults to 'None' if not set

def test_get_value_after_clear(client):
    with client.session_transaction() as session:
        session['value'] = 'test_value'
    with client.session_transaction() as session:
        session.clear()
    response = client.get('/get')
    assert response.data == b'None'  # Ensure it defaults to 'None' after clearing session