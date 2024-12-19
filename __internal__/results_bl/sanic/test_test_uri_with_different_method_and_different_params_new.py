import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")

    @app.route("/test_post", methods=["POST"])
    async def test_post(request):
        return text('I am post method')

    return app

def test_post_method(app):
    request, response = app.test_client.post("/test_post")
    assert response.status == 200
    assert response.text == 'I am post method'

def test_post_method_with_invalid_data(app):
    request, response = app.test_client.post("/test_post", json={"invalid": "data"})
    assert response.status == 200
    assert response.text == 'I am post method'

def test_post_method_with_no_data(app):
    request, response = app.test_client.post("/test_post", data=None)
    assert response.status == 200
    assert response.text == 'I am post method'