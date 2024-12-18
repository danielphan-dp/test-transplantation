def test_get_session_value(app, client):
    @app.route("/set_session")
    def set_session():
        flask.session['value'] = 'test_value'
        return "", 204

    with client:
        client.get("/set_session")
        response = client.get('/get')
        assert response.data.decode() == 'test_value'

def test_get_session_value_default(app, client):
    with client:
        response = client.get('/get')
        assert response.data.decode() == 'None'

def test_get_session_value_none(app, client):
    @app.route("/set_session_none")
    def set_session_none():
        flask.session['value'] = None
        return "", 204

    with client:
        client.get("/set_session_none")
        response = client.get('/get')
        assert response.data.decode() == 'None'

def test_get_session_value_empty_string(app, client):
    @app.route("/set_session_empty")
    def set_session_empty():
        flask.session['value'] = ''
        return "", 204

    with client:
        client.get("/set_session_empty")
        response = client.get('/get')
        assert response.data.decode() == ''