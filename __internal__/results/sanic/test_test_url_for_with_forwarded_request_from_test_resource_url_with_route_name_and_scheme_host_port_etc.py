import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_url_for_with_no_forwarded_request(app):
    @app.route("/test_view")
    def test_view(request):
        return text("Test View")

    assert app.url_for("test_view") == "/test_view"
    assert app.url_for("test_view", _external=True) == "http://localhost/test_view"

def test_url_for_with_invalid_view_name(app):
    with pytest.raises(Exception) as e:
        app.url_for("non_existent_view")
        assert "Endpoint with name `non_existent_view` was not found" in str(e.value)

def test_url_for_with_custom_server_name(app):
    app.config.SERVER_NAME = "custom-server"
    @app.route("/custom_view")
    def custom_view(request):
        return text("Custom View")

    assert app.url_for("custom_view", _external=True) == "http://custom-server/custom_view"

def test_url_for_with_different_ports(app):
    app.config.SERVER_NAME = "my-server"
    app.config.PROXIES_COUNT = 1
    request, response = app.test_client.get(
        "/",
        headers={
            "X-Forwarded-For": "127.1.2.3",
            "X-Forwarded-Proto": "https",
            "X-Forwarded-Port": "8080",
        },
    )
    assert request.url_for("custom_view") == "https://my-server:8080/custom_view"

def test_url_for_with_query_parameters(app):
    @app.route("/query_view")
    def query_view(request):
        return text("Query View")

    assert app.url_for("query_view", param1="value1", param2="value2") == "/query_view?param1=value1&param2=value2"