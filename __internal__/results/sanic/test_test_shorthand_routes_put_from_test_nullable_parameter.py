import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")

    @app.put("/put")
    def handler(request):
        return text("I am put method")

    return app

def test_put_method(app):
    request, response = app.test_client.put("/put")
    assert response.text == "I am put method"

def test_put_method_invalid_method(app):
    request, response = app.test_client.get("/put")
    assert response.status == 405

def test_put_method_with_data(app):
    request, response = app.test_client.put("/put", data="Test Data")
    assert response.text == "I am put method"

def test_put_method_empty_body(app):
    request, response = app.test_client.put("/put", data="")
    assert response.text == "I am put method"

def test_put_method_with_headers(app):
    headers = {"Custom-Header": "Value"}
    request, response = app.test_client.put("/put", headers=headers)
    assert response.text == "I am put method"