import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import URLBuildError

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.delete("/delete", name="route_delete")
    def delete_handler(request):
        return text("I am delete method")

    return app

def test_delete_route(app):
    request, response = app.test_client.delete("/delete")
    assert response.text == "I am delete method"
    assert response.status == 200

def test_delete_route_not_found(app):
    request, response = app.test_client.delete("/nonexistent")
    assert response.status == 404

def test_named_route(app):
    assert app.router.routes_all[("delete",)].name == "app.route_delete"
    assert app.url_for("route_delete") == "/delete"
    with pytest.raises(URLBuildError):
        app.url_for("nonexistent_handler")