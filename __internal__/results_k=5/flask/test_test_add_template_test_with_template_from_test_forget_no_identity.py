import pytest
import flask

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

def test_get_session_value_none(client):
    rv = client.get('/get')
    assert rv.data == b'None'

def test_get_session_value_set(client):
    with client.session_transaction() as session:
        session['value'] = 'test_value'
    rv = client.get('/get')
    assert rv.data == b'test_value'

def test_get_session_value_empty_string(client):
    with client.session_transaction() as session:
        session['value'] = ''
    rv = client.get('/get')
    assert rv.data == b''

def test_get_session_value_nonexistent(client):
    rv = client.get('/get')
    assert rv.data == b'None'  # Ensure it defaults to 'None' if not set

def test_get_session_value_after_clear(client):
    with client.session_transaction() as session:
        session['value'] = 'test_value'
    with client.session_transaction() as session:
        session.clear()
    rv = client.get('/get')
    assert rv.data == b'None'  # Ensure it defaults to 'None' after clearing session