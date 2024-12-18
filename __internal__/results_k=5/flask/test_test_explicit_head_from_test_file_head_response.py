import pytest
import flask

def test_head_response(app, client):
    class HeadView(flask.views.MethodView):
        def head(self):
            return flask.Response('', headers={'X-Method': 'HEAD'})

    app.add_url_rule("/head", view_func=HeadView.as_view("head_view"))
    
    rv = client.head("/head")
    assert rv.data == b""
    assert rv.headers["X-Method"] == "HEAD"
    assert rv.status_code == 200

def test_head_with_different_route(app, client):
    class AnotherView(flask.views.MethodView):
        def head(self):
            return flask.Response('', headers={'X-Method': 'HEAD'})

    app.add_url_rule("/another", view_func=AnotherView.as_view("another_view"))
    
    rv = client.head("/another")
    assert rv.data == b""
    assert rv.headers["X-Method"] == "HEAD"
    assert rv.status_code == 200

def test_head_response_no_content(app, client):
    class NoContentView(flask.views.MethodView):
        def head(self):
            return flask.Response('', headers={'X-Method': 'HEAD'})

    app.add_url_rule("/no-content", view_func=NoContentView.as_view("no_content_view"))
    
    rv = client.head("/no-content")
    assert rv.data == b""
    assert rv.headers["X-Method"] == "HEAD"
    assert rv.status_code == 200

def test_head_response_with_custom_header(app, client):
    class CustomHeaderView(flask.views.MethodView):
        def head(self):
            return flask.Response('', headers={'X-Custom-Header': 'CustomValue', 'X-Method': 'HEAD'})

    app.add_url_rule("/custom-header", view_func=CustomHeaderView.as_view("custom_header_view"))
    
    rv = client.head("/custom-header")
    assert rv.data == b""
    assert rv.headers["X-Custom-Header"] == "CustomValue"
    assert rv.headers["X-Method"] == "HEAD"
    assert rv.status_code == 200