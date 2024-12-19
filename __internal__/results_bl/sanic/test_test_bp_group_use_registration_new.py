import pytest
from sanic import Sanic, Blueprint, text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

@pytest.fixture
def handler():
    async def handle_request(request):
        return text('I am get method')
    return handle_request

def test_bp_group_use_registration(app, handler):
    bp = Blueprint("Test", version=1.1)
    bp.route("/")(handler)
    group = Blueprint.group(bp, version=1)
    app.blueprint(group, version=1.2)

    _, response = app.test_client.get("/v1.2")
    assert response.status == 200

def test_get_method_response(app, handler):
    bp = Blueprint("Test", version=1.1)
    bp.route("/")(handler)
    app.blueprint(bp)

    _, response = app.test_client.get("/")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_not_found(app):
    bp = Blueprint("Test", version=1.1)
    app.blueprint(bp)

    _, response = app.test_client.get("/nonexistent")
    assert response.status == 404

def test_get_method_with_query_params(app, handler):
    bp = Blueprint("Test", version=1.1)
    bp.route("/")(handler)
    app.blueprint(bp)

    _, response = app.test_client.get("/?param=value")
    assert response.status == 200
    assert response.text == 'I am get method'