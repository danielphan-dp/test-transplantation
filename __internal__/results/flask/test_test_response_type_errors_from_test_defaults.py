import flask
import pytest

def test_get_session_value():
    app = flask.Flask(__name__)
    app.secret_key = 'test_secret'
    app.testing = True

    @app.route('/set/<value>')
    def set_value(value):
        flask.session['value'] = value
        return 'Value set'

    c = app.test_client()

    # Test default session value
    response = c.get('/get')
    assert response.data == b'None'

    # Test setting and getting a session value
    c.get('/set/test_value')
    response = c.get('/get')
    assert response.data == b'test_value'

    # Test setting and getting a different session value
    c.get('/set/another_value')
    response = c.get('/get')
    assert response.data == b'another_value'

    # Test getting session value after clearing session
    with flask.session_transaction() as sess:
        sess.clear()
    response = c.get('/get')
    assert response.data == b'None'