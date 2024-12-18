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

def test_head_method_with_invalid_method(app, client):
    @app.route("/head", methods=["HEAD"])
    def head_method():
        return flask.Response('', headers={'X-Method': 'HEAD'})

    rv = client.get("/head")
    assert rv.status_code == 405
    assert sorted(rv.allow) == ["HEAD"]

def test_head_method_with_other_routes(app, client):
    @app.route("/other", methods=["GET"])
    def other_method():
        return "Other Method"

    @app.route("/head", methods=["HEAD"])
    def head_method():
        return flask.Response('', headers={'X-Method': 'HEAD'})

    rv = client.get("/other")
    assert rv.data == b"Other Method"
    
    rv = client.head("/other")
    assert rv.status_code == 405
    assert sorted(rv.allow) == ["GET", "HEAD"]