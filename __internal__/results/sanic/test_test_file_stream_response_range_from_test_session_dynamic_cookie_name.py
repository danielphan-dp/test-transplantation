import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize("url", ["/", "/test", "/another_test"])
def test_get_method(app: Sanic, url):
    @app.route(url, methods=["GET"])
    def get_method(request):
        return text("I am get method")

    request, response = app.test_client.get(url)
    assert response.status == 200
    assert response.text == "I am get method"

@pytest.mark.parametrize("url", ["/nonexistent", "/invalid"])
def test_get_method_invalid_url(app: Sanic, url):
    @app.route("/valid", methods=["GET"])
    def valid_get(request):
        return text("I am valid get method")

    request, response = app.test_client.get(url)
    assert response.status == 404
    assert "Requested URL" in response.text

def test_get_method_with_query_params(app: Sanic):
    @app.route("/query", methods=["GET"])
    def get_with_query(request):
        param = request.args.get("param", "default")
        return text(f"Query param is {param}")

    request, response = app.test_client.get("/query?param=test")
    assert response.status == 200
    assert response.text == "Query param is test"

    request, response = app.test_client.get("/query")
    assert response.status == 200
    assert response.text == "Query param is default"