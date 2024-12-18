import pytest
import flask
from flask.views import MethodView

def test_head_response(app, client):
    class HeadView(MethodView):
        def head(self):
            return flask.Response('', headers={'X-Method': 'HEAD'})

    app.add_url_rule("/head", view_func=HeadView.as_view("head_view"))
    rv = client.head("/head")
    assert rv.data == b""
    assert rv.headers["X-Method"] == "HEAD"

def test_head_with_different_route(app, client):
    class AnotherView(MethodView):
        def head(self):
            return flask.Response('', headers={'X-Method': 'HEAD'})

    app.add_url_rule("/another", view_func=AnotherView.as_view("another_view"))
    rv = client.head("/another")
    assert rv.data == b""
    assert rv.headers["X-Method"] == "HEAD"

def test_head_empty_response(app, client):
    class EmptyView(MethodView):
        def head(self):
            return flask.Response('', headers={'X-Method': 'HEAD'})

    app.add_url_rule("/empty", view_func=EmptyView.as_view("empty_view"))
    rv = client.head("/empty")
    assert rv.data == b""
    assert rv.headers["X-Method"] == "HEAD"