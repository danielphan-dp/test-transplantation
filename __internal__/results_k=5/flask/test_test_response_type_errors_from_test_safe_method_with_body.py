import flask
import pytest

def test_get_method_with_session_value():
    app = flask.Flask(__name__)
    app.testing = True

    @app.route('/set/<value>')
    def set_value(value):
        flask.session['value'] = value
        return 'Value set'

    @app.route('/get')
    def get():
        v = flask.session.get('value', 'None')
        return v

    c = app.test_client()

    # Test default session value
    response = c.get('/get')
    assert response.data == b'None'

    # Test setting and getting a session value
    c.get('/set/test_value')
    response = c.get('/get')
    assert response.data == b'test_value'

    # Test setting and getting another session value
    c.get('/set/another_value')
    response = c.get('/get')
    assert response.data == b'another_value'

def test_get_method_with_no_session_value():
    app = flask.Flask(__name__)
    app.testing = True

    @app.route('/get')
    def get():
        v = flask.session.get('value', 'None')
        return v

    c = app.test_client()

    # Test getting value when session is empty
    response = c.get('/get')
    assert response.data == b'None'