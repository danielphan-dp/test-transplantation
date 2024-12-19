import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")

    @app.post("/hello/")
    def handler_post(request):
        return text("OK")

    return app

def test_post_method_empty_body(app):
    request, response = app.test_client.post("/hello/", json={})
    assert response.text == "OK"

def test_post_method_with_data(app):
    request, response = app.test_client.post("/hello/", json={"key": "value"})
    assert response.text == "OK"

def test_post_method_invalid_route(app):
    request, response = app.test_client.post("/invalid/")
    assert response.status == 404

def test_post_method_with_query_params(app):
    request, response = app.test_client.post("/hello/?param=value")
    assert response.text == "OK"

def test_post_method_with_headers(app):
    request, response = app.test_client.post("/hello/", headers={"Custom-Header": "value"})
    assert response.text == "OK"