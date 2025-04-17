import flask
import pytest

def test_head_response(app, client):
    @app.route("/head_test", methods=["HEAD"])
    def head_test():
        return flask.Response('', headers={'X-Method': 'HEAD'})

    rv = client.head("/head_test")
    assert rv.status_code == 200
    assert not rv.data
    assert rv.headers["X-Method"] == "HEAD"

def test_head_with_other_methods(app, client):
    @app.route("/method_test", methods=["GET", "HEAD"])
    def method_test():
        return flask.Response("GET method", headers={'X-Method': flask.request.method})

    rv = client.get("/method_test")
    assert rv.data == b"GET method"
    assert rv.headers["X-Method"] == "GET"

    rv = client.head("/method_test")
    assert rv.status_code == 200
    assert not rv.data
    assert rv.headers["X-Method"] == "HEAD"

def test_head_on_nonexistent_route(app, client):
    rv = client.head("/nonexistent")
    assert rv.status_code == 404

def test_head_with_custom_headers(app, client):
    @app.route("/custom_head", methods=["HEAD"])
    def custom_head():
        return flask.Response('', headers={'X-Custom-Header': 'CustomValue'})

    rv = client.head("/custom_head")
    assert rv.status_code == 200
    assert rv.headers["X-Custom-Header"] == "CustomValue"