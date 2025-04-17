import pytest
from sanic import Sanic
from sanic.response import text, json

@pytest.fixture
def app():
    app = Sanic("TestApp")

    @app.route("/ads/<ad_id>", methods=["POST"])
    async def ad_post(request, ad_id):
        return json({"ad_id": ad_id})

    return app

def test_post_method_with_valid_id(app):
    request, response = app.test_client.post("/ads/1234")
    assert response.status == 200
    assert response.json == {"ad_id": "1234"}

def test_post_method_with_string_id(app):
    request, response = app.test_client.post("/ads/test_id")
    assert response.status == 200
    assert response.json == {"ad_id": "test_id"}

def test_post_method_with_empty_id(app):
    request, response = app.test_client.post("/ads/")
    assert response.status == 404

def test_post_method_with_invalid_route(app):
    request, response = app.test_client.post("/ads/invalid_route")
    assert response.status == 200
    assert response.json == {"ad_id": "invalid_route"}

def test_post_method_with_special_characters(app):
    request, response = app.test_client.post("/ads/!@#$%^&*()")
    assert response.status == 200
    assert response.json == {"ad_id": "!@#$%^&*()"}