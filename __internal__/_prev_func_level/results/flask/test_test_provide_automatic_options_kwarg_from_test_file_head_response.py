import flask
import pytest

def test_head_response(app, client):
    class Index(flask.views.MethodView):
        def head(self):
            return flask.Response('', headers={'X-Method': 'HEAD'})

    app.add_url_rule("/", view_func=Index.as_view("index"))

    rv = client.head("/")
    assert rv.status_code == 200
    assert not rv.data
    assert rv.headers["X-Method"] == "HEAD"

def test_head_response_with_other_methods(app, client):
    class Index(flask.views.MethodView):
        def get(self):
            return "GET"

        def post(self):
            return "POST"

        def head(self):
            return flask.Response('', headers={'X-Method': 'HEAD'})

    app.add_url_rule("/", view_func=Index.as_view("index"), methods=["GET", "POST", "HEAD"])

    rv = client.get("/")
    assert rv.data == b"GET"

    rv = client.post("/")
    assert rv.data == b"POST"

    rv = client.head("/")
    assert rv.status_code == 200
    assert not rv.data
    assert rv.headers["X-Method"] == "HEAD"

def test_head_response_not_allowed(app, client):
    class Index(flask.views.MethodView):
        def get(self):
            return "GET"

    app.add_url_rule("/", view_func=Index.as_view("index"), methods=["GET"])

    rv = client.head("/")
    assert rv.status_code == 405
    assert sorted(rv.allow) == ["GET"]