import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

@app.route("/get_test", methods=["GET"])
async def get_method(request):
    return text('I am get method')

def test_get_method(app):
    request, response = app.test_client.get("/get_test")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_not_found(app):
    request, response = app.test_client.get("/non_existent_route")
    assert response.status == 404

def test_get_method_with_query_params(app):
    @app.route("/get_test_with_params", methods=["GET"])
    async def get_method_with_params(request):
        return text(f'Query param: {request.args.get("param", "none")}')

    request, response = app.test_client.get("/get_test_with_params?param=test")
    assert response.status == 200
    assert response.text == 'Query param: test'