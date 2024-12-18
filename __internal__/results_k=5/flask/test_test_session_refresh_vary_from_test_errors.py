def test_get_session_value(app, client):
    @app.route("/set_value")
    def set_value():
        flask.session["value"] = "test_value"
        return ""

    @app.route("/get")
    def get():
        v = flask.session.get('value', 'None')
        return v

    # Test setting a session value
    rv = client.get("/set_value")
    assert rv.status_code == 200

    # Test getting the session value
    rv = client.get("/get")
    assert rv.data.decode() == "test_value"

    # Test getting a non-existent session value
    with client.session_transaction() as session:
        session.clear()
    rv = client.get("/get")
    assert rv.data.decode() == "None"