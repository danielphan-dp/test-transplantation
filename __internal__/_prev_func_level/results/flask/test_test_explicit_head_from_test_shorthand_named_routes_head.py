import pytest
import flask

def test_head_response(app, client):
    class Index(flask.views.MethodView):
        def head(self):
            return flask.Response('', headers={'X-Method': 'HEAD'})

    app.add_url_rule("/", view_func=Index.as_view("index"))
    rv = client.head("/")
    assert rv.data == b""
    assert rv.headers["X-Method"] == "HEAD"

def test_head_with_different_route(app, client):
    class Index(flask.views.MethodView):
        def head(self):
            return flask.Response('', headers={'X-Method': 'HEAD'})

    app.add_url_rule("/test", view_func=Index.as_view("test_index"))
    rv = client.head("/test")
    assert rv.data == b""
    assert rv.headers["X-Method"] == "HEAD"

def test_head_empty_response(app, client):
    class Index(flask.views.MethodView):
        def head(self):
            return flask.Response('', headers={'X-Method': 'HEAD'})

    app.add_url_rule("/", view_func=Index.as_view("index"))
    rv = client.head("/")
    assert rv.data == b""
    assert rv.headers["X-Method"] == "HEAD"

def test_head_with_custom_header(app, client):
    class Index(flask.views.MethodView):
        def head(self):
            return flask.Response('', headers={'X-Custom-Header': 'CustomValue', 'X-Method': 'HEAD'})

    app.add_url_rule("/", view_func=Index.as_view("index"))
    rv = client.head("/")
    assert rv.data == b""
    assert rv.headers["X-Custom-Header"] == "CustomValue"
    assert rv.headers["X-Method"] == "HEAD"