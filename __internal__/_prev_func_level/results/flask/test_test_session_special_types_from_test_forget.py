def test_get_session_value(app, client):
    @app.route("/set")
    def set_session_value():
        flask.session['value'] = 'test_value'
        return "", 204

    @app.route("/clear")
    def clear_session_value():
        flask.session.pop('value', None)
        return "", 204

    with client:
        # Test setting a session value
        client.get("/set")
        response = client.get("/get")
        assert response.data.decode() == 'test_value'

        # Test getting a session value when it is not set
        client.get("/clear")
        response = client.get("/get")
        assert response.data.decode() == 'None'

        # Test setting a session value to None
        with client:
            flask.session['value'] = None
            response = client.get("/get")
            assert response.data.decode() == 'None'