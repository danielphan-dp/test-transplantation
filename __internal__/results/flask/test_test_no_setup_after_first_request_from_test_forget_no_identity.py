import flask
import pytest

@pytest.fixture
def client(app):
    return app.test_client()

@app.route('/set/<value>')
def set_value(value):
    flask.session['value'] = value
    return "Value set"

def test_get_value_from_session(client):
    client.get('/set/test_value')
    response = client.get('/get')
    assert response.data == b'test_value'

def test_get_value_not_set(client):
    response = client.get('/get')
    assert response.data == b'None'

def test_get_value_after_clear(client):
    client.get('/set/test_value')
    with client.session_transaction() as session:
        session.clear()
    response = client.get('/get')
    assert response.data == b'None'