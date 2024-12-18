import flask
import pytest

def test_get_method_with_session(app):
    @app.route("/set")
    def set_value():
        flask.session['value'] = 'TestValue'
        return "Value Set"

    @app.route("/get")
    def get_value():
        return flask.session.get('value', 'None')

    with app.test_client() as c:
        # Test default session value
        rv = c.get("/get")
        assert rv.data == b'None'

        # Set session value and test retrieval
        c.get("/set")
        rv = c.get("/get")
        assert rv.data == b'TestValue'

        # Clear session and test retrieval
        with c.session_transaction() as sess:
            sess.clear()
        rv = c.get("/get")
        assert rv.data == b'None'