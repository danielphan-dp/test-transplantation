import pytest
from sanic import Sanic
from sanic.text import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    class DummyView:
        def get(self, request):
            return text("I am get method")

    app.add_route(DummyView().get, "/")
    return app

@pytest.mark.parametrize('path', ["/", "/nonexistent"])
def test_get_method(app, path):
    request, response = app.test_client.get(path)
    
    if path == "/":
        assert response.status == 200
        assert response.text == "I am get method"
    else:
        assert response.status == 404
        assert "Requested URL" in response.text

def test_get_method_with_query_params(app):
    request, response = app.test_client.get("/?param=value")
    assert response.status == 200
    assert response.text == "I am get method"