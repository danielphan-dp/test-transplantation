import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('expected', [
    "I am get method",
])
def test_get_method_response(app: Sanic, expected):
    @app.get("/get")
    def handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/get")
    
    assert response.text == expected
    assert response.status == 200

def test_get_method_with_invalid_route(app: Sanic):
    request, response = app.test_client.get("/invalid")
    
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_middleware(app: Sanic):
    results = []

    @app.middleware
    async def middleware(request):
        results.append(request)

    @app.get("/get")
    def handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/get")

    assert response.text == "I am get method"
    assert len(results) == 1
    assert results[0] is request

def test_get_method_with_custom_header(app: Sanic):
    @app.get("/get")
    def handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/get", headers={"X-Custom-Header": "value"})
    
    assert response.text == "I am get method"
    assert response.status == 200
    assert response.headers.get("X-Custom-Header") is None  # No custom header in response