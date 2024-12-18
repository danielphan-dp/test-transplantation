import flask
import pytest

def test_head_method(app, client):
    class HeadView(flask.views.MethodView):
        def head(self):
            return flask.Response('', headers={'X-Method': 'HEAD'})

    app.add_url_rule("/head", view_func=HeadView.as_view("head_view"))

    rv = client.head("/head")
    assert rv.status_code == 200
    assert rv.data == b""
    assert rv.headers["X-Method"] == "HEAD"

def test_head_method_with_different_route(app, client):
    class AnotherView(flask.views.MethodView):
        def head(self):
            return flask.Response('', headers={'X-Method': 'HEAD'})

    app.add_url_rule("/another", view_func=AnotherView.as_view("another_view"))

    rv = client.head("/another")
    assert rv.status_code == 200
    assert rv.data == b""
    assert rv.headers["X-Method"] == "HEAD"

def test_head_method_not_allowed(app, client):
    class NotAllowedView(flask.views.MethodView):
        def post(self):
            return "POST method"

    app.add_url_rule("/not_allowed", view_func=NotAllowedView.as_view("not_allowed_view"), methods=["POST"])

    rv = client.head("/not_allowed")
    assert rv.status_code == 405
    assert "POST" in rv.headers["Allow"]

def test_head_method_with_content(app, client):
    class ContentView(flask.views.MethodView):
        def get(self):
            return "Content"

        def head(self):
            return flask.Response('', headers={'X-Method': 'HEAD'})

    app.add_url_rule("/content", view_func=ContentView.as_view("content_view"))

    rv = client.get("/content")
    assert rv.data == b"Content"

    rv = client.head("/content")
    assert rv.status_code == 200
    assert rv.data == b""