def test_get_value_from_session(app, client):
    app.testing = True

    @app.route("/set/<value>")
    def set_value(value):
        flask.session['value'] = value
        return "Value set"

    @app.route("/get")
    def get():
        v = flask.session.get('value', 'None')
        return v

    # Test default value when session is empty
    rv = client.get("/get")
    assert rv.data == b'None'

    # Test setting a value in the session
    rv = client.get("/set/test_value")
    assert rv.data == b'Value set'

    # Test retrieving the value from the session
    rv = client.get("/get")
    assert rv.data == b'test_value'

    # Test setting another value in the session
    rv = client.get("/set/another_value")
    assert rv.data == b'Value set'

    # Test retrieving the new value from the session
    rv = client.get("/get")
    assert rv.data == b'another_value'