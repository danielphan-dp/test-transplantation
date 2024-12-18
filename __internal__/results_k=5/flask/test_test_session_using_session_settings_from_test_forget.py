import flask
import pytest

def test_get_session_value(app, client):
    app.config.update(
        SERVER_NAME="www.example.com:8080",
        APPLICATION_ROOT="/test",
        SESSION_COOKIE_DOMAIN=".example.com",
        SESSION_COOKIE_HTTPONLY=False,
        SESSION_COOKIE_SECURE=True,
        SESSION_COOKIE_PARTITIONED=True,
        SESSION_COOKIE_SAMESITE="Lax",
        SESSION_COOKIE_PATH="/",
    )

    @app.route("/set")
    def set_value():
        flask.session['value'] = 'test_value'
        return "Value set"

    @app.route("/get")
    def get_value():
        return flask.session.get('value', 'None')

    rv = client.get("/set", "http://www.example.com:8080/test/")
    assert rv.data == b"Value set"

    rv = client.get("/get", "http://www.example.com:8080/test/")
    assert rv.data == b"test_value"

    flask.session.pop('value', None)
    rv = client.get("/get", "http://www.example.com:8080/test/")
    assert rv.data == b'None'

    rv = client.get("/set", "http://www.example.com:8080/test/")
    assert rv.data == b"Value set"

    rv = client.get("/get", "http://www.example.com:8080/test/")
    assert rv.data == b"test_value"