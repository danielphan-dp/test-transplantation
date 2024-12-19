import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('url', ["/", "/test"])
def test_get_method(app: Sanic, url):
    @app.get(url)
    def handler(request):
        return text("I am get method")

    request, response = app.test_client.get(url)
    assert response.text == "I am get method"
    assert response.status == 200

@pytest.mark.parametrize('url', ["/nonexistent", "/invalid"])
def test_get_method_invalid_url(app: Sanic, url):
    request, response = app.test_client.get(url)
    assert response.status == 404
    assert "Requested URL" in response.text

def test_get_method_with_query_params(app: Sanic):
    @app.get("/query")
    def handler(request):
        return text(f"Query params: {request.args}")

    request, response = app.test_client.get("/query?param1=value1&param2=value2")
    assert response.text == "Query params: {'param1': ['value1'], 'param2': ['value2']}"
    assert response.status == 200

def test_get_method_with_headers(app: Sanic):
    @app.get("/headers")
    def handler(request):
        return text(f"Headers: {request.headers}")

    request, response = app.test_client.get("/headers", headers={"Custom-Header": "value"})
    assert response.text == "Headers: {'host': 'localhost', 'custom-header': 'value'}"
    assert response.status == 200