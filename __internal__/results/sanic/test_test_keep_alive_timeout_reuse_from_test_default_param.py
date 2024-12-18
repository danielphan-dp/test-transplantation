import asyncio
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.skipif(bool(os.environ.get('SANIC_NO_UVLOOP')) or platform.system() == 'Windows', reason='Not testable with current client')
def test_get_method_response(app):
    """Test the response of the GET method in the DummyView."""
    class DummyView:
        def get(self, request):
            return text('I am get method')

    app.add_route(DummyView().get, "/get")

    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_with_invalid_route(app):
    """Test the response for an invalid route."""
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_custom_header(app):
    """Test the GET method with a custom header."""
    class DummyView:
        def get(self, request):
            return text('I am get method')

    app.add_route(DummyView().get, "/get")

    headers = {"Custom-Header": "Test"}
    request, response = app.test_client.get("/get", headers=headers)
    assert response.status == 200
    assert response.text == "I am get method"