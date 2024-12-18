import pytest
import flask

def test_explicit_head(app, client):
    class Index(flask.views.MethodView):
        def get(self):
            return "GET"

        def head(self):
            return flask.Response("", headers={"X-Method": "HEAD"})

    app.add_url_rule("/", view_func=Index.as_view("index"))
    
    rv = client.get("/")
    assert rv.data == b"GET"
    
    rv = client.head("/")
    assert rv.data == b""
    assert rv.headers["X-Method"] == "HEAD"

def test_head_with_custom_header(app, client):
    class Index(flask.views.MethodView):
        def head(self):
            return flask.Response("", headers={"X-Custom-Header": "CustomValue"})

    app.add_url_rule("/", view_func=Index.as_view("index"))
    
    rv = client.head("/")
    assert rv.data == b""
    assert rv.headers["X-Custom-Header"] == "CustomValue"

def test_head_method_not_allowed(app, client):
    class Index(flask.views.MethodView):
        def post(self):
            return "POST"

    app.add_url_rule("/", view_func=Index.as_view("index"))
    
    rv = client.head("/")
    assert rv.status_code == 405
    assert set(rv.headers["Allow"].split(", ")) == {"POST"}

def test_head_empty_response(app, client):
    class Index(flask.views.MethodView):
        def head(self):
            return flask.Response("", headers={"X-Method": "HEAD"})

    app.add_url_rule("/", view_func=Index.as_view("index"))
    
    rv = client.head("/")
    assert rv.data == b""
    assert rv.headers["X-Method"] == "HEAD"