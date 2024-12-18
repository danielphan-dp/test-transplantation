import flask
import pytest

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_value_from_session(client):
    with client.session_transaction() as session:
        session['value'] = 'Test Value'
    rv = client.get('/get')
    assert rv.data == b'Test Value'

def test_get_value_not_set(client):
    rv = client.get('/get')
    assert rv.data == b'None'

def test_get_value_with_none(client):
    with client.session_transaction() as session:
        session['value'] = None
    rv = client.get('/get')
    assert rv.data == b'None'