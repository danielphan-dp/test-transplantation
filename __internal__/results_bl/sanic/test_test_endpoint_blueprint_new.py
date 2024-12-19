import pytest
from sanic import Sanic, Blueprint
from sanic.response import text

app = Sanic("named")
bp = Blueprint("my_blueprint", url_prefix="/bp")

@bp.route("/")
async def bp_root(request):
    return text("Hello")

@app.route("/get")
async def get_method(request):
    return text('I am get method')

app.blueprint(bp)

@pytest.mark.asyncio
async def test_get_method():
    request, response = await app.test_client.get("/get")
    assert response.text == 'I am get method'
    assert response.status == 200

@pytest.mark.asyncio
async def test_get_method_not_found():
    request, response = await app.test_client.get("/nonexistent")
    assert response.status == 404

@pytest.mark.asyncio
async def test_bp_root():
    request, response = await app.test_client.get("/bp")
    assert request.endpoint == "named.my_blueprint.bp_root"
    assert response.text == "Hello"
    assert response.status == 200