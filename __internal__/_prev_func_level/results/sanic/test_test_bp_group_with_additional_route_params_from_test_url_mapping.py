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
        return text('I am delete method')

    _, response = app.test_client.delete("/delete")
    assert response.text == 'I am delete method'
    assert response.status == 200

def test_delete_method_unauthorized(app):
    @app.route("/delete", methods=["DELETE"])
    def delete_method(request):
        return text('I am delete method')

    _, response = app.test_client.delete("/delete", headers={"authorization": "invalid"})
    assert response.text == 'I am delete method'
    assert response.status == 200

def test_delete_method_with_invalid_route(app):
    @app.route("/delete", methods=["DELETE"])
    def delete_method(request):
        return text('I am delete method')

    _, response = app.test_client.delete("/invalid_route")
    assert response.status == 404

def test_delete_method_with_additional_params(app):
    @app.route("/delete/<param>", methods=["DELETE"])
    def delete_method_with_param(request, param):
        return text(f'Delete method called with param: {param}')

    _, response = app.test_client.delete("/delete/test_param")
    assert response.text == 'Delete method called with param: test_param'
    assert response.status == 200

def test_delete_method_with_invalid_method(app):
    @app.route("/delete", methods=["DELETE"])
    def delete_method(request):
        return text('I am delete method')

    _, response = app.test_client.get("/delete")
    assert response.status == 405
    assert response.headers.get("allow") == "DELETE"