import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

@pytest.mark.parametrize('path,strict,expected', [
    ('/url-for', False, '/url-for'),
    ('/url-for/', False, '/url-for'),
    ('/url-for', True, '/url-for'),
    ('/url-for/', True, '/url-for/'),
])
def test_url_for_with_trailing_slash(app, path, strict, expected):
    @app.route(path, strict_slashes=strict)
    def handler(request):
        return text('url-for')

    url = app.url_for("handler")
    assert url == expected

    request, response = app.test_client.get(url)
    assert response.status == 200
    assert response.text == 'url-for'

def test_url_for_with_server_name(app):
    server_name = "example.com"
    app.config.update({"SERVER_NAME": server_name})
    path = "/url-for"

    @app.route(path)
    def handler(request):
        return text('url-for')

    url = f"http://{server_name}{path}"
    assert url == app.url_for("handler", _server=None, _external=True)
    request, response = app.test_client.get(url)
    assert response.status == 200
    assert response.text == 'url-for'

def test_fails_if_endpoint_not_found(app):
    @app.route("/url-for")
    def handler(request):
        return text('url-for')

    with pytest.raises(Exception) as e:
        app.url_for("non_existent_handler")
        assert "Endpoint with name `non_existent_handler` was not found" in str(e.value)

def test_fails_url_build_if_param_not_passed(app):
    @app.route("/<param>")
    def handler(request, param):
        return text(param)

    with pytest.raises(Exception) as e:
        app.url_for("handler")
        assert "Required parameter `param` was not passed to url_for" in str(e.value)