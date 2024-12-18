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

def test_post_method(app):
    request, response = app.test_client.post("/hello/")
    assert response.text == "OK"

def test_post_method_with_slash(app):
    request, response = app.test_client.post("/hello")
    assert response.status == 404

def test_post_method_invalid_route(app):
    request, response = app.test_client.post("/invalid_route")
    assert response.status == 404

def test_post_method_with_data(app):
    request, response = app.test_client.post("/hello/", data={"key": "value"})
    assert response.text == "OK"

def test_post_method_empty_body(app):
    request, response = app.test_client.post("/hello/", data="")
    assert response.text == "OK"