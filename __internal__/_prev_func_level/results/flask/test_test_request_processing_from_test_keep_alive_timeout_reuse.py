def test_get_value_from_session(app, client):
    @app.route("/set/<value>")
    def set_value(value):
        flask.session['value'] = value
        return "Value set"

    @app.route("/get")
    def get_value():
        return flask.session.get('value', 'None')

    # Test default session value
    rv = client.get("/get")
    assert rv.data == b'None'

    # Test setting a session value
    rv = client.get("/set/test_value")
    assert rv.data == b'Value set'

    # Test retrieving the session value
    rv = client.get("/get")
    assert rv.data == b'test_value'

    # Test clearing the session
    with client.session_transaction() as session:
        session.clear()

    rv = client.get("/get")
    assert rv.data == b'None'