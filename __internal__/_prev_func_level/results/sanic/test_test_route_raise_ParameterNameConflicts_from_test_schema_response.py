import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/api/v1/test")
    def handler(request):
        return text("I am get method")

    return app

def test_get_method_success(app):
    request, response = app.test_client.get("/api/v1/test")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_not_found(app):
    request, response = app.test_client.get("/api/v1/non_existent")
    assert response.status == 404
    assert "Requested URL /api/v1/non_existent not found" in response.text

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/api/v1/<user>/<user>/")
    assert response.status == 404
    assert "Requested URL /api/v1/<user>/<user>/ not found" in response.text

def test_get_method_with_parameter_conflict(app):
    @app.get("/api/v1/<user>/<user>/")
    def handler(request, user):
        return text("OK")

    with pytest.raises(ParameterNameConflicts):
        app.router.finalize()