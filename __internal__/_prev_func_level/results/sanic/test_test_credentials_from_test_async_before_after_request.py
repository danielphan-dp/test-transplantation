import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.route("/get")
    def get_method(request):
        return text("I am get method")

    return app

@pytest.mark.parametrize("request_path, expected_response", [
    ("/get", "I am get method"),
    ("/nonexistent", "Not Found"),
])
async def test_get_method(app, request_path, expected_response):
    request, response = await app.test_client.get(request_path)
    
    if request_path == "/get":
        assert response.text == expected_response
    else:
        assert response.status == 404
        assert "Not Found" in response.text

@pytest.mark.parametrize("request_path", [
    ("/get"),
])
async def test_get_method_with_headers(app, request_path):
    headers = {"Authorization": "Bearer some_token"}
    request, response = await app.test_client.get(request_path, headers=headers)
    
    assert response.text == "I am get method"
    assert response.status == 200

@pytest.mark.parametrize("request_path", [
    ("/get"),
])
async def test_get_method_with_invalid_method(app, request_path):
    request, response = await app.test_client.post(request_path)
    
    assert response.status == 405
    assert "Method POST not allowed for URL" in response.text