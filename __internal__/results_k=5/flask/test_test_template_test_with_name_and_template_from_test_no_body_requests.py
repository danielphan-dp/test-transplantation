import flask
import pytest

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_with_default_value(client):
    rv = client.get('/get')
    assert rv.data == b'None'

def test_get_with_session_value(client):
    with client.session_transaction() as session:
        session['value'] = 'Test Value'
    rv = client.get('/get')
    assert rv.data == b'Test Value'

def test_get_with_empty_session(client):
    with client.session_transaction() as session:
        session.clear()
    rv = client.get('/get')
    assert rv.data == b'None'