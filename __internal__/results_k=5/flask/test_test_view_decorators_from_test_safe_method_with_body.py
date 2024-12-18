import flask
import pytest

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_value_from_session(client):
    with client.session_transaction() as session:
        session['value'] = 'Test Value'
    response = client.get('/get')
    assert response.data.decode('utf-8') == 'Test Value'

def test_get_value_from_session_default(client):
    response = client.get('/get')
    assert response.data.decode('utf-8') == 'None'

def test_get_value_from_session_empty(client):
    with client.session_transaction() as session:
        session['value'] = ''
    response = client.get('/get')
    assert response.data.decode('utf-8') == ''