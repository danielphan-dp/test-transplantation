import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import URLBuildError

@pytest.fixture
def app():
    app = Sanic("app")

    @app.route("/url-for", name="url_for")
    def url_for(request):
        return text('url-for')

    return app

def test_url_for_with_valid_route(app):
    assert app.url_for("url_for") == "/url-for"
    request, response = app.test_client.get("/url-for")
    assert response.status == 200
    assert response.text == "url-for"

def test_url_for_with_invalid_route(app):
    with pytest.raises(URLBuildError) as e:
        app.url_for("non_existent_route")
        e.match("Endpoint with name `app.non_existent_route` was not found")

def test_url_for_with_query_params(app):
    @app.route("/url-for-with-params", methods=["GET"], name="url_for_with_params")
    def url_for_with_params(request):
        return text('url-for with params')

    assert app.url_for("url_for_with_params", param1="value1") == "/url-for-with-params?param1=value1"
    request, response = app.test_client.get("/url-for-with-params?param1=value1")
    assert response.status == 200
    assert response.text == "url-for with params"

def test_url_for_with_multiple_params(app):
    @app.route("/url-for-multiple-params", methods=["GET"], name="url_for_multiple_params")
    def url_for_multiple_params(request):
        return text('url-for multiple params')

    assert app.url_for("url_for_multiple_params", param1="value1", param2="value2") == "/url-for-multiple-params?param1=value1&param2=value2"
    request, response = app.test_client.get("/url-for-multiple-params?param1=value1&param2=value2")
    assert response.status == 200
    assert response.text == "url-for multiple params"