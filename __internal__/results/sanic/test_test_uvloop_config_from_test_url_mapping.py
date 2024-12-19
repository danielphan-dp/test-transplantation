import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('path', ["/", "/test"])
def test_get_method(app: Sanic, path):
    @app.get(path)
    def handler(request):
        return text('I am get method')

    request, response = app.test_client.get(path)
    assert response.text == 'I am get method'
    assert response.status == 200

def test_get_method_not_found(app: Sanic):
    request, response = app.test_client.get("/non_existent")
    assert response.status == 404
    assert "Requested URL /non_existent not found" in response.text

def test_get_method_with_query_params(app: Sanic):
    @app.get("/query")
    def handler(request):
        return text(f"Query param: {request.args.get('param', 'not provided')}")

    request, response = app.test_client.get("/query?param=test")
    assert response.text == "Query param: test"
    assert response.status == 200

    request, response = app.test_client.get("/query")
    assert response.text == "Query param: not provided"
    assert response.status == 200