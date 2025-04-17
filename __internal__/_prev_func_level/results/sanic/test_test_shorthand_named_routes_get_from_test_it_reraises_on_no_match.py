import asyncio
import pytest
from sanic import Sanic
from sanic.blueprints import Blueprint
from sanic.exceptions import URLBuildError
from sanic.response import text

def test_get_method_response():
    app = Sanic("app")

    @app.get("/get")
    def handler(request):
        return text("I am get method")

    request, response = app.test_client.get("/get")
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_invalid_route():
    app = Sanic("app")

    @app.get("/get")
    def handler(request):
        return text("I am get method")

    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_blueprint():
    app = Sanic("app")
    bp = Blueprint("test_bp", url_prefix="/bp")

    @bp.get("/get")
    def handler(request):
        return text("Blueprint")

    app.blueprint(bp)

    request, response = app.test_client.get("/bp/get")
    assert response.text == "Blueprint"
    assert response.status == 200

def test_get_method_no_match():
    app = Sanic("app")

    @app.get("/get")
    def handler(request):
        return text("I am get method")

    with pytest.raises(URLBuildError):
        app.url_for("non_existent_route")