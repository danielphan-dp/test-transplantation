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

def test_get_method_invalid_route(app: Sanic):
    request, response = app.test_client.get("/invalid_route")
    
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

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

def test_get_method_with_query_param(app: Sanic):
    @app.get("/get")
    def handler(request):
        return text(f'I am get method with query param: {request.args.get("param", "none")}')

    request, response = app.test_client.get("/get?param=test")

    assert response.text == "I am get method with query param: test"