import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize("expected", [
    "I am get method",
])
def test_get_method_response(app: Sanic, expected):
    @app.get("/get")
    def get_handler(request):
        return text("I am get method")

    request, response = app.test_client.get("/get")
    
    assert response.status == 200
    assert response.text == expected

@pytest.mark.parametrize("path", [
    "/get",
    "/nonexistent",
])
def test_get_method_edge_cases(app: Sanic, path):
    @app.get("/get")
    def get_handler(request):
        return text("I am get method")

    request, response = app.test_client.get(path)
    
    if path == "/get":
        assert response.status == 200
        assert response.text == "I am get method"
    else:
        assert response.status == 404
        assert "Requested URL" in response.text

def test_get_method_with_query_params(app: Sanic):
    @app.get("/get")
    def get_handler(request):
        return text(f"I am get method with query param: {request.args.get('param', 'none')}")

    request, response = app.test_client.get("/get?param=test")
    
    assert response.status == 200
    assert response.text == "I am get method with query param: test"