import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import URLBuildError

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_url_for_basic(app):
    @app.route("/url-for", name="url_for")
    async def handler(request):
        return text("url-for")

    assert app.url_for("url_for") == "/url-for"
    request, response = app.test_client.get("/url-for")
    assert response.status == 200
    assert response.text == "url-for"

def test_url_for_with_nonexistent_endpoint(app):
    with pytest.raises(URLBuildError) as e:
        app.url_for("nonexistent")
        e.match("Endpoint with name `app.nonexistent` was not found")

def test_url_for_with_query_params(app):
    @app.route("/url-for", methods=["GET"], name="url_for_with_params")
    async def handler(request):
        return text("url-for with params")

    url = app.url_for("url_for_with_params", param1="value1", param2="value2")
    assert url == "/url-for?param1=value1&param2=value2"
    request, response = app.test_client.get(url)
    assert response.status == 200
    assert response.text == "url-for with params"

def test_url_for_with_missing_params(app):
    @app.route("/folder/<folder_id>", name="folder_route")
    async def handler(request, folder_id):
        return text(f"Folder ID: {folder_id}")

    with pytest.raises(URLBuildError) as e:
        app.url_for("folder_route")
        e.match("Required parameter `folder_id` was not passed to url_for")