import pytest
from sanic import Sanic
from sanic.response import text
from sanic.request import Request

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_get_method(app):
    @app.route("/get_test", methods=["GET"])
    def get_method(request: Request):
        return text("I am get method")

    _, response = app.test_client.get("/get_test")
    assert response.text == "I am get method"

def test_get_method_unauthorized(app):
    @app.route("/get_test", methods=["GET"])
    def get_method(request: Request):
        return text("I am get method")

    _, response = app.test_client.get("/get_test", headers={"authorization": "Invalid"})
    assert response.text == "I am get method"  # Assuming no auth check in get method

def test_get_method_with_query_params(app):
    @app.route("/get_test", methods=["GET"])
    def get_method(request: Request):
        return text(f"I am get method with query param: {request.args.get('param')}")

    _, response = app.test_client.get("/get_test?param=test")
    assert response.text == "I am get method with query param: test"