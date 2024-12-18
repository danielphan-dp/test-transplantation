import flask
import pytest

def test_get_session_value():
    app = flask.Flask(__name__)
    app.secret_key = 'test_secret'
    client = app.test_client()

    @app.route('/set/<value>')
    def set_value(value):
        flask.session['value'] = value
        return 'Value set'

    @app.route('/get')
    def get():
        v = flask.session.get('value', 'None')
        return v

    # Test default session value
    rv = client.get('/get')
    assert rv.data == b'None'

    # Test setting and getting session value
    client.get('/set/test_value')
    rv = client.get('/get')
    assert rv.data == b'test_value'

    # Test setting session value to None
    client.get('/set/None')
    rv = client.get('/get')
    assert rv.data == b'None'

    # Test setting session value to an empty string
    client.get('/set/')
    rv = client.get('/get')
    assert rv.data == b''