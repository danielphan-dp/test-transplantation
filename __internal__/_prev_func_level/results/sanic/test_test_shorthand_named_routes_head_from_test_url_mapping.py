import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import URLBuildError

@pytest.fixture
def app():
    return Sanic("test_app")

def test_head_method(app):
    @app.head("/head", name="route_head")
    def handler(request):
        return text("OK")

    assert app.router.routes_all[("head",)].name == "test_app.route_head"
    assert app.url_for("route_head") == "/head"

    # Test HEAD request
    request, response = app.test_client.head("/head")
    assert response.status == 200
    assert not response.body  # HEAD should not return a body

    # Test invalid URL for URLBuildError
    with pytest.raises(URLBuildError):
        app.url_for("non_existent_handler")

def test_head_empty_response(app):
    @app.head("/empty", name="route_empty")
    def empty_handler(request):
        return text('', headers={'method': 'HEAD'})

    assert app.router.routes_all[("head",)].name == "test_app.route_empty"
    request, response = app.test_client.head("/empty")
    assert response.status == 200
    assert not response.body  # HEAD should not return a body

def test_head_with_custom_header(app):
    @app.head("/custom-header", name="route_custom_header")
    def custom_header_handler(request):
        return text('', headers={'X-Custom-Header': 'value'})

    request, response = app.test_client.head("/custom-header")
    assert response.status == 200
    assert response.headers['X-Custom-Header'] == 'value'