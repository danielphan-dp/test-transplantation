import flask
import pytest

def test_get_value_from_session():
    app = flask.Flask(__name__)
    client = app.test_client()
    app.secret_key = 'test_secret'

    @app.route('/set/<value>')
    def set_value(value):
        flask.session['value'] = value
        return 'Value set'

    @app.route('/get')
    def get():
        v = flask.session.get('value', 'None')
        return v

    # Test default value when session is empty
    rv = client.get('/get')
    assert rv.data == b'None'

    # Test setting a value in the session
    client.get('/set/test_value')
    rv = client.get('/get')
    assert rv.data == b'test_value'

    # Test setting another value in the session
    client.get('/set/another_value')
    rv = client.get('/get')
    assert rv.data == b'another_value'

    # Test clearing the session
    with client.session_transaction() as session:
        session.clear()
    rv = client.get('/get')
    assert rv.data == b'None'