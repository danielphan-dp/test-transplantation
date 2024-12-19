import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

@app.route("/get")
async def get_handler(request):
    return text('I am get method')

def test_get_method(app):
    _, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_middleware_with_get_method(app):
    @app.middleware
    async def halt_request(request):
        return text("OK")

    @app.route("/get")
    async def get_handler(request):
        return text('I am get method')

    _, response = app.test_client.get("/get", gather_request=False)
    assert response.status == 200
    assert response.text == "OK"

def test_get_method_not_found(app):
    _, response = app.test_client.get("/nonexistent")
    assert response.status == 404

def test_get_method_with_query_params(app):
    @app.route("/get")
    async def get_handler(request):
        return text(f'Query param: {request.args.get("param", "not found")}')

    _, response = app.test_client.get("/get?param=test")
    assert response.status == 200
    assert response.text == 'Query param: test'