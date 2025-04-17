import uuid
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/")
    async def get_handler(request):
        return text("I am get method")

    return app

def test_get_method(app):
    request, response = app.test_client.get("/")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404

def test_get_method_with_uuid(app):
    results = []

    @app.route("/quirky/<unique_id:uuid>")
    async def handler(request, unique_id):
        results.append(unique_id)
        return text("OK")

    generated_uuid = uuid.uuid4()
    request, response = app.test_client.get(f"/quirky/{generated_uuid}")
    assert response.status == 200
    assert response.text == "OK"
    assert isinstance(results[0], uuid.UUID)

def test_get_method_with_non_uuid(app):
    request, response = app.test_client.get("/quirky/non-existing")
    assert response.status == 404

def test_get_method_with_empty_request(app):
    request, response = app.test_client.get("/")
    assert response.status == 200
    assert response.text == "I am get method"