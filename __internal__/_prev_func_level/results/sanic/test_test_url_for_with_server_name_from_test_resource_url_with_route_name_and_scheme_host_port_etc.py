import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import URLBuildError

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_url_for_with_server_name_and_params(app):
    server_name = "test_host:8080"
    app.config.update({"SERVER_NAME": server_name})
    path = "/myurl"

    @app.route(path)
    def passes(request):
        return text("this should pass")

    url = f"http://{server_name}{path}?param1=value1&param2=value2"
    assert url == app.url_for("passes", param1="value1", param2="value2", _server=None, _external=True)
    request, response = app.test_client.get(url)
    assert response.status == 200
    assert response.text == "this should pass"

def test_url_for_with_invalid_endpoint(app):
    server_name = "test_host:8080"
    app.config.update({"SERVER_NAME": server_name})

    with pytest.raises(URLBuildError) as e:
        app.url_for("non_existent_endpoint")
        assert e.match("Endpoint with name `app.non_existent_endpoint` was not found")

def test_url_for_with_missing_params(app):
    server_name = "test_host:8080"
    app.config.update({"SERVER_NAME": server_name})
    path = "/myurl"

    @app.route(path)
    def passes(request):
        return text("this should pass")

    with pytest.raises(URLBuildError) as e:
        app.url_for("passes", _server=None)
        assert e.match("Required parameter `param` was not passed to url_for")  # Assuming 'param' is required

def test_url_for_with_different_schemes(app):
    server_name = "test_host:8080"
    app.config.update({"SERVER_NAME": server_name})
    path = "/myurl"

    @app.route(path)
    def passes(request):
        return text("this should pass")

    url_http = f"http://{server_name}{path}"
    url_https = f"https://{server_name}{path}"
    
    assert url_http == app.url_for("passes", _server=None, _external=True, _scheme="http")
    assert url_https == app.url_for("passes", _server=None, _external=True, _scheme="https")

    request_http, response_http = app.test_client.get(url_http)
    assert response_http.status == 200
    assert response_http.text == "this should pass"

    request_https, response_https = app.test_client.get(url_https)
    assert response_https.status == 200
    assert response_https.text == "this should pass"