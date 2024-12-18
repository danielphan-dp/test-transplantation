import asyncio
import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import URLBuildError

def test_get_method():
    app = Sanic("app")

    @app.route("/get", methods=["GET"])
    async def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get("/get")
    assert response.text == "I am get method"

    request, response = app.test_client.post("/get")
    assert response.status == 405  # Method not allowed

    request, response = app.test_client.put("/get")
    assert response.status == 405  # Method not allowed

    request, response = app.test_client.delete("/get")
    assert response.status == 405  # Method not allowed

    assert app.url_for("get_method") == "/get"
    with pytest.raises(URLBuildError):
        app.url_for("non_existent_route")