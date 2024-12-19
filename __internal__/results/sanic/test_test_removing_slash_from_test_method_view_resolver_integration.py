import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")

    @app.post("/rest/<resource>")
    async def post(request, resource):
        return text('I am post method')

    return app

def test_post_method(app):
    request, response = app.test_client.post("/rest/test_resource")
    assert response.text == 'I am post method'
    assert response.status == 200

def test_post_method_with_invalid_resource(app):
    request, response = app.test_client.post("/rest/")
    assert response.status == 404

def test_post_method_with_empty_resource(app):
    request, response = app.test_client.post("/rest/")
    assert response.status == 404

def test_post_method_with_data(app):
    request, response = app.test_client.post("/rest/test_resource", json={"key": "value"})
    assert response.text == 'I am post method'
    assert response.status == 200

def test_post_method_with_invalid_method(app):
    request, response = app.test_client.get("/rest/test_resource")
    assert response.status == 405
    assert "Method GET not allowed for URL /rest/test_resource" in response.text