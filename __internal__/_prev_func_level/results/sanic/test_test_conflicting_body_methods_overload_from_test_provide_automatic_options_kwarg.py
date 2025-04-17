import pytest
from sanic import Sanic
from sanic.response import text, json

@pytest.fixture
def app():
    app = Sanic("TestApp")

    @app.delete("/p/<foo>")
    async def delete(request, foo):
        return json(
            {"name": request.route.name, "body": str(request.body), "foo": foo}
        )

    return app

def test_delete_method_with_valid_param(app):
    _, response = app.test_client.delete("/p/test")
    assert response.status == 200
    assert response.json == {
        "name": "delete",
        "foo": "test",
        "body": str("".encode()),
    }

def test_delete_method_with_no_param(app):
    _, response = app.test_client.delete("/p/")
    assert response.status == 404

def test_delete_method_with_invalid_param(app):
    _, response = app.test_client.delete("/p/invalid_param")
    assert response.status == 200
    assert response.json == {
        "name": "delete",
        "foo": "invalid_param",
        "body": str("".encode()),
    }

def test_delete_method_with_empty_param(app):
    _, response = app.test_client.delete("/p/")
    assert response.status == 404

def test_delete_method_with_special_characters(app):
    _, response = app.test_client.delete("/p/@#$%")
    assert response.status == 200
    assert response.json == {
        "name": "delete",
        "foo": "@#$%",
        "body": str("".encode()),
    }