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

def test_delete_method_with_valid_foo(app):
    _, response = app.test_client.delete("/p/test")
    assert response.status == 200
    assert response.json == {
        "name": "delete",
        "foo": "test",
        "body": str("".encode()),
    }

def test_delete_method_with_empty_foo(app):
    _, response = app.test_client.delete("/p/")
    assert response.status == 404

def test_delete_method_with_nonexistent_foo(app):
    _, response = app.test_client.delete("/p/nonexistent")
    assert response.status == 404

def test_delete_method_without_foo(app):
    _, response = app.test_client.delete("/p/")
    assert response.status == 404

def test_delete_method_with_special_characters(app):
    _, response = app.test_client.delete("/p/!@#$%^&*()")
    assert response.status == 200
    assert response.json == {
        "name": "delete",
        "foo": "!@#$%^&*()",
        "body": str("".encode()),
    }