import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('unquote', [True, False, None])
def test_get_method(app, unquote):
    class DummyView:
        def get(self, request):
            return text('I am get method')

    app.add_route(DummyView().get, "/")

    request, response = app.test_client.get("/")
    assert response.status == 200
    assert response.text == 'I am get method'

    # Test with unquoted URL
    if unquote:
        request, response = app.test_client.get("/%E5%95%8A")
        assert response.status == 200
        assert response.text == 'I am get method'
    
    # Test with invalid route
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

    # Test with method not allowed
    request, response = app.test_client.post("/")
    assert response.status == 405
    assert "Method POST not allowed for URL /" in response.text