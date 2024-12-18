import flask
import pytest

def test_get_value_from_session(app, client):
    app.testing = True

    @app.route("/set")
    def set_value():
        flask.session['value'] = 'Test Value'
        return "Value Set"

    @app.route("/get")
    def get_value():
        return flask.session.get('value', 'None')

    with client:
        resp_set = client.get("/set")
        assert resp_set.data == b"Value Set"
        assert resp_set.status_code == 200

        resp_get = client.get("/get")
        assert resp_get.data == b'Test Value'
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

def test_get_value_with_none_default(app, client):
    app.testing = True

    @app.route("/set_none")
    def set_none_value():
        flask.session['value'] = None
        return "None Value Set"

    @app.route("/get")
    def get_value():
        return flask.session.get('value', 'None')

    with client:
        resp_set = client.get("/set_none")
        assert resp_set.data == b"None Value Set"
        assert resp_set.status_code == 200

        resp_get = client.get("/get")
        assert resp_get.data == b'None'
        assert resp_get.status_code == 200