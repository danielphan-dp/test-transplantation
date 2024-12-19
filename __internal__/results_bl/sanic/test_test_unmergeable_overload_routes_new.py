import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_post_method(app):
    @app.route("/post_test", methods=["POST"])
    async def post_handler(request):
        return text('I am post method')

    request, response = app.test_client.post("/post_test")
    assert response.text == 'I am post method'
    assert response.status == 200

def test_post_method_invalid_method(app):
    @app.route("/post_test_invalid", methods=["GET"])
    async def get_handler(request):
        return text('This should not be accessible via POST')

    request, response = app.test_client.post("/post_test_invalid")
    assert response.status == 405

def test_post_method_no_route(app):
    request, response = app.test_client.post("/non_existent_route")
    assert response.status == 404