import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")

    @app.route("/put", methods=["PUT"])
    async def put_method(request):
        return text("I am put method")

    return app

def test_put_method(app):
    request, response = app.test_client.put("/put")
    assert response.text == "I am put method"

def test_put_method_with_data(app):
    request, response = app.test_client.put("/put", data="Sample Data")
    assert response.text == "I am put method"

def test_put_method_with_invalid_route(app):
    request, response = app.test_client.put("/invalid")
    assert response.status == 404

def test_put_method_with_empty_body(app):
    request, response = app.test_client.put("/put", data="")
    assert response.text == "I am put method"