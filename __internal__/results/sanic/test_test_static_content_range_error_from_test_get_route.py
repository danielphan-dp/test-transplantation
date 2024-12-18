import pytest
from sanic import Sanic
from sanic.response import text
from sanic.blueprints import Blueprint

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt'])
def test_get_method_response(app, file_name, static_file_directory):
    app = Sanic("test_app")

    class DummyView:
        def get(self, request):
            return text('I am get method')

    app.add_route(DummyView().get, "/get")

    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == 'I am get method'

    # Test with additional headers
    headers = {"Custom-Header": "value"}
    request, response = app.test_client.get("/get", headers=headers)
    assert response.status == 200
    assert response.text == 'I am get method'
    assert response.headers["Custom-Header"] == "value"

    # Test with invalid route
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

    # Test with query parameters
    request, response = app.test_client.get("/get?param=value")
    assert response.status == 200
    assert response.text == 'I am get method'