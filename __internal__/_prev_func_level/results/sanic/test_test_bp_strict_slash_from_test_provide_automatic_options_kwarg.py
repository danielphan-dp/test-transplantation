import pytest
from sanic import Sanic
from sanic.response import text
from sanic.blueprints import Blueprint

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_post_method(app):
    bp = Blueprint("test_post")

    @bp.post("/post/", strict_slashes=True)
    def post_handler(request):
        return text("I am post method")

    app.blueprint(bp)

    request, response = app.test_client.post("/post/")
    assert response.text == "I am post method"
    assert response.status == 200

    request, response = app.test_client.post("/post")
    assert response.status == 404

    request, response = app.test_client.get("/post/")
    assert response.status == 405
    assert "Method GET not allowed for URL /post/" in response.text

    request, response = app.test_client.options("/post/")
    assert response.status == 200
    assert "POST" in response.headers.get("Allow")