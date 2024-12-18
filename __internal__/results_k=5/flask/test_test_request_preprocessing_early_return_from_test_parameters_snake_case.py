import flask
import pytest

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_session_value(client):
    with client.session_transaction() as session:
        session['value'] = 'test_value'
    rv = client.get('/get')
    assert rv.data == b'test_value'

def test_get_session_value_default(client):
    rv = client.get('/get')
    assert rv.data == b'None'

def test_get_session_value_empty(client):
    with client.session_transaction() as session:
        session.clear()
    rv = client.get('/get')
    assert rv.data == b'None'