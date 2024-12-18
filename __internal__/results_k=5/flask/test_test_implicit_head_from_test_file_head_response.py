import pytest
import flask

def test_explicit_head(app, client):
    class Index(flask.views.MethodView):
        def get(self):
            return "GET"

        def head(self):
            return flask.Response("", headers={"X-Method": "HEAD"})

    app.add_url_rule("/", view_func=Index.as_view("index"))
    
    # Test GET request
    rv = client.get("/")
    assert rv.data == b"GET"
    
    # Test HEAD request
    rv = client.head("/")
    assert rv.data == b""
    assert rv.headers["X-Method"] == "HEAD"

    # Test additional headers
    rv = client.head("/")
    assert "X-Method" in rv.headers
    assert rv.headers["X-Method"] == "HEAD"