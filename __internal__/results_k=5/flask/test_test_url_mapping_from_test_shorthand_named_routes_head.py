import flask
import pytest

def test_head_method(app, client):
    @app.route("/head", methods=["HEAD"])
    def head_method():
        return flask.Response('', headers={'X-Method': 'HEAD'})

    rv = client.head("/head")
    assert rv.status_code == 200
    assert rv.data == b''
    assert rv.headers['X-Method'] == 'HEAD'

def test_head_method_with_different_route(app, client):
    @app.route("/another_head", methods=["HEAD"])
    def another_head_method():
        return flask.Response('', headers={'X-Method': 'HEAD'})

    rv = client.head("/another_head")
    assert rv.status_code == 200
    assert rv.data == b''
    assert rv.headers['X-Method'] == 'HEAD'

def test_head_method_not_allowed(app, client):
    @app.route("/not_allowed", methods=["POST"])
    def not_allowed_method():
        return "Not Allowed", 405

    rv = client.head("/not_allowed")
    assert rv.status_code == 405
    assert rv.data == b''

def test_head_method_with_content(app, client):
    @app.route("/content", methods=["GET"])
    def content_method():
        return "This is a GET response"

    rv = client.get("/content")
    assert rv.data == b'This is a GET response'

    rv = client.head("/content")
    assert rv.status_code == 200
    assert rv.data == b''