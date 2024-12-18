import pytest
from sanic import Sanic
from sanic.response import text

def test_get_method():
    app = Sanic("app")

    @app.route("/get", methods=["GET"])
    async def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get("/get")
    assert response.text == "I am get method"
    assert response.status == 200

    request, response = app.test_client.post("/get")
    assert response.status == 405  # Method Not Allowed

    request, response = app.test_client.put("/get")
    assert response.status == 405  # Method Not Allowed

    request, response = app.test_client.delete("/get")
    assert response.status == 405  # Method Not Allowed

    assert app.url_for("get_method") == "/get"