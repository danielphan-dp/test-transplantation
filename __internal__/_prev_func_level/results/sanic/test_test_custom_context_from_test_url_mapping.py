import random
from sanic.response import json, text
from ujson import loads

def test_get_method(app):
    class DummyView:
        def get(self, request):
            return text('I am get method')

    app.add_route(DummyView().get, "/get")

    request, response = app.test_client.get("/get")
    assert response.text == "I am get method"

    # Test for non-existent route
    request, response = app.test_client.get("/non_existent")
    assert response.status == 404
    assert "Requested URL /non_existent not found" in response.text

    # Test for method not allowed
    request, response = app.test_client.post("/get")
    assert response.status == 405
    assert "Method POST not allowed for URL /get" in response.text

    # Test with additional middleware
    @app.middleware("request")
    async def add_custom_header(request):
        request.headers['X-Custom-Header'] = 'TestHeader'

    request, response = app.test_client.get("/get")
    assert response.headers['X-Custom-Header'] == 'TestHeader'