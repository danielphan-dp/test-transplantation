import pytest
from sanic import Sanic
from sanic.response import text
from sanic.request import Request
from sanic.blueprints import Blueprint

@pytest.fixture
def app():
    app = Sanic("TestApp")
    blueprint = Blueprint("test_blueprint")

    @blueprint.route("/patch", methods=["PATCH"])
    def patch_method(request: Request):
        return text("I am patch method")

    app.blueprint(blueprint)
    return app

def test_patch_method(app):
    _, response = app.test_client.patch("/patch")
    assert response.status == 200
    assert response.text == "I am patch method"

def test_patch_method_with_invalid_data(app):
    _, response = app.test_client.patch("/patch", data={"invalid": "data"})
    assert response.status == 200
    assert response.text == "I am patch method"

def test_patch_method_without_auth(app):
    _, response = app.test_client.patch("/patch")
    assert response.status == 200
    assert response.text == "I am patch method"

def test_patch_method_with_empty_body(app):
    _, response = app.test_client.patch("/patch", data="")
    assert response.status == 200
    assert response.text == "I am patch method"