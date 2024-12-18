import pytest
import flask

def test_head_response(app, client):
    class Index(flask.views.MethodView):
        def head(self):
            return flask.Response('', headers={'X-Method': 'HEAD'})

    app.add_url_rule("/", view_func=Index.as_view("index"))
    
    # Test HEAD request
    rv = client.head("/")
    assert rv.data == b""
    assert rv.headers["X-Method"] == "HEAD"
    
    # Test GET request to ensure it still works
    rv = client.get("/")
    assert rv.data == b""
    assert rv.headers["X-Method"] == "HEAD"  # Ensure headers are consistent

def test_head_with_different_methods(app, client):
    class Index(flask.views.MethodView):
        def get(self):
            return "GET"

        def post(self):
            return "POST"

        def head(self):
            return flask.Response("", headers={"X-Method": "HEAD"})

    app.add_url_rule("/", view_func=Index.as_view("index"))
    
    # Test GET request
    rv = client.get("/")
    assert rv.data == b"GET"
    
    # Test POST request
    rv = client.post("/")
    assert rv.data == b"POST"
    
    # Test HEAD request
    rv = client.head("/")
    assert rv.data == b""
    assert rv.headers["X-Method"] == "HEAD"

def test_head_empty_response(app, client):
    class Index(flask.views.MethodView):
        def head(self):
            return flask.Response("", headers={"X-Method": "HEAD"})

    app.add_url_rule("/", view_func=Index.as_view("index"))
    
    # Test HEAD request
    rv = client.head("/")
    assert rv.data == b""
    assert rv.status_code == 200
    assert rv.headers["X-Method"] == "HEAD"