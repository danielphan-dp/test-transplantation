def test_get_session_value_none(app, client):
    @app.route("/get")
    def get():
        v = flask.session.get('value', 'None')
        return v

    assert client.get("/get").data == b'None'

def test_get_session_value_set(app, client):
    @app.after_request
    def modify_session(response):
        flask.session["value"] = "test_value"
        return response

    @app.route("/get")
    def get():
        v = flask.session.get('value', 'None')
        return v

    assert client.get("/get").data == b'test_value'

def test_get_session_value_empty_string(app, client):
    @app.after_request
    def modify_session(response):
        flask.session["value"] = ""
        return response

    @app.route("/get")
    def get():
        v = flask.session.get('value', 'None')
        return v

    assert client.get("/get").data == b''

def test_get_session_value_none_after_clear(app, client):
    @app.after_request
    def modify_session(response):
        flask.session["value"] = "test_value"
        return response

    @app.route("/clear")
    def clear_session():
        flask.session.clear()
        return "Session Cleared"

    @app.route("/get")
    def get():
        v = flask.session.get('value', 'None')
        return v

    client.get("/clear")
    assert client.get("/get").data == b'None'