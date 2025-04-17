import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('strict_slashes', [True, False, None])
def test_get_method(app, strict_slashes):
    app.get("/")(lambda request: text("I am get method"))

    request, response = app.test_client.get("/")
    assert response.text == "I am get method"

    request, response = app.test_client.get("/", strict_slashes=strict_slashes)
    assert response.text == "I am get method"

def test_get_method_not_found(app):
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404
    assert "Requested URL /nonexistent not found" in response.text

def test_get_method_with_query_params(app):
    @app.get("/query")
    async def handler(request):
        return text(f"Query param: {request.args.get('param', 'not provided')}")

    request, response = app.test_client.get("/query?param=test")
    assert response.text == "Query param: test"

    request, response = app.test_client.get("/query")
    assert response.text == "Query param: not provided"