import flask
import pytest

@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client

def test_get_session_value_none(client):
    response = client.get('/get')
    assert response.data.decode() == 'None'

def test_get_session_value_set(client):
    @app.route('/set_value')
    def set_value():
        flask.session['value'] = 'test_value'
        return ''
    
    client.get('/set_value')
    response = client.get('/get')
    assert response.data.decode() == 'test_value'

def test_get_session_value_after_clear(client):
    @app.route('/set_value')
    def set_value():
        flask.session['value'] = 'test_value'
        return ''
    
    client.get('/set_value')
    client.get('/clear')
    response = client.get('/get')
    assert response.data.decode() == 'None'

def test_get_session_value_default(client):
    @app.route('/set_default_value')
    def set_default_value():
        flask.session.setdefault('value', 'default_value')
        return ''
    
    client.get('/set_default_value')
    response = client.get('/get')
    assert response.data.decode() == 'default_value'