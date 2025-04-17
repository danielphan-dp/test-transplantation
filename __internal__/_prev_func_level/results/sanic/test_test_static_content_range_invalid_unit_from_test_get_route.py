import pytest
from sanic import Sanic
from sanic.text import text

@pytest.mark.parametrize('param', ['valid_param', 'another_param'])
def test_get_method_with_params(app, param):
    class DummyView:
        def get(self, request, my_param_here: str):
            return text(f"I am get method with {my_param_here}")

    app.add_route(DummyView().get, f"/{param}")

    request, response = app.test_client.get(f"/{param}")

    assert response.status == 200
    assert f"I am get method with {param}" in response.text

def test_get_method_without_params(app):
    class DummyView:
        def get(self, request):
            return text("I am get method")

    app.add_route(DummyView().get, "/")

    request, response = app.test_client.get("/")

    assert response.status == 200
    assert response.text == "I am get method"