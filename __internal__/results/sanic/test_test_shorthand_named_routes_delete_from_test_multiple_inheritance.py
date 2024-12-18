import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_delete_method(app):
    @app.delete("/delete")
    def delete_handler(request):
        return text("I am delete method")

    request, response = app.test_client.delete("/delete")
    assert response.text == "I am delete method"
    assert response.status == 200

def test_delete_route_name(app):
    @app.delete("/delete", name="route_delete")
    def delete_handler(request):
        return text("OK")

    assert app.router.routes_all[("delete",)].name == "app.route_delete"
    assert app.url_for("route_delete") == "/delete"

def test_delete_method_not_found(app):
    request, response = app.test_client.delete("/nonexistent")
    assert response.status == 404
    assert b"Not Found" in response.body

def test_delete_method_with_query_params(app):
    @app.delete("/delete")
    def delete_handler(request):
        return text(f"Deleted item with id: {request.args.get('id')}")

    request, response = app.test_client.delete("/delete?id=123")
    assert response.text == "Deleted item with id: 123"
    assert response.status == 200

def test_delete_method_with_invalid_route(app):
    with pytest.raises(Exception):
        app.url_for("invalid_route")