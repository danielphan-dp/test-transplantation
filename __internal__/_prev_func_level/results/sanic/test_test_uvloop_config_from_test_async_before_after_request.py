import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('use', (False, True))
def test_get_method(app: Sanic, monkeypatch, use):
    @app.get("/get", name="get_method")
    def get_handler(request):
        return text('I am get method')

    app.config["USE_UVLOOP"] = use
    request, response = app.test_client.get("/get")
    
    assert response.status == 200
    assert response.text == 'I am get method'

    if OS_IS_WINDOWS:
        assert not app.config["USE_UVLOOP"]
    else:
        assert app.config["USE_UVLOOP"] == use

    # Additional edge case: Test with invalid route
    request, response = app.test_client.get("/invalid_route")
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

    # Test with a different method (POST)
    request, response = app.test_client.post("/get")
    assert response.status == 405
    assert "Method POST not allowed for URL /get" in response.text