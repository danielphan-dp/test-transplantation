import asyncio
import pytest
from sanic import Sanic
from sanic.blueprints import Blueprint
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_head_request(app):
    bp = Blueprint("test_blueprint_head_request")

    @bp.head("/head")
    async def head(request):
        return text('', headers={'method': 'HEAD'})

    app.blueprint(bp)

    request, response = app.test_client.head("/head")
    assert response.status == 200
    assert response.text == ""
    assert response.headers['method'] == 'HEAD'

def test_head_request_with_invalid_route(app):
    request, response = app.test_client.head("/invalid")
    assert response.status == 404

def test_head_request_with_additional_headers(app):
    bp = Blueprint("test_blueprint_head_request_headers")

    @bp.head("/head_with_headers")
    async def head_with_headers(request):
        return text('', headers={'method': 'HEAD', 'Custom-Header': 'Value'})

    app.blueprint(bp)

    request, response = app.test_client.head("/head_with_headers")
    assert response.status == 200
    assert response.text == ""
    assert response.headers['Custom-Header'] == 'Value'