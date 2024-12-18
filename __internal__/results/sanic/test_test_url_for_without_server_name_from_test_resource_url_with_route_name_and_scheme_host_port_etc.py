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

def test_url_for_with_external_url(app):
    request, response = app.test_client.get("/url-for")
    assert response.status == 200
    assert response.text == "url-for"

    url = app.url_for("url_for", _external=True)
    assert url == f"http://127.0.0.1:{request.server_port}/url-for"

def test_url_for_with_invalid_view_name(app):
    with pytest.raises(Exception) as e:
        app.url_for("non_existent_view")
    assert "Endpoint with name `non_existent_view` was not found" in str(e.value)

def test_url_for_with_query_params(app):
    @app.route("/query")
    def query_view(request):
        return text("query response")

    request, response = app.test_client.get("/query")
    assert response.status == 200
    url = app.url_for("query_view", param1="value1", param2="value2")
    assert url == f"http://127.0.0.1:{request.server_port}/query?param1=value1&param2=value2"

def test_url_for_with_server_name(app):
    server_name = "example.com"
    app.config.update({"SERVER_NAME": server_name})

    url = app.url_for("url_for", _external=True)
    assert url == f"http://{server_name}/url-for"