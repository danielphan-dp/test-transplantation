import pytest
from sanic import Sanic, Blueprint
from sanic.response import text
from sanic.request import Request

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_patch_method(app):
    @app.route("/patch", methods=["PATCH"])
    def patch_method(request: Request):
        return text("I am patch method")

    _, response = app.test_client.patch("/patch")
    assert response.status == 200
    assert response.text == "I am patch method"

def test_patch_method_with_data(app):
    @app.route("/patch_data", methods=["PATCH"])
    def patch_data_method(request: Request):
        return text(request.json.get("data", "No data"))

    _, response = app.test_client.patch("/patch_data", json={"data": "Test Data"})
    assert response.status == 200
    assert response.text == "Test Data"

def test_patch_method_without_data(app):
    @app.route("/patch_no_data", methods=["PATCH"])
    def patch_no_data_method(request: Request):
        return text(request.json.get("data", "No data"))

    _, response = app.test_client.patch("/patch_no_data")
    assert response.status == 200
    assert response.text == "No data"

def test_patch_method_unauthorized(app):
    @app.route("/secure_patch", methods=["PATCH"])
    def secure_patch_method(request: Request):
        auth = request.headers.get("authorization")
        if not auth or auth != "Bearer valid_token":
            return text("Unauthorized", status=401)
        return text("Authorized")

    _, response = app.test_client.patch("/secure_patch")
    assert response.status == 401
    assert response.text == "Unauthorized"

    _, response = app.test_client.patch("/secure_patch", headers={"authorization": "Bearer valid_token"})
    assert response.status == 200
    assert response.text == "Authorized"