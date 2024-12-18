import flask
import pytest

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_value_none(client):
    response = client.get('/get')
    assert response.data == b'None'

def test_get_value_set(client, app):
    with app.app_context():
        flask.session['value'] = 'test_value'
    response = client.get('/get')
    assert response.data == b'test_value'

def test_get_value_after_clear(client, app):
    with app.app_context():
        flask.session['value'] = 'test_value'
        flask.session.clear()
    response = client.get('/get')
    assert response.data == b'None'

def test_get_value_with_different_session(client, app):
    with app.app_context():
        flask.session['value'] = 'session_value'
    response = client.get('/get')
    assert response.data == b'session_value'

def test_get_value_multiple_requests(client, app):
    with app.app_context():
        flask.session['value'] = 'first_value'
    response1 = client.get('/get')
    assert response1.data == b'first_value'
    
    with app.app_context():
        flask.session['value'] = 'second_value'
    response2 = client.get('/get')
    assert response2.data == b'second_value'