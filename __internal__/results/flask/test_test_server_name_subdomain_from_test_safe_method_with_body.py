import flask
import pytest

@pytest.fixture
def client():
    app = flask.Flask(__name__)
    with app.test_client() as client:
        yield client

@app.route('/get')
def get():
    v = flask.session.get('value', 'None')
    return v

def test_get_with_no_session_value(client):
    rv = client.get('/get')
    assert rv.data == b'None'

def test_get_with_session_value(client):
    with client.session_transaction() as session:
        session['value'] = 'test_value'
    rv = client.get('/get')
    assert rv.data == b'test_value'

def test_get_with_empty_session(client):
    with client.session_transaction() as session:
        session.clear()
    rv = client.get('/get')
    assert rv.data == b'None'

def test_get_with_none_session_value(client):
    with client.session_transaction() as session:
        session['value'] = None
    rv = client.get('/get')
    assert rv.data == b'None'