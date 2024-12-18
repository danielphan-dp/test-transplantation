import flask
import pytest

def test_get_value_from_session(app, client):
    app.testing = True

    @app.route("/set")
    def set_value():
        flask.session['value'] = 'Test Value'
        return "Value Set"

    with client:
        resp = client.get("/set")
        assert resp.data == b"Value Set"
        assert resp.status_code == 200

    with client:
        resp = client.get('/get')
        assert resp.data == b'Test Value'
        assert resp.status_code == 200

def test_get_value_not_set(app, client):
    app.testing = True

    with client:
        resp = client.get('/get')
        assert resp.data == b'None'
        assert resp.status_code == 200

def test_get_value_after_clear(app, client):
    app.testing = True

    @app.route("/set")
    def set_value():
        flask.session['value'] = 'Another Value'
        return "Value Set"

    @app.route("/clear")
    def clear_value():
        flask.session.clear()
        return "Session Cleared"

    with client:
        resp = client.get("/set")
        assert resp.data == b"Value Set"
        assert resp.status_code == 200

    with client:
        resp = client.get('/clear')
        assert resp.data == b"Session Cleared"
        assert resp.status_code == 200

    with client:
        resp = client.get('/get')
        assert resp.data == b'None'
        assert resp.status_code == 200