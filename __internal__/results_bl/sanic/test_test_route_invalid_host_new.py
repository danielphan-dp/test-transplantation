import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_get_method_valid(app):
    @app.get("/test")
    async def handler(request):
        return text("I am get method")

    request, response = app.test_client.get("/test")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_invalid_host(app):
    host = 321
    with pytest.raises(ValueError) as excinfo:
        @app.get("/test", host=host)
        async def handler(request):
            return text("pass")

    assert str(excinfo.value) == (
        "Expected either string or Iterable of " "host strings, not {!r}"
    ).format(host)

def test_get_method_no_route(app):
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404

def test_get_method_with_query_params(app):
    @app.get("/test")
    async def handler(request):
        return text(f"Query param: {request.args.get('param')}")

    request, response = app.test_client.get("/test?param=value")
    assert response.status == 200
    assert response.text == "Query param: value"