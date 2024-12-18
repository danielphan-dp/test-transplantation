def test_get_session_value_none(app, client):
    @app.route("/get")
    def get():
        v = flask.session.get('value', 'None')
        return v

    response = client.get("/get")
    assert response.data == b'None'

def test_get_session_value_set(app, client):
    @app.after_request
    def modify_session(response):
        flask.session["value"] = "42"
        return response

    @app.route("/get")
    def get():
        v = flask.session.get('value', 'None')
        return v

    response = client.get("/get")
    assert response.data == b'42'

def test_get_session_value_empty_string(app, client):
    @app.after_request
    def modify_session(response):
        flask.session["value"] = ""
        return response

    @app.route("/get")
    def get():
        v = flask.session.get('value', 'None')
        return v

    response = client.get("/get")
    assert response.data == b''

def test_get_session_value_none_with_other_key(app, client):
    @app.after_request
    def modify_session(response):
        flask.session["other_key"] = "value"
        return response

    @app.route("/get")
    def get():
        v = flask.session.get('value', 'None')
        return v

    response = client.get("/get")
    assert response.data == b'None'