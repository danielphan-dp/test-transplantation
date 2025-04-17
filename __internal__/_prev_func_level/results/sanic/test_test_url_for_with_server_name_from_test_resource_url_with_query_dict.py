import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import URLBuildError

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_url_for_without_server_name(app):
    @app.route("/myurl")
    def passes(request):
        return text("this should pass")

    url = app.url_for("passes", _server=None, _external=True)
    assert url == "http://localhost/myurl"
    request, response = app.test_client.get(url)
    assert response.status == 200
    assert response.text == "this should pass"

def test_url_for_with_invalid_endpoint(app):
    with pytest.raises(URLBuildError) as e:
        app.url_for("non_existent_endpoint")
        assert e.match("Endpoint with name `app.non_existent_endpoint` was not found")

def test_url_for_with_query_params(app):
    @app.route("/myurl")
    def passes(request):
        return text("this should pass")

    url = app.url_for("passes", param1="value1", param2="value2")
    assert url == "http://localhost/myurl?param1=value1&param2=value2"
    request, response = app.test_client.get(url)
    assert response.status == 200
    assert response.text == "this should pass"

def test_url_for_with_path_params(app):
    @app.route("/myurl/<param>")
    def passes(request, param):
        return text(f"this should pass with param: {param}")

    url = app.url_for("passes", param="test")
    assert url == "http://localhost/myurl/test"
    request, response = app.test_client.get(url)
    assert response.status == 200
    assert response.text == "this should pass with param: test"