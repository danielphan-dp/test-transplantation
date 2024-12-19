import pytest
from sanic import Sanic
from sanic.response import text
from sanic.request import Request
from sanic.blueprints import Blueprint

AUTH = "valid_auth_token"

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
    header = {"authorization": " ".join(["Basic", AUTH])}
    
    _, response = app.test_client.patch("/patch", headers=header)
    assert response.text == "I am patch method"
    
    _, response = app.test_client.patch("/patch")
    assert response.status == 401

    _, response = app.test_client.patch("/patch", headers={})
    assert response.status == 401

    _, response = app.test_client.patch("/patch", headers={"authorization": "InvalidToken"})
    assert response.status == 401