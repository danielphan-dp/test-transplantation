import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize("url", ["/", "/test", "/another_test"])
def test_get_method(app: Sanic, url):
    @app.route(url, methods=["GET"])
    def get_route(request):
        return text("I am get method")

    request, response = app.test_client.get(url)
    assert response.status == 200
    assert response.text == "I am get method"

@pytest.mark.parametrize("url", ["/invalid", "/not_found"])
def test_get_method_not_found(app: Sanic, url):
    @app.route("/valid", methods=["GET"])
    def valid_route(request):
        return text("I am get method")

    request, response = app.test_client.get(url)
    assert response.status == 404
    assert "Requested URL" in response.text

@pytest.mark.parametrize("url", ["/", "/test"])
def test_get_method_with_middleware(app: Sanic, url):
    results = []

    @app.middleware
    async def handler(request):
        results.append(request)

    @app.route(url, methods=["GET"])
    def get_route(request):
        return text("I am get method")

    request, response = app.test_client.get(url)
    assert response.text == "I am get method"
    assert len(results) == 1
    assert results[0].url == url

@pytest.mark.parametrize("url", ["/", "/test"])
def test_get_method_with_custom_response(app: Sanic, url):
    @app.route(url, methods=["GET"])
    def get_route(request):
        return text("Custom response", status=201)

    request, response = app.test_client.get(url)
    assert response.status == 201
    assert response.text == "Custom response"