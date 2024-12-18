import pytest
import flask
from blueprintapp.app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_get_value_none(client):
    response = client.get('/get')
    assert response.data == b'None'

def test_get_value_set(client):
    with app.app_context():
        flask.session['value'] = 'test_value'
    response = client.get('/get')
    assert response.data == b'test_value'

def test_get_value_empty_string(client):
    with app.app_context():
        flask.session['value'] = ''
    response = client.get('/get')
    assert response.data == b''

def test_get_value_special_characters(client):
    with app.app_context():
        flask.session['value'] = 'value_with_special_chars_!@#$%^&*()'
    response = client.get('/get')
    assert response.data == b'value_with_special_chars_!@#$%^&*()'