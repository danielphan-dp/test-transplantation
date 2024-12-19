import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

@app.get("/test")
async def get_method(request):
    return text('I am get method')

def test_get_method_response(app):
    request, resp = app.test_client.get("/test")
    assert resp.text == 'I am get method'

def test_get_method_with_ipv6(app):
    request, resp = app.test_client.get("/test", host="::1")
    assert resp.text == 'I am get method'
    assert request.ip == "::1"

def test_get_method_with_invalid_path(app):
    request, resp = app.test_client.get("/invalid_path")
    assert resp.status == 404

def test_get_method_with_no_host(app):
    request, resp = app.test_client.get("/test", host="")
    assert resp.status == 400

def test_get_method_with_different_http_methods(app):
    request, resp = app.test_client.post("/test")
    assert resp.status == 405

    request, resp = app.test_client.put("/test")
    assert resp.status == 405

    request, resp = app.test_client.delete("/test")
    assert resp.status == 405