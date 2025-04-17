def test_get_session_value(app, client):
    @app.route("/set")
    def set_value():
        flask.session['value'] = 'test_value'
        return ""

    @app.route("/get")
    def get_value():
        return flask.session.get('value', 'None')

    # Test setting a session value
    client.get("/set")
    rv = client.get("/get")
    assert rv.data == b'test_value'

    # Test getting a session value when it is not set
    flask.session.clear()  # Clear the session
    rv = client.get("/get")
    assert rv.data == b'None'

    # Test getting a session value after expiration
    @app.route("/expire")
    def expire_session():
        flask.session['value'] = 'temporary_value'
        flask.session.permanent = True
        return ""

    client.get("/expire")
    assert "set-cookie" in client.get("/").headers
    flask.session.permanent = False  # Simulate session expiration
    rv = client.get("/get")
    assert rv.data == b'None'