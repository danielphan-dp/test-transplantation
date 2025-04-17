import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_post_method_response(app):
    @app.post("/test")
    async def handler(request):
        return text('I am post method')

    request, response = app.test_client.post("/test")
    assert response.status == 200
    assert response.text == 'I am post method'

def test_post_method_with_large_payload(app):
    @app.post("/test")
    async def handler(request):
        return text('I am post method')

    data = "a" * 1000
    _, response = app.test_client.post("/test", gather_request=False, data=data)
    assert response.status == 413
    assert "Request body" in response.text

def test_post_method_with_empty_payload(app):
    @app.post("/test")
    async def handler(request):
        return text('I am post method')

    request, response = app.test_client.post("/test", data="")
    assert response.status == 200
    assert response.text == 'I am post method'

def test_post_method_with_invalid_content_type(app):
    @app.post("/test")
    async def handler(request):
        return text('I am post method')

    headers = {"content-type": "application/xml"}
    request, response = app.test_client.post("/test", data="<data></data>", headers=headers)
    assert response.status == 200
    assert response.text == 'I am post method'