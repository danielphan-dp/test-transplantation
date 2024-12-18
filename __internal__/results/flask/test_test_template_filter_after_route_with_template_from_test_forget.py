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

def test_get_value_in_session(client):
    with client.session_transaction() as session:
        session['value'] = 'test_value'
    rv = client.get('/get')
    assert rv.data == b'test_value'

def test_get_value_not_in_session(client):
    rv = client.get('/get')
    assert rv.data == b'None'

def test_get_value_with_none_in_session(client):
    with client.session_transaction() as session:
        session['value'] = None
    rv = client.get('/get')
    assert rv.data == b'None'