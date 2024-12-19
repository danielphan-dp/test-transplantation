import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    @app.route("/", methods=["POST"])
    async def post(request):
        return text("I am post method")
    return app

def test_post_method_valid_content_type(app):
    request, response = app.test_client.post("/", json={"key": "value"})
    assert response.text == "I am post method"

def test_post_method_empty_body(app):
    request, response = app.test_client.post("/", data="")
    assert response.text == "I am post method"

def test_post_method_invalid_json(app):
    request, response = app.test_client.post("/", data="invalid json")
    assert response.text == "I am post method"

def test_post_method_no_content_type(app):
    request, response = app.test_client.post("/", data="test data", headers={"Content-Type": ""})
    assert response.text == "I am post method"

def test_post_method_form_data(app):
    request, response = app.test_client.post("/", data={"key": "value"})
    assert response.text == "I am post method"