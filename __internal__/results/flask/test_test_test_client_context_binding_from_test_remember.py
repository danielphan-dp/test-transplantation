import flask
import pytest

def test_get_value_from_session(app, client):
    app.testing = True

    @app.route("/set")
    def set_value():
        flask.session['value'] = 'test_value'
        return "Value set!"

    @app.route("/get")
    def get_value():
        return flask.session.get('value', 'None')

    with client:
        resp_set = client.get("/set")
        assert resp_set.data == b"Value set!"
        assert resp_set.status_code == 200

        resp_get = client.get("/get")
        assert resp_get.data == b"test_value"
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

def test_get_value_with_none(app, client):
    app.testing = True

    @app.route("/set_none")
    def set_none():
        flask.session['value'] = None
        return "None set!"

    @app.route("/get")
    def get_value():
        return flask.session.get('value', 'None')

    with client:
        resp_set = client.get("/set_none")
        assert resp_set.data == b"None set!"
        assert resp_set.status_code == 200

        resp_get = client.get("/get")
        assert resp_get.data == b'None'
        assert resp_get.status_code == 200