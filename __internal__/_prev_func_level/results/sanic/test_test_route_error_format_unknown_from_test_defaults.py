import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import SanicException

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/text")
    def handler(request):
        return text('I am get method')

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/text")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_custom_header(app):
    request, response = app.test_client.get("/text", headers={"X-Custom-Header": "value"})
    assert response.status == 200
    assert response.text == 'I am get method'
    assert response.headers.get("X-Custom-Header") is None

def test_get_method_with_query_params(app):
    request, response = app.test_client.get("/text?foo=bar")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_error_format_unknown(app):
    with pytest.raises(SanicException, match="Unknown format: bad"):
        @app.get("/text", error_format="bad")
        def handler(request):
            return text('I am get method')