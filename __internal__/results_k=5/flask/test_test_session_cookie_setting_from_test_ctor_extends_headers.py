import flask
import pytest

def test_get_session_value(app):
    @app.route("/set")
    def set_value():
        flask.session['value'] = 'test_value'
        return "Value set"

    @app.route("/clear")
    def clear_value():
        flask.session.pop('value', None)
        return "Value cleared"

    with app.test_client() as c:
        # Test setting a session value
        assert c.get("/set").data == b"Value set"
        rv = c.get("/get")
        assert rv.data == b'test_value'

        # Test getting a session value when it is not set
        c.get("/clear")
        rv = c.get("/get")
        assert rv.data == b'None'