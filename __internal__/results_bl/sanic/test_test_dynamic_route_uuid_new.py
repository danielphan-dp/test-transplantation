import uuid
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_get_method(app):
    @app.route("/get")
    async def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get("/get")
    assert response.text == 'I am get method'
    assert response.status == 200

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/non-existing-route")
    assert response.status == 404

def test_get_method_with_query_params(app):
    @app.route("/get_with_query")
    async def get_with_query(request):
        return text('Query received')

    request, response = app.test_client.get("/get_with_query?param=value")
    assert response.text == 'Query received'
    assert response.status == 200

def test_get_method_empty_query(app):
    @app.route("/get_with_empty_query")
    async def get_with_empty_query(request):
        return text('Empty query received')

    request, response = app.test_client.get("/get_with_empty_query?")
    assert response.text == 'Empty query received'
    assert response.status == 200

def test_get_method_with_uuid(app):
    @app.route("/get_with_uuid/<unique_id:uuid>")
    async def get_with_uuid(request, unique_id):
        return text(f'UUID received: {unique_id}')

    generated_uuid = uuid.uuid4()
    request, response = app.test_client.get(f"/get_with_uuid/{generated_uuid}")
    assert response.text == f'UUID received: {generated_uuid}'
    assert response.status == 200

def test_get_method_with_invalid_uuid(app):
    @app.route("/get_with_invalid_uuid/<unique_id:uuid>")
    async def get_with_invalid_uuid(request, unique_id):
        return text('Invalid UUID')

    request, response = app.test_client.get("/get_with_invalid_uuid/invalid-uuid")
    assert response.status == 404