import flask
import pytest

def test_get_value_from_session(app, client):
    @app.route('/set/<value>')
    def set_value(value):
        flask.session['value'] = value
        return "Value set"

    @app.route('/get')
    def get():
        v = flask.session.get('value', 'None')
        return v

    client.get('/set/test_value')
    response = client.get('/get')
    assert response.data == b'test_value'

def test_get_value_not_set(app, client):
    @app.route('/get')
    def get():
        v = flask.session.get('value', 'None')
        return v

    response = client.get('/get')
    assert response.data == b'None'

def test_get_value_with_none_default(app, client):
    @app.route('/get')
    def get():
        v = flask.session.get('value', None)
        return str(v)

    response = client.get('/get')
    assert response.data == b'None'