import pytest
from sanic import Sanic
from sanic.response import text

app = Sanic("test_app")

class DummyView:
    def get(self, request):
        return text('I am get method')

@app.get("/")
async def handler(request):
    view = DummyView()
    return view.get(request)

def test_get_method_response(app):
    request, response = app.test_client.get("/")
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404

def test_get_method_with_additional_headers(app):
    request, response = app.test_client.get("/", headers={"X-Custom-Header": "value"})
    assert response.text == "I am get method"
    assert response.status == 200
    assert response.headers.get("X-Custom-Header") is None

def test_get_method_with_query_params(app):
    request, response = app.test_client.get("/?foo=bar")
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_content_type(app):
    request, response = app.test_client.get("/")
    assert response.content_type == "text/plain; charset=utf-8"