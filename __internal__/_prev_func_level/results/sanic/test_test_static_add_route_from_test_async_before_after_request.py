import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('strict_slashes', [True, False, None])
def test_get_method(app, strict_slashes):
    @app.get("/get")
    async def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get("/get", strict_slashes=strict_slashes)
    assert response.text == 'I am get method'

def test_get_method_not_found(app):
    request, response = app.test_client.get("/non_existent_route")
    assert response.status == 404
    assert "Requested URL /non_existent_route not found" in response.text

def test_get_method_with_invalid_method(app):
    @app.get("/get")
    async def get_method(request):
        return text('I am get method')

    request, response = app.test_client.post("/get")
    assert response.status == 405
    assert "Method POST not allowed for URL /get" in response.text