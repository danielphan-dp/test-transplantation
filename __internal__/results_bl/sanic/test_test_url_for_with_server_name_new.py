import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_url_for_without_server_name(app):
    path = "/test-url"
    
    @app.route(path)
    def test_route(request):
        return text("test route response")

    url = app.url_for("test_route", _server=None, _external=True)
    assert url == f"http://localhost{path}"
    request, response = app.test_client.get(url)
    assert response.status == 200
    assert response.text == "test route response"

def test_url_for_invalid_route(app):
    with pytest.raises(Exception):
        app.url_for("non_existent_route")

def test_url_for_with_different_path(app):
    path = "/another-url"
    
    @app.route(path)
    def another_route(request):
        return text("another route response")

    url = app.url_for("another_route", _server=None, _external=True)
    assert url == f"http://localhost{path}"
    request, response = app.test_client.get(url)
    assert response.status == 200
    assert response.text == "another route response"

def test_url_for_with_query_parameters(app):
    path = "/query-url"
    
    @app.route(path)
    def query_route(request):
        return text("query response")

    url = app.url_for("query_route", _server=None, _external=True, param1="value1", param2="value2")
    assert url == "http://localhost/query-url?param1=value1&param2=value2"
    request, response = app.test_client.get(url)
    assert response.status == 200
    assert response.text == "query response"