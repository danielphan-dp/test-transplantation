import flask
import pytest

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_value_from_session(client):
    with client.session_transaction() as session:
        session['value'] = 'test_value'
    response = client.get('/get')
    assert response.data.decode() == 'test_value'

def test_get_value_not_set(client):
    response = client.get('/get')
    assert response.data.decode() == 'None'

def test_get_value_after_clear_session(client):
    with client.session_transaction() as session:
        session['value'] = 'test_value'
    with client.session_transaction() as session:
        session.clear()
    response = client.get('/get')
    assert response.data.decode() == 'None'