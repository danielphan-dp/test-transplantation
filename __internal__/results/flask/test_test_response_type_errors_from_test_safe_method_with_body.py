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

    # Test clearing the session
    with flask.session_transaction() as sess:
        sess.clear()
    response = c.get('/get')
    assert response.data == b'None'