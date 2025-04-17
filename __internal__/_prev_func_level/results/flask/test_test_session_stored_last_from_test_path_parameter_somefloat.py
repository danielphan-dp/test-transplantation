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

def test_get_session_value_empty(app, client):
    @app.route("/get")
    def get():
        v = flask.session.get('value', 'None')
        return v

    assert client.get("/get").data == b'None'

def test_get_session_value_overwrite(app, client):
    @app.after_request
    def modify_session(response):
        flask.session["value"] = "initial_value"
        return response

    @app.after_request
    def modify_session_later(response):
        flask.session["value"] = "overwritten_value"
        return response

    @app.route("/get")
    def get():
        v = flask.session.get('value', 'None')
        return v

    assert client.get("/get").data == b'overwritten_value'