import flask
import pytest

def test_get_value_from_session(app, client):
    app.testing = True

    @app.route("/set")
    def set_value():
        flask.session['value'] = 42
        return "Value set!"

    with client:
        resp = client.get("/set")
        assert resp.data == b"Value set!"
        assert resp.status_code == 200

    with client:
        resp = client.get("/get")
        assert resp.data == b'42'
        assert resp.status_code == 200

def test_get_value_not_set(app, client):
    app.testing = True

    with client:
        resp = client.get("/get")
        assert resp.data == b'None'
        assert resp.status_code == 200

def test_get_value_with_different_session(app, client):
    app.testing = True

    @app.route("/set_another")
    def set_another_value():
        flask.session['value'] = 'Hello'
        return "Another value set!"

    with client:
        resp = client.get("/set_another")
        assert resp.data == b"Another value set!"
        assert resp.status_code == 200

    with client:
        resp = client.get("/get")
        assert resp.data == b'Hello'
        assert resp.status_code == 200

def test_get_value_after_session_clear(app, client):
    app.testing = True

    @app.route("/set")
    def set_value():
        flask.session['value'] = 100
        return "Value set!"

    @app.route("/clear")
    def clear_session():
        flask.session.clear()
        return "Session cleared!"

    with client:
        resp = client.get("/set")
        assert resp.data == b"Value set!"
        assert resp.status_code == 200

    with client:
        resp = client.get("/clear")
        assert resp.data == b"Session cleared!"
        assert resp.status_code == 200

    with client:
        resp = client.get("/get")
        assert resp.data == b'None'
        assert resp.status_code == 200