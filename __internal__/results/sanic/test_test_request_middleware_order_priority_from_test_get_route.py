import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize("expected", ["I am get method"])
def test_get_method_response(app: Sanic, expected):
    @app.get("/")
    async def handler(request):
        return text("I am get method")

    request, response = app.test_client.get("/")
    
    assert response.status == 200
    assert response.text == expected

@pytest.mark.parametrize("url", ["/", "/nonexistent"])
def test_get_method_edge_cases(app: Sanic, url):
    @app.get("/")
    async def handler(request):
        return text("I am get method")

    request, response = app.test_client.get(url)
    
    if url == "/":
        assert response.status == 200
        assert response.text == "I am get method"
    else:
        assert response.status == 404
        assert "Requested URL" in response.text

def test_get_method_with_middleware(app: Sanic):
    results = []

    @app.middleware
    async def middleware(request):
        results.append(request)

    @app.get("/")
    async def handler(request):
        return text("I am get method")

    request, response = app.test_client.get("/")
    
    assert response.text == "I am get method"
    assert len(results) == 1
    assert results[0] is request