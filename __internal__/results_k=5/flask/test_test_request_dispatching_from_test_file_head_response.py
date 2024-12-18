import flask
import pytest

def test_head_response(app, client):
    @app.route("/head-test", methods=["HEAD"])
    def head_test():
        return flask.Response('', headers={'X-Method': 'HEAD'})

    rv = client.head("/head-test")
    assert rv.status_code == 200
    assert rv.data == b""
    assert rv.headers["X-Method"] == "HEAD"

def test_head_with_other_methods(app, client):
    @app.route("/method-test", methods=["GET", "HEAD"])
    def method_test():
        return flask.Response("GET response", headers={'X-Method': flask.request.method})

    rv = client.get("/method-test")
    assert rv.data == b"GET response"
    assert rv.headers["X-Method"] == "GET"

    rv = client.head("/method-test")
    assert rv.data == b""
    assert rv.headers["X-Method"] == "HEAD"

def test_head_not_allowed(app, client):
    @app.route("/not-allowed", methods=["POST"])
    def not_allowed():
        return "Method Not Allowed", 405

    rv = client.head("/not-allowed")
    assert rv.status_code == 405
    assert "HEAD" not in rv.allow
    assert "POST" in rv.allow

def test_head_empty_response(app, client):
    @app.route("/empty-head", methods=["HEAD"])
    def empty_head():
        return flask.Response('', headers={'X-Method': 'HEAD'})

    rv = client.head("/empty-head")
    assert rv.status_code == 200
    assert rv.data == b""
    assert rv.headers["X-Method"] == "HEAD"