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
        assert str(e.value) == "Endpoint with name `non_existent_view` was not found"

def test_url_for_with_different_schemes(app):
    @app.route("/secure_view")
    def secure_view(request):
        return text("Secure View")

    request, response = app.test_client.get(
        "/",
        headers={
            "X-Forwarded-Proto": "https",
            "X-Forwarded-Port": "443",
        },
    )
    assert request.url_for("secure_view") == "https://localhost/secure_view"

    request, response = app.test_client.get(
        "/",
        headers={
            "X-Forwarded-Proto": "http",
            "X-Forwarded-Port": "80",
        },
    )
    assert request.url_for("secure_view") == "http://localhost/secure_view"

def test_url_for_with_custom_server_name(app):
    app.config.SERVER_NAME = "custom-server"
    
    @app.route("/custom_view")
    def custom_view(request):
        return text("Custom View")

    assert app.url_for("custom_view", _external=True) == "http://custom-server/custom_view"