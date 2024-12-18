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
        return "Value Set"

    @app.route("/clear")
    def clear_value():
        flask.session.pop('value', None)
        return "Value Cleared"

    # Test setting a session value
    rv = client.get("/set", "http://www.example.com:8080/test/")
    assert rv.data == b"Value Set"

    # Test getting the session value
    rv = client.get("/get", "http://www.example.com:8080/test/")
    assert rv.data == b'test_value'

    # Test clearing the session value
    rv = client.get("/clear", "http://www.example.com:8080/test/")
    assert rv.data == b"Value Cleared"

    # Test getting the session value after clearing
    rv = client.get("/get", "http://www.example.com:8080/test/")
    assert rv.data == b'None'