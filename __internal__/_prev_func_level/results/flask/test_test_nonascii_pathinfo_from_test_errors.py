def test_get_value_from_session(app, client):
    @app.route("/set_value/<value>")
    def set_value(value):
        flask.session['value'] = value
        return "Value set!"

    @app.route("/get_value")
    def get_value():
        return flask.session.get('value', 'None')

    # Test setting a value in the session
    client.get("/set_value/test_value")
    rv = client.get("/get_value")
    assert rv.data == b"test_value"

    # Test getting a default value when session is empty
    with client.session_transaction() as session:
        session.clear()
    rv = client.get("/get_value")
    assert rv.data == b'None'

    # Test setting a non-ASCII value in the session
    client.get("/set_value/киртест")
    rv = client.get("/get_value")
    assert rv.data == b'киртест'