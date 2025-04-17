import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.route("/get")
    async def get_method(request):
        return text("I am get method")

    return app

@pytest.mark.parametrize("url, expected_response", [
    ("/get", "I am get method"),
    ("/non_existent", "Not Found"),
])
def test_get_method(app, url, expected_response):
    request, response = app.test_client.get(url)
    
    if url == "/get":
        assert response.text == expected_response
    else:
        assert response.status == 404
        assert "Not Found" in response.text

def test_get_method_with_invalid_method(app):
    request, response = app.test_client.post("/get")
    assert response.status == 405
    assert "Method POST not allowed for URL /get" in response.text

def test_get_method_with_headers(app):
    headers = {"Custom-Header": "Test"}
    request, response = app.test_client.get("/get", headers=headers)
    assert response.text == "I am get method"
    assert response.status == 200
    assert request.headers.get("Custom-Header") == "Test"