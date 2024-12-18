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
    
    # Test GET request to ensure it doesn't affect HEAD
    rv = client.get("/")
    assert rv.data == b""
    
def test_head_with_different_headers(app, client):
    class Index(flask.views.MethodView):
        def head(self):
            return flask.Response('', headers={'X-Method': 'HEAD', 'Custom-Header': 'Value'})

    app.add_url_rule("/", view_func=Index.as_view("index"))
    
    rv = client.head("/")
    assert rv.data == b""
    assert rv.headers["X-Method"] == "HEAD"
    assert rv.headers["Custom-Header"] == "Value"

def test_head_empty_response(app, client):
    class Index(flask.views.MethodView):
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
    class Index(flask.views.MethodView):
        def head(self):
            return flask.Response('', headers={'X-Method': 'HEAD', 'Content-Length': '0'})

    app.add_url_rule("/", view_func=Index.as_view("index"))
    
    rv = client.head("/")
    assert rv.data == b""
    assert rv.headers["Content-Length"] == '0'