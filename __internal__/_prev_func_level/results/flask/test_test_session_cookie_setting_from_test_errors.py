import flask
import pytest

def test_get_session_value(app):
    @app.route("/set_value")
    def set_value():
        flask.session['value'] = 'test_value'
        return "Value set"

    @app.route("/get_value")
    def get_value():
        return flask.session.get('value', 'None')

    with app.test_client() as c:
        # Test default session value
        rv = c.get("/get_value")
        assert rv.data == b'None'

        # Set session value
        c.get("/set_value")

        # Test session value after setting
        rv = c.get("/get_value")
        assert rv.data == b'test_value'

        # Clear session and test again
        with flask.session_transaction() as sess:
            sess.clear()
        
        rv = c.get("/get_value")
        assert rv.data == b'None'