def test_get_value_from_session(app, client):
    app.testing = True

    @app.route("/set/<value>")
    def set_value(value):
        flask.session['value'] = value
        return "Value set"

    @app.route("/clear")
    def clear_value():
        flask.session.pop('value', None)
        return "Value cleared"

    # Test setting a value in the session
    rv = client.get("/set/test_value")
    assert rv.data == b"Value set"

    # Test getting the value from the session
    rv = client.get("/get")
    assert rv.data == b"test_value"

    # Test clearing the session value
    rv = client.get("/clear")
    assert rv.data == b"Value cleared"

    # Test getting the value after clearing the session
    rv = client.get("/get")
    assert rv.data == b'None'