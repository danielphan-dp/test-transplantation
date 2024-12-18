import flask
import pytest

def test_head_response(app, client):
    class Index(flask.views.MethodView):
        def get(self):
            return "GET"

        def head(self):
            return flask.Response('', headers={'X-Method': 'HEAD'})

    app.add_url_rule("/", view_func=Index.as_view("index"))

    rv = client.get("/")
    assert rv.data == b"GET"

    rv = client.head("/")
    assert rv.status_code == 200
    assert not rv.data
    assert rv.headers["X-Method"] == "HEAD"

def test_head_response_with_different_methods(app, client):
    class Index(flask.views.MethodView):
        def get(self):
            return "GET"

        def head(self):
            return flask.Response('', headers={'X-Method': 'HEAD'})

    app.add_url_rule("/", view_func=Index.as_view("index"), methods=["GET", "HEAD"])

    rv = client.post("/")
    assert rv.status_code == 405
    assert sorted(rv.allow) == ["GET", "HEAD"]

    rv = client.delete("/")
    assert rv.status_code == 405
    assert sorted(rv.allow) == ["GET", "HEAD"]