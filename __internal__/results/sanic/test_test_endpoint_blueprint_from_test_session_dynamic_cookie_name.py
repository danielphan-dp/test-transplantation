import pytest
from sanic import Sanic
from sanic.response import text

def test_get_method():
    app = Sanic("test_app")

    @app.route("/get", methods=["GET"])
    def get_method(request):
        return text("I am get method")

    request, response = app.test_client.get("/get")

    assert response.status == 200
    assert response.text == "I am get method"
    assert request.method == "GET"
    assert request.path == "/get"