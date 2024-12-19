import asyncio
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('strict_slashes', [True, False, None])
def test_get_method(app, strict_slashes):
    @app.get("/")
    async def handler(request):
        return text("I am get method")

    request, response = app.test_client.get("/")
    assert response.status == 200
    assert response.text == "I am get method"

@pytest.mark.parametrize('strict_slashes', [True, False, None])
def test_get_method_not_found(app, strict_slashes):
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404
    assert "Requested URL /nonexistent not found" in response.text

@pytest.mark.parametrize('strict_slashes', [True, False, None])
def test_get_method_with_query_param(app, strict_slashes):
    @app.get("/query")
    async def handler(request):
        return text(f"Query param received: {request.args.get('param', 'none')}")

    request, response = app.test_client.get("/query?param=test")
    assert response.status == 200
    assert response.text == "Query param received: test"