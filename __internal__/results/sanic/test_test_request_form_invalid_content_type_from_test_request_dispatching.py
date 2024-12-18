import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_post_method_response(app):
    @app.route("/", methods=["POST"])
    async def post(request):
        return text('I am post method')

    request, response = app.test_client.post("/")
    assert response.status == 200
    assert response.text == 'I am post method'

def test_post_method_with_invalid_content_type(app):
    @app.route("/", methods=["POST"])
    async def post(request):
        return text('I am post method')

    headers = {"content-type": "application/xml"}
    request, response = app.test_client.post("/", data="<test>data</test>", headers=headers)
    assert response.status == 200
    assert response.text == 'I am post method'

def test_post_method_empty_body(app):
    @app.route("/", methods=["POST"])
    async def post(request):
        return text('I am post method')

    request, response = app.test_client.post("/", data="")
    assert response.status == 200
    assert response.text == 'I am post method'

def test_post_method_with_json(app):
    @app.route("/", methods=["POST"])
    async def post(request):
        return text('I am post method')

    request, response = app.test_client.post("/", json={"key": "value"})
    assert response.status == 200
    assert response.text == 'I am post method'