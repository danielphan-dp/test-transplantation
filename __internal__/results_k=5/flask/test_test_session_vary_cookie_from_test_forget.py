def test_get_session_value(app, client):
    @app.route("/set_value")
    def set_value():
        flask.session["value"] = "test_value"
        return ""

    @app.route("/clear_value")
    def clear_value():
        flask.session.clear()
        return ""

    # Test when session value is set
    client.get("/set_value")
    response = client.get("/get")
    assert response.data.decode() == "test_value"

    # Test when session value is not set
    client.get("/clear_value")
    response = client.get("/get")
    assert response.data.decode() == "None"