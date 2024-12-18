import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('max_age', [30.0, 30.1, 'test'])
def test_get_method(app, max_age):
    @app.get("/")
    def handler(request):
        return text("I am get method")

    request, response = app.test_client.get("/")
    assert response.status == 200
    assert response.text == "I am get method"

@pytest.mark.parametrize('max_age', [None, -1, 0])
def test_get_method_with_invalid_max_age(app, max_age):
    @app.get("/")
    def handler(request):
        response = text("I am get method")
        if max_age is not None:
            response.cookies["test"]["max-age"] = max_age
        return response

    request, response = app.test_client.get("/")
    assert response.status == 200
    assert response.text == "I am get method"