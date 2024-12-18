import flask
import pytest

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_with_default_value(client):
    response = client.get('/get')
    assert response.data == b'None'

def test_get_with_session_value(client):
    with client.session_transaction() as session:
        session['value'] = 'test_value'
    response = client.get('/get')
    assert response.data == b'test_value'

def test_get_with_empty_session(client):
    with client.session_transaction() as session:
        session.clear()
    response = client.get('/get')
    assert response.data == b'None'