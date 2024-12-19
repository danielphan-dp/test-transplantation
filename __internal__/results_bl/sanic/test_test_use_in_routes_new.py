import pytest
from sanic import Sanic
from sanic.text import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    @app.route("/", methods=["POST"])
    def handler(request):
        return text("I am post method")
    return app

def test_post_method(app):
    _, response = app.test_client.post("/")
    assert response.status == 200
    assert response.text == "I am post method"

def test_post_method_with_invalid_route(app):
    _, response = app.test_client.post("/invalid")
    assert response.status == 404

def test_post_method_with_empty_body(app):
    _, response = app.test_client.post("/", data="")
    assert response.status == 200
    assert response.text == "I am post method"

def test_post_method_with_json_content(app):
    _, response = app.test_client.post("/", json={"key": "value"})
    assert response.status == 200
    assert response.text == "I am post method"