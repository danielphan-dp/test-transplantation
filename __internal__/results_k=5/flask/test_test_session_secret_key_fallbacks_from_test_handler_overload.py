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

def test_get_value_from_empty_session(client):
    response = client.get('/get')
    assert response.data.decode() == 'None'

def test_get_value_after_session_reset(client):
    client.get('/set_value')
    app.secret_key = 'new test key'
    response = client.get('/get')
    assert response.data.decode() == 'None'

def test_get_value_with_fallback_secret_key(client):
    client.get('/set_value')
    app.secret_key = 'new test key'
    app.config["SECRET_KEY_FALLBACKS"] = ["test key"]
    response = client.get('/get')
    assert response.data.decode() == 'test_value'