import pytest
import flask
from flask.views import MethodView

def test_head_response(app, client):
    class Index(MethodView):
        def head(self):
            return flask.Response('', headers={'X-Method': 'HEAD'})

    app.add_url_rule("/", view_func=Index.as_view("index"))
    rv = client.head("/")
    assert rv.data == b""
    assert rv.headers["X-Method"] == "HEAD"

def test_head_with_different_headers(app, client):
    class Index(MethodView):
        def head(self):
            return flask.Response('', headers={'X-Method': 'HEAD', 'Custom-Header': 'Value'})

    app.add_url_rule("/", view_func=Index.as_view("index"))
    rv = client.head("/")
    assert rv.data == b""
    assert rv.headers["X-Method"] == "HEAD"
    assert rv.headers["Custom-Header"] == "Value"

def test_head_empty_response(app, client):
    class Index(MethodView):
        def head(self):
            return flask.Response('', headers={'X-Method': 'HEAD'})

    app.add_url_rule("/", view_func=Index.as_view("index"))
    rv = client.head("/")
    assert rv.data == b""
    assert rv.status_code == 200

def test_head_not_found(app, client):
    rv = client.head("/nonexistent")
    assert rv.status_code == 404

def test_head_with_content_length(app, client):
    class Index(MethodView):
        def head(self):
            return flask.Response('', headers={'X-Method': 'HEAD', 'Content-Length': '0'})

    app.add_url_rule("/", view_func=Index.as_view("index"))
    rv = client.head("/")
    assert rv.headers["Content-Length"] == '0'