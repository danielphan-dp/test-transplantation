import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")

    @app.route("/ads/<ad_id>", methods=["POST"])
    async def ad_post(request, ad_id):
        return text('I am post method')

    return app

def test_post_method_with_valid_id(app):
    request, response = app.test_client.post("/ads/valid_id")
    assert response.status == 200
    assert response.text == 'I am post method'

def test_post_method_with_empty_id(app):
    request, response = app.test_client.post("/ads/")
    assert response.status == 404

def test_post_method_with_special_characters(app):
    request, response = app.test_client.post("/ads/@special!")
    assert response.status == 200
    assert response.text == 'I am post method'

def test_post_method_with_numeric_id(app):
    request, response = app.test_client.post("/ads/12345")
    assert response.status == 200
    assert response.text == 'I am post method'