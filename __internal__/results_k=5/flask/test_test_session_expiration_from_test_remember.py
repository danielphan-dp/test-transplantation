def test_get_session_value(app, client):
    @app.route("/set_value")
    def set_value():
        flask.session["value"] = "test_value"
        return ""

    @app.route("/get_value")
    def get_value():
        return flask.session.get('value', 'None')

    # Test setting a session value
    client.get("/set_value")
    rv = client.get("/get_value")
    assert rv.data == b"test_value"

    # Test getting a session value when not set
    flask.session.pop('value', None)  # Clear the session value
    rv = client.get("/get_value")
    assert rv.data == b"None"

    # Test setting session value to None
    @app.route("/set_none")
    def set_none():
        flask.session["value"] = None
        return ""

    client.get("/set_none")
    rv = client.get("/get_value")
    assert rv.data == b"None"