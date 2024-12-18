import flask
import pytest

def test_get_value_from_session(app, client):
    app.testing = True

    @app.route("/set")
    def set_value():
        flask.session['value'] = 'test_value'
        return "Value set!"

    with client:
        resp = client.get("/set")
        assert resp.data == b"Value set!"
        assert resp.status_code == 200

    with client:
        resp = client.get('/get')
        assert resp.data == b'test_value'
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
        flask.session['value'] = 'test_value'
        return "Value set!"

    @app.route("/clear")
    def clear_value():
        flask.session.clear()
        return "Session cleared!"

    with client:
        client.get("/set")
        resp = client.get('/clear')
        assert resp.data == b"Session cleared!"
        assert resp.status_code == 200

    with client:
        resp = client.get('/get')
        assert resp.data == b'None'
        assert resp.status_code == 200