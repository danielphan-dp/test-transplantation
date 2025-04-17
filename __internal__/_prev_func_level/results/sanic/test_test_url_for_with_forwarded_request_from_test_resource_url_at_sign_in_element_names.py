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

def test_url_for_with_different_ports(app):
    app.config.SERVER_NAME = "my-server:8080"
    
    @app.route("/another_view/")
    def another_view(request):
        return text("Another View")

    assert app.url_for("another_view") == "/another_view"
    assert app.url_for("another_view", _external=True) == "http://my-server:8080/another_view"

def test_url_for_with_custom_headers(app):
    @app.route("/custom_view/")
    def custom_view(request):
        return text("Custom View")

    request, response = app.test_client.get(
        "/custom_view/",
        headers={
            "X-Forwarded-For": "192.168.1.1",
            "X-Forwarded-Proto": "http",
            "X-Forwarded-Port": "8080",
        },
    )
    assert request.url_for("custom_view") == "http://my-server:8080/custom_view"