import pytest
from sanic import Sanic, Blueprint
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_delete_method(app):
    @app.route("/delete", methods=["DELETE"])
    def delete_method(request):
        return text("I am delete method")

    _, response = app.test_client.delete("/delete")
    assert response.text == "I am delete method"
    assert response.status == 200

def test_delete_method_with_invalid_route(app):
    _, response = app.test_client.delete("/nonexistent")
    assert response.status == 404

def test_delete_method_with_authentication(app):
    @app.route("/secure-delete", methods=["DELETE"])
    def secure_delete(request):
        auth = request.headers.get("authorization")
        if auth == "Bearer valid_token":
            return text("Secure delete successful")
        return text("Unauthorized", status=401)

    _, response = app.test_client.delete("/secure-delete", headers={"authorization": "Bearer valid_token"})
    assert response.text == "Secure delete successful"
    assert response.status == 200

    _, response = app.test_client.delete("/secure-delete")
    assert response.text == "Unauthorized"
    assert response.status == 401

def test_delete_method_with_custom_header(app):
    @app.route("/custom-header-delete", methods=["DELETE"])
    def custom_header_delete(request):
        return text("Custom header received", headers={"x-custom-header": "value"})

    _, response = app.test_client.delete("/custom-header-delete")
    assert response.text == "Custom header received"
    assert response.headers.get("x-custom-header") == "value"