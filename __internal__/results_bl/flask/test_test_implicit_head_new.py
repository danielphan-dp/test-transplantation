import pytest
import flask
from flask.views import MethodView

def test_head_method(app, client):
    class HeadView(MethodView):
        def head(self):
            return flask.Response('', headers={'X-Method': 'HEAD'})

    app.add_url_rule("/head", view_func=HeadView.as_view("head_view"))
    
    rv = client.head("/head")
    assert rv.data == b""
    assert rv.headers["X-Method"] == "HEAD"

def test_head_method_with_invalid_route(app, client):
    rv = client.head("/invalid")
    assert rv.status_code == 404

def test_head_method_with_additional_headers(app, client):
    class CustomHeadView(MethodView):
        def head(self):
            return flask.Response('', headers={'X-Method': 'HEAD', 'Custom-Header': 'Value'})

    app.add_url_rule("/custom_head", view_func=CustomHeadView.as_view("custom_head_view"))
    
    rv = client.head("/custom_head")
    assert rv.data == b""
    assert rv.headers["X-Method"] == "HEAD"
    assert rv.headers["Custom-Header"] == "Value"