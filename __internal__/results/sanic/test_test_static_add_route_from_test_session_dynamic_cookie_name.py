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

    # Test with an invalid route
    request, response = app.test_client.get("/invalid_route", strict_slashes=strict_slashes)
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

    # Test with a different method
    request, response = app.test_client.post("/get", strict_slashes=strict_slashes)
    assert response.status == 405
    assert "Method POST not allowed for URL /get" in response.text