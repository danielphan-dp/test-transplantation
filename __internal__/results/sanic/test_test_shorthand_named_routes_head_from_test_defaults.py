import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import URLBuildError

def test_head_method():
    app = Sanic("app")

    @app.head("/head", name="route_head")
    def handler(request):
        return text("OK")

    # Test if the route is correctly registered
    assert app.router.routes_all[("head",)].name == "app.route_head"
    assert app.url_for("route_head") == "/head"

    # Test the HEAD request
    request, response = app.test_client.head("/head")
    assert response.status == 200
    assert response.text == ''
    assert response.headers['method'] == 'HEAD'

    # Test URL building for non-existent handler
    with pytest.raises(URLBuildError):
        app.url_for("non_existent_handler")

    # Test HEAD request to a non-existent route
    request, response = app.test_client.head("/non_existent")
    assert response.status == 404

    # Test HEAD request with additional headers
    request, response = app.test_client.head("/head", headers={"X-Custom-Header": "value"})
    assert response.headers.get("X-Custom-Header") is None  # HEAD should not return body or custom headers

    # Test if the method is indeed HEAD
    assert response.headers['method'] == 'HEAD'