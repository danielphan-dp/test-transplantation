def test_get_session_value(app, client):
    @app.route("/set")
    def set_session_value():
        flask.session["value"] = "test_value"
        return "Value set"

    @app.route("/get")
    def get_session_value():
        return flask.session.get('value', 'None')

    client.get("/set")
    assert client.get("/get").data == b"test_value"

def test_get_session_value_default(app, client):
    @app.route("/get")
    def get_session_value():
        return flask.session.get('value', 'None')

    assert client.get("/get").data == b"None"

def test_get_session_value_after_modification(app, client):
    @app.after_request
    def modify_session(response):
        flask.session["value"] = "modified_value"
        return response

    @app.route("/get")
    def get_session_value():
        return flask.session.get('value', 'None')

    assert client.get("/get").data == b"None"
    assert client.get("/get").data == b"modified_value"