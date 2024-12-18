import pytest
import flask

@pytest.fixture
def app():
    app = flask.Flask(__name__)
    app.secret_key = 'test_secret'
    with app.app_context():
        yield app

@app.route('/set/<value>')
def set_value(value):
    flask.session['value'] = value
    return "Value set"

def test_get_value_none(app):
    c = app.test_client()
    response = c.get('/get')
    assert response.data == b'None'

def test_get_value_set(app):
    c = app.test_client()
    c.get('/set/test_value')
    response = c.get('/get')
    assert response.data == b'test_value'

def test_get_value_empty_string(app):
    c = app.test_client()
    c.get('/set/')
    response = c.get('/get')
    assert response.data == b''

def test_get_value_after_clear(app):
    c = app.test_client()
    c.get('/set/test_value')
    with app.app_context():
        flask.session.clear()
    response = c.get('/get')
    assert response.data == b'None'