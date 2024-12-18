import flask
import pytest

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_value_none(client, app):
    response = client.get('/get')
    assert response.data.decode() == 'None'

def test_get_value_set(client, app):
    with app.app_context():
        flask.session['value'] = 'Test Value'
    response = client.get('/get')
    assert response.data.decode() == 'Test Value'

def test_get_value_empty_string(client, app):
    with app.app_context():
        flask.session['value'] = ''
    response = client.get('/get')
    assert response.data.decode() == ''

def test_get_value_special_characters(client, app):
    with app.app_context():
        flask.session['value'] = 'Special@#Value!'
    response = client.get('/get')
    assert response.data.decode() == 'Special@#Value!'