import flask
import pytest

@pytest.fixture
def client(app):
    return app.test_client()

@app.route('/set_value')
def set_value():
    flask.session['value'] = 'test_value'
    return ''

def test_get_value_from_session(client):
    client.get('/set_value')
    response = client.get('/get')
    assert response.data.decode() == 'test_value'

def test_get_value_no_session(client):
    response = client.get('/get')
    assert response.data.decode() == 'None'

def test_get_value_after_session_clear(client):
    client.get('/set_value')
    with client.session_transaction() as session:
        session.clear()
    response = client.get('/get')
    assert response.data.decode() == 'None'

def test_get_value_with_different_session(client):
    client.get('/set_value')
    with client.session_transaction() as session:
        session['value'] = 'new_value'
    response = client.get('/get')
    assert response.data.decode() == 'new_value'