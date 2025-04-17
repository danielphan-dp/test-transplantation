import flask
import pytest

def test_get_value_from_session(app, client):
    app.testing = True

    @app.route("/set")
    def set_value():
        flask.session['value'] = 42
        return "Value set!"

    @app.route("/get")
    def get_value():
        return flask.session.get('value', 'None')

    with client:
        resp_set = client.get("/set")
        assert resp_set.data == b"Value set!"
        assert resp_set.status_code == 200

        resp_get = client.get("/get")
        assert resp_get.data == b"42"
        assert resp_get.status_code == 200

def test_get_value_not_set(app, client):
    app.testing = True

    @app.route("/get")
    def get_value():
        return flask.session.get('value', 'None')

    with client:
        resp_get = client.get("/get")
        assert resp_get.data == b'None'
        assert resp_get.status_code == 200

def test_get_value_after_clear(app, client):
    app.testing = True

    @app.route("/set")
    def set_value():
        flask.session['value'] = 42
        return "Value set!"

    @app.route("/clear")
    def clear_value():
        flask.session.clear()
        return "Session cleared!"

    @app.route("/get")
    def get_value():
        return flask.session.get('value', 'None')

    with client:
        client.get("/set")
        resp_clear = client.get("/clear")
        assert resp_clear.data == b"Session cleared!"
        assert resp_clear.status_code == 200

        resp_get = client.get("/get")
        assert resp_get.data == b'None'
        assert resp_get.status_code == 200