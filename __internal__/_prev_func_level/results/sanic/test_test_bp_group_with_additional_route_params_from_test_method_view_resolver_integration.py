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

    @blueprint.route("/put_test", methods=["PUT"])
    def put_method(request: Request):
        return text("I am put method")

    app.blueprint(blueprint)
    return app

def test_put_method_success(app):
    header = {"authorization": "Basic " + AUTH}
    _, response = app.test_client.put("/put_test", headers=header)
    assert response.text == "I am put method"

def test_put_method_unauthorized(app):
    _, response = app.test_client.put("/put_test")
    assert response.status == 401

def test_put_method_with_invalid_auth(app):
    header = {"authorization": "Basic invalid_token"}
    _, response = app.test_client.put("/put_test", headers=header)
    assert response.status == 401

def test_put_method_with_empty_body(app):
    header = {"authorization": "Basic " + AUTH}
    _, response = app.test_client.put("/put_test", headers=header, data="")
    assert response.text == "I am put method"  # Assuming the method does not depend on body content

def test_put_method_with_additional_headers(app):
    header = {"authorization": "Basic " + AUTH, "Custom-Header": "value"}
    _, response = app.test_client.put("/put_test", headers=header)
    assert response.text == "I am put method"