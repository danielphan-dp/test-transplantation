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

def test_url_for_with_query_parameters(app):
    @app.route("/query_view/")
    def query_view(request):
        return text("Query View")

    assert app.url_for("query_view", param1="value1", param2="value2") == "/query_view/?param1=value1&param2=value2"

def test_url_for_with_forwarded_request(app):
    @app.get("/forwarded_view/")
    def forwarded_view(request):
        return text("Forwarded View")

    app.config.SERVER_NAME = "my-server"
    app.config.PROXIES_COUNT = 1
    request, response = app.test_client.get(
        "/",
        headers={
            "X-Forwarded-For": "127.1.2.3",
            "X-Forwarded-Proto": "https",
            "X-Forwarded-Port": "6789",
        },
    )
    assert app.url_for("forwarded_view") == "/forwarded_view"
    assert (
        app.url_for("forwarded_view", _external=True)
        == "http://my-server/forwarded_view"
    )
    assert (
        request.url_for("forwarded_view") == "https://my-server:6789/forwarded_view"
    )