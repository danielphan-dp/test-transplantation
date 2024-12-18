def test_get_value_from_session(app, client):
    @app.route("/set/<value>")
    def set_value(value):
        flask.session['value'] = value
        return "Value set"

    @app.route("/get")
    def get_value():
        return flask.session.get('value', 'None')

    # Test setting a value in the session
    response = client.get("/set/test_value")
    assert response.data == b"Value set"

    # Test getting the value from the session
    response = client.get("/get")
    assert response.data == b"test_value"

    # Test getting a default value when session is empty
    with client.session_transaction() as session:
        session.clear()
    response = client.get("/get")
    assert response.data == b'None'