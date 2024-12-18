import flask
import pytest

def test_get_value_from_session():
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

    with app.test_request_context():
        # Test default value when session is empty
        response = client.get('/get')
        assert response.data == b'None'

    with app.test_request_context():
        # Test setting a value in the session
        client.get('/set/test_value')
        response = client.get('/get')
        assert response.data == b'test_value'

    with app.test_request_context():
        # Test setting another value in the session
        client.get('/set/another_value')
        response = client.get('/get')
        assert response.data == b'another_value'

    with app.test_request_context():
        # Test clearing the session
        with flask.session_transaction() as session:
            session.clear()
        response = client.get('/get')
        assert response.data == b'None'