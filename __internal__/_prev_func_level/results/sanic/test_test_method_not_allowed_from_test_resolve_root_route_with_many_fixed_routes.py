import pytest
from sanic import Sanic, Request, response

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_head_method_with_no_content(app):
    @app.route("/", methods=["HEAD"])
    async def head_handler(request: Request):
        return response.text('', headers={'method': 'HEAD'})

    request, response = app.test_client.head("/")
    assert response.status == 200
    assert response.headers["Content-Length"] == "0"
    assert response.headers["method"] == "HEAD"

def test_head_method_not_allowed_for_post(app):
    @app.post("/")
    async def post_handler(request: Request):
        return response.json({"message": "not allowed"})

    request, response = app.test_client.head("/")
    assert response.status == 405
    assert set(response.headers["Allow"].split(", ")) == {"GET", "POST"}
    assert response.headers["Content-Length"] == "0"

def test_head_method_not_allowed_for_patch(app):
    @app.patch("/")
    async def patch_handler(request: Request):
        return response.json({"message": "not allowed"})

    request, response = app.test_client.head("/")
    assert response.status == 405
    assert set(response.headers["Allow"].split(", ")) == {"GET", "PATCH"}
    assert response.headers["Content-Length"] == "0"