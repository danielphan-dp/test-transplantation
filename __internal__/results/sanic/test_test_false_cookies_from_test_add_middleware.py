import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('request_data, expected_response', [
    (None, "I am get method"),
    ({"param": "value"}, "I am get method"),
])
def test_get_method_response(request_data, expected_response):
    app = Sanic("test_app")

    @app.get("/")
    async def handler(request):
        return text("I am get method")

    request, response = app.test_client.get("/", json=request_data)
    
    assert response.text == expected_response
    assert response.status == 200

@pytest.mark.parametrize('request_data', [
    ({"invalid_param": "value"}),
])
def test_get_method_invalid_request(request_data):
    app = Sanic("test_app")

    @app.get("/")
    async def handler(request):
        return text("I am get method")

    request, response = app.test_client.get("/", json=request_data)
    
    assert response.text == "I am get method"
    assert response.status == 200