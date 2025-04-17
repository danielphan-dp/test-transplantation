import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_post_method_response(app):
    @app.route("/post", methods=["POST"])
    async def post_handler(request):
        return text('I am post method')

    request, response = app.test_client.post("/post")
    
    assert response.status == 200
    assert response.text == 'I am post method'

def test_post_with_empty_payload(app):
    @app.route("/post", methods=["POST"])
    async def post_handler(request):
        return text('I am post method')

    payload = ""
    headers = {"content-type": "application/x-www-form-urlencoded"}

    request, response = app.test_client.post("/post", data=payload, headers=headers)

    assert response.status == 200
    assert response.text == 'I am post method'

def test_post_with_invalid_content_type(app):
    @app.route("/post", methods=["POST"])
    async def post_handler(request):
        return text('I am post method')

    headers = {"content-type": "text/plain"}
    request, response = app.test_client.post("/post", data="test data", headers=headers)

    assert response.status == 200
    assert response.text == 'I am post method'