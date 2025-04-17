import flask
import pytest

def test_get_value_from_session(app, client):
    app.testing = True

    @app.route("/set_value")
    def set_value():
        flask.session['value'] = 42
        return "Value set"

    with client:
        resp = client.get("/set_value")
        assert resp.data == b"Value set"
        assert resp.status_code == 200

    with client:
        resp = client.get('/get')
        assert resp.data == b'42'
        assert resp.status_code == 200

def test_get_value_not_set(app, client):
    app.testing = True

    with client:
        resp = client.get('/get')
        assert resp.data == b'None'
        assert resp.status_code == 200

def test_get_value_with_different_session(app, client):
    app.testing = True

    @app.route("/set_different_value")
    def set_different_value():
        flask.session['value'] = 'Hello'
        return "Different value set"

    with client:
        resp = client.get("/set_different_value")
        assert resp.data == b"Different value set"
        assert resp.status_code == 200

    with client:
        resp = client.get('/get')
        assert resp.data == b'Hello'
        assert resp.status_code == 200

def test_get_value_after_session_clear(app, client):
    app.testing = True

    @app.route("/set_value")
    def set_value():
        flask.session['value'] = 42
        return "Value set"

    @app.route("/clear_session")
    def clear_session():
        flask.session.clear()
        return "Session cleared"

    with client:
        resp = client.get("/set_value")
        assert resp.data == b"Value set"
        assert resp.status_code == 200

    with client:
        resp = client.get('/clear_session')
        assert resp.data == b"Session cleared"
        assert resp.status_code == 200

    with client:
        resp = client.get('/get')
        assert resp.data == b'None'
        assert resp.status_code == 200