import flask
import pytest

def test_get_session_value(app, client):
    @app.route("/set")
    def set_value():
        flask.session['value'] = 'test_value'
        return "Value set"

    @app.route("/get")
    def get_value():
        return flask.session.get('value', 'None')

    with client:
        # Test default session value
        rv = client.get("/get")
        assert rv.data == b'None'

        # Set a session value and test retrieval
        client.get("/set")
        rv = client.get("/get")
        assert rv.data == b'test_value'

        # Test session after clearing it
        with client.session_transaction() as sess:
            sess.clear()
        rv = client.get("/get")
        assert rv.data == b'None'