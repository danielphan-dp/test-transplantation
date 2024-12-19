import pytest
from sanic import Sanic
from sanic.response import text
from sanic.request import Request

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

def test_delete_method_with_invalid_route(app):
    @app.route("/delete", methods=["DELETE"])
    def delete_method(request):
        return text("I am delete method")

    _, response = app.test_client.get("/delete")
    assert response.status == 405  # Method Not Allowed

def test_delete_method_with_auth(app):
    @app.route("/secure-delete", methods=["DELETE"])
    def secure_delete(request):
        auth = request.headers.get("authorization")
        if auth == "Bearer valid_token":
            return text("Authorized delete")
        return text("Unauthorized", status=401)

    _, response = app.test_client.delete("/secure-delete", headers={"authorization": "Bearer valid_token"})
    assert response.text == "Authorized delete"

    _, response = app.test_client.delete("/secure-delete")
    assert response.status == 401
    assert response.text == "Unauthorized"