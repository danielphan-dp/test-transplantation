import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import URLBuildError

@pytest.fixture
def app():
    return Sanic("test_app")

def test_head_method_empty_response(app):
    @app.head("/head")
    def handler(request):
        return text('', headers={'method': 'HEAD'})

    request, response = app.test_client.head("/head")
    assert response.data == b''
    assert response.headers['method'] == 'HEAD'

def test_head_method_with_invalid_route(app):
    with pytest.raises(URLBuildError):
        app.url_for("non_existent_route")

def test_head_method_route_name(app):
    @app.head("/head", name="route_head")
    def handler(request):
        return text('', headers={'method': 'HEAD'})

    assert app.router.routes_all[("head",)].name == "app.route_head"
    assert app.url_for("route_head") == "/head"