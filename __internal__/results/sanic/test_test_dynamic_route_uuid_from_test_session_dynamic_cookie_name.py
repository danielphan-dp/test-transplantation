import uuid
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.route("/get")
    def get(request):
        return text('I am get method')

    return app

def test_get_method(app):
    request, response = app.test_client.get("/get")
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/non-existing")
    assert response.status == 404

def test_get_method_with_uuid(app):
    generated_uuid = uuid.uuid4()
    url = f"/quirky/{generated_uuid}"
    
    @app.route("/quirky/<unique_id:uuid>")
    async def handler(request, unique_id):
        return text("OK")

    request, response = app.test_client.get(url)
    assert response.text == "OK"
    assert response.status == 200

def test_get_method_with_invalid_uuid(app):
    request, response = app.test_client.get("/quirky/non-existing")
    assert response.status == 404