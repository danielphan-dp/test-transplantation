import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('unquote', [True, False])
def test_get_method(app, unquote):
    class DummyView:
        def get(self, request):
            return text('I am get method')

    app.add_route(DummyView().get, "/get")

    request, response = app.test_client.get("/get")
    assert response.text == "I am get method"

    # Test with unquoted URL
    if unquote:
        request, response = app.test_client.get("/get")
        assert response.text == "I am get method"
    else:
        request, response = app.test_client.get("/%67%65%74")
        assert response.text == "I am get method"  # Assuming URL encoding for "/get" is used

    # Test for method not allowed
    request, response = app.test_client.post("/get")
    assert response.status == 405
    assert "Method POST not allowed for URL /get" in response.text

    # Test for invalid route
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text