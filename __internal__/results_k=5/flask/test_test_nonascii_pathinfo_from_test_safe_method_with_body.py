import flask
import pytest

@pytest.fixture
def client(app):
    return app.test_client()

@app.route('/set_value/<value>')
def set_value(value):
    flask.session['value'] = value
    return "Value set"

def test_get_value_none(client):
    rv = client.get('/get')
    assert rv.data == b'None'

def test_get_value_set(client):
    client.get('/set_value/test_value')
    rv = client.get('/get')
    assert rv.data == b'test_value'

def test_get_value_nonascii(client):
    client.get('/set_value/\xe2\x9c\x94')  # Setting a non-ASCII value
    rv = client.get('/get')
    assert rv.data == b'\xe2\x9c\x94'  # Checking if the non-ASCII value is retrieved correctly

def test_get_value_empty(client):
    client.get('/set_value/')
    rv = client.get('/get')
    assert rv.data == b''  # Checking if an empty string is handled correctly

def test_get_value_special_characters(client):
    client.get('/set_value/!@#$%^&*()')
    rv = client.get('/get')
    assert rv.data == b'!@#$%^&*()'  # Checking if special characters are handled correctly