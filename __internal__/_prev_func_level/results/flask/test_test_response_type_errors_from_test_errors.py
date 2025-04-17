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

    c = app.test_client()

    # Test default session value
    response = c.get('/get')
    assert response.data.decode() == 'None'

    # Test setting a value in the session
    c.get('/set/test_value')
    response = c.get('/get')
    assert response.data.decode() == 'test_value'

    # Test setting a different value in the session
    c.get('/set/another_value')
    response = c.get('/get')
    assert response.data.decode() == 'another_value'

    # Test session with no value set
    with c.session_transaction() as sess:
        sess.clear()
    response = c.get('/get')
    assert response.data.decode() == 'None'