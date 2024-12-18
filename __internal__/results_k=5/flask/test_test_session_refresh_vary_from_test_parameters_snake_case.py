import flask
import pytest

def test_get_session_value(app, client):
    @app.route("/set")
    def set_value():
        flask.session["value"] = "test_value"
        return ""

    @app.route("/get")
    def get_value():
        return flask.session.get('value', 'None')

    # Set the session value
    client.get("/set")
    
    # Test retrieving the session value
    rv = client.get("/get")
    assert rv.data.decode() == "test_value"

    # Test when session value is not set
    with client.session_transaction() as session:
        session.clear()
    rv = client.get("/get")
    assert rv.data.decode() == "None"