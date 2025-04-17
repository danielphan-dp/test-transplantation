import pytest
import flask

def test_get_method_with_session_value(app, client):
    @app.route('/set/<value>')
    def set_value(value):
        flask.session['value'] = value
        return 'Value set'

    @app.route('/get')
    def get():
        v = flask.session.get('value', 'None')
        return v

    client.get('/set/test_value')
    response = client.get('/get')
    assert response.data == b'test_value'

def test_get_method_with_no_session_value(app, client):
    @app.route('/get')
    def get():
        v = flask.session.get('value', 'None')
        return v

    response = client.get('/get')
    assert response.data == b'None'

def test_get_method_with_empty_session_value(app, client):
    @app.route('/set/empty')
    def set_empty():
        flask.session['value'] = ''
        return 'Empty value set'

    @app.route('/get')
    def get():
        v = flask.session.get('value', 'None')
        return v

    client.get('/set/empty')
    response = client.get('/get')
    assert response.data == b''