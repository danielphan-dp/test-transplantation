import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.route("/url-for")
    def url_for(request):
        return text("url-for")

    return app

def test_url_for_with_server_name(app):
    server_name = "example.com"
    app.config.update({"SERVER_NAME": server_name})
    request, response = app.test_client.get("/url-for")
    assert response.text == "url-for"
    assert response.status == 200
    expected_url = f"http://{server_name}:{request.server_port}/url-for"
    assert request.url_for("url_for") == expected_url

def test_url_for_without_server_name(app):
    request, response = app.test_client.get("/url-for")
    assert response.text == "url-for"
    assert response.status == 200
    expected_url = f"http://127.0.0.1:{request.server_port}/url-for"
    assert request.url_for("url_for") == expected_url

def test_url_for_invalid_view_name(app):
    with pytest.raises(Exception) as e:
        app.url_for("non_existent_view")
    assert "Endpoint with name `non_existent_view` was not found" in str(e.value)