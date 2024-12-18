import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_url_for_with_default_server_name(app):
    @app.route("/url-for")
    def url_for_handler(request):
        return text("url-for")

    app.config.SERVER_NAME = "my-server"
    expected_url = "http://my-server/url-for"
    assert app.url_for("url_for_handler", _external=True) == expected_url

    request, response = app.test_client.get("/url-for")
    assert request.url_for("url_for_handler") == expected_url

def test_url_for_with_https_server_name(app):
    @app.route("/url-for")
    def url_for_handler(request):
        return text("url-for")

    app.config.SERVER_NAME = "https://my-server/path"
    expected_url = "https://my-server/path/url-for"
    assert app.url_for("url_for_handler", _external=True) == expected_url

    request, response = app.test_client.get("/url-for")
    assert request.url_for("url_for_handler") == expected_url

def test_url_for_with_no_server_name(app):
    @app.route("/url-for")
    def url_for_handler(request):
        return text("url-for")

    app.config.SERVER_NAME = None
    expected_url = "http://localhost:8000/url-for"  # Assuming default port
    assert app.url_for("url_for_handler", _external=True) == expected_url

    request, response = app.test_client.get("/url-for")
    assert request.url_for("url_for_handler") == expected_url

def test_url_for_with_invalid_endpoint(app):
    with pytest.raises(Exception) as e:
        app.url_for("non_existent_handler")
        assert "Endpoint with name `non_existent_handler` was not found" in str(e.value)