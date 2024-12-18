import flask
import pytest

@pytest.fixture
def client(app):
    return app.test_client()

@app.route('/set_value/<value>')
def set_value(value):
    flask.session['value'] = value
    return "Value set!"

def test_get_value_none(client):
    response = client.get('/get')
    assert response.data == b'None'

def test_get_value_set(client):
    client.get('/set_value/test_value')
    response = client.get('/get')
    assert response.data == b'test_value'

def test_get_value_empty_string(client):
    client.get('/set_value/')
    response = client.get('/get')
    assert response.data == b''

def test_get_value_special_characters(client):
    client.get('/set_value/!@#$%^&*()')
    response = client.get('/get')
    assert response.data == b'!@#$%^&*()'