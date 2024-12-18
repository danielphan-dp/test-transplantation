import flask
import pytest

@pytest.fixture
def client(app):
    return app.test_client()

@app.route('/set_value/<value>')
def set_value(value):
    flask.session['value'] = value
    return "Value set"

def test_get_value_from_session(client):
    client.get('/set_value/test_value')
    response = client.get('/get')
    assert response.data == b'test_value'

def test_get_value_from_empty_session(client):
    response = client.get('/get')
    assert response.data == b'None'

def test_get_value_after_session_clear(client):
    client.get('/set_value/test_value')
    with client.session_transaction() as session:
        session.clear()
    response = client.get('/get')
    assert response.data == b'None'