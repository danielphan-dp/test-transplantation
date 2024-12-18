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

    rv = client.get("/head")
    assert rv.status_code == 405

def test_head_method_with_other_methods(app, client):
    @app.route("/head", methods=["GET", "HEAD"])
    def head_method():
        return flask.Response('', headers={'X-Method': 'HEAD'})

    rv = client.get("/head")
    assert rv.status_code == 200
    assert rv.data == b''
    assert rv.headers['X-Method'] == 'HEAD'

    rv = client.post("/head")
    assert rv.status_code == 405

def test_head_method_no_content(app, client):
    @app.route("/empty", methods=["HEAD"])
    def empty_head():
        return flask.Response('', headers={'X-Method': 'HEAD'})

    rv = client.head("/empty")
    assert rv.status_code == 200
    assert rv.data == b''

def test_head_method_with_invalid_route(app, client):
    rv = client.head("/nonexistent")
    assert rv.status_code == 404