import pytest
import flask

def test_explicit_head(app, client):
    class Index(flask.views.MethodView):
        def get(self):
            return flask.Response("GET", headers={"X-Method": flask.request.method})

        def head(self):
            return flask.Response('', headers={'X-Method': 'HEAD'})

    app.add_url_rule("/", view_func=Index.as_view("index"))
    
    rv = client.get("/")
    assert rv.data == b"GET"
    assert rv.headers["X-Method"] == "GET"
    
    rv = client.head("/")
    assert rv.data == b""
    assert rv.headers["X-Method"] == "HEAD"

def test_head_with_custom_header(app, client):
    class Index(flask.views.MethodView):
        def head(self):
            return flask.Response('', headers={'X-Custom-Header': 'CustomValue'})

    app.add_url_rule("/", view_func=Index.as_view("index"))
    
    rv = client.head("/")
    assert rv.data == b""
    assert rv.headers["X-Custom-Header"] == "CustomValue"

def test_head_on_nonexistent_route(app, client):
    rv = client.head("/nonexistent")
    assert rv.status_code == 404

def test_head_with_query_parameters(app, client):
    class Index(flask.views.MethodView):
        def head(self):
            return flask.Response('', headers={'X-Method': 'HEAD'})

    app.add_url_rule("/", view_func=Index.as_view("index"))
    
    rv = client.head("/?param=value")
    assert rv.data == b""
    assert rv.headers["X-Method"] == "HEAD"