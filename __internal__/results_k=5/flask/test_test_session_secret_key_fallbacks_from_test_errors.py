def test_get_session_value(app, client) -> None:
    @app.route("/set_value", methods=["POST"])
    def set_value() -> str:
        flask.session["value"] = "test_value"
        return ""

    @app.route("/get_value", methods=["GET"])
    def get_value() -> str:
        return flask.session.get("value", "None")

    # Set session with a value
    client.post("/set_value")
    assert client.get("/get_value").data.decode() == "test_value"

    # Change secret key, session can't be loaded and appears empty
    app.secret_key = "new test key"
    assert client.get("/get_value").data.decode() == "None"

    # Add initial secret key as fallback, session can be loaded
    app.config["SECRET_KEY_FALLBACKS"] = ["test key"]
    assert client.get("/get_value").data.decode() == "None"

    # Test with no session value set
    with client.session_transaction() as session:
        session.clear()
    assert client.get("/get_value").data.decode() == "None"