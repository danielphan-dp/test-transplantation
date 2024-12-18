import flask
import pytest

def test_get_value_from_session():
    app = flask.Flask(__name__)
    app.testing = True
    app.secret_key = 'test_secret'

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

    # Test setting and getting a string value
    c.get('/set/test_value')
    response = c.get('/get')
    assert response.data == b'test_value'

    # Test setting and getting an integer value
    c.get('/set/123')
    response = c.get('/get')
    assert response.data == b'123'

    # Test setting and getting a None value
    c.get('/set/None')
    response = c.get('/get')
    assert response.data == b'None'