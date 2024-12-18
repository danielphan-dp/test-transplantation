import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('url', ["/", "/myurl"])
def test_get_method(app, url):
    @app.route(url)
    class DummyView:
        def get(self, request):
            return text("I am get method")

    request, response = app.test_client.get(url)
    assert response.status == 200
    assert response.text == "I am get method"

@pytest.mark.parametrize('url', ["/nonexistent", "/myurl"])
def test_get_method_not_found(app, url):
    @app.route("/myurl")
    class DummyView:
        def get(self, request):
            return text("I am get method")

    request, response = app.test_client.get(url)
    if url == "/nonexistent":
        assert response.status == 404
        assert "Requested URL" in response.text

@pytest.mark.parametrize('url', ["/myurl"])
def test_get_method_with_different_routes(app, url):
    @app.route(url)
    class DummyView:
        def get(self, request):
            return text("I am get method")

    request, response = app.test_client.get(url)
    assert response.status == 200
    assert response.text == "I am get method"