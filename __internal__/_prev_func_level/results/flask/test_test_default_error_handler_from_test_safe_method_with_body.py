import flask
import pytest
from werkzeug.exceptions import HTTPException, NotFound, Forbidden

def test_get_method_with_default_value():
    app = flask.Flask(__name__)
    app.secret_key = 'test_secret'

    @app.route('/get')
    def get():
        v = flask.session.get('value', 'None')
        return v

    client = app.test_client()

    # Test default value when session is empty
    response = client.get('/get')
    assert response.data == b'None'

def test_get_method_with_session_value():
    app = flask.Flask(__name__)
    app.secret_key = 'test_secret'

    @app.route('/get')
    def get():
        v = flask.session.get('value', 'None')
        return v

    client = app.test_client()

    # Set session value
    with client.session_transaction() as session:
        session['value'] = 'test_value'

    # Test when session has a value
    response = client.get('/get')
    assert response.data == b'test_value'

def test_get_method_with_nonexistent_session_key():
    app = flask.Flask(__name__)
    app.secret_key = 'test_secret'

    @app.route('/get')
    def get():
        v = flask.session.get('value', 'None')
        return v

    client = app.test_client()

    # Test when session key does not exist
    with client.session_transaction() as session:
        session.clear()  # Ensure session is empty

    response = client.get('/get')
    assert response.data == b'None'