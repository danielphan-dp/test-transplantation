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
    response = client.get('/get')
    assert response.data == b'None'

def test_get_method_with_set_value():
    app = flask.Flask(__name__)
    app.secret_key = 'test_secret'

    @app.route('/set/<value>')
    def set_value(value):
        flask.session['value'] = value
        return 'Value set'

    @app.route('/get')
    def get():
        v = flask.session.get('value', 'None')
        return v

    client = app.test_client()
    client.get('/set/test_value')
    response = client.get('/get')
    assert response.data == b'test_value'

def test_get_method_with_no_session():
    app = flask.Flask(__name__)
    app.secret_key = 'test_secret'

    @app.route('/get')
    def get():
        v = flask.session.get('value', 'None')
        return v

    client = app.test_client()
    response = client.get('/get')
    assert response.data == b'None'

def test_get_method_with_forbidden_access():
    app = flask.Flask(__name__)
    app.secret_key = 'test_secret'

    @app.route('/get')
    def get():
        v = flask.session.get('value', 'None')
        return v

    @app.errorhandler(Forbidden)
    def forbidden_handler(e):
        return "forbidden", 403

    client = app.test_client()
    with pytest.raises(Forbidden):
        client.get('/get', follow_redirects=False)