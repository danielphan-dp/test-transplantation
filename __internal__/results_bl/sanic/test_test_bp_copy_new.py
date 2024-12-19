import pytest
from sanic import Sanic, Blueprint
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_get_method(app):
    bp = Blueprint("test_bp", version=1)

    @bp.get("/get")
    def get_method(request):
        return text('I am get method')

    app.blueprint(bp)

    _, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_not_found(app):
    bp = Blueprint("test_bp", version=1)

    @bp.get("/get")
    def get_method(request):
        return text('I am get method')

    app.blueprint(bp)

    _, response = app.test_client.get("/nonexistent")
    assert response.status == 404

def test_get_method_with_query_params(app):
    bp = Blueprint("test_bp", version=1)

    @bp.get("/get")
    def get_method(request):
        return text(f'I am get method with param: {request.args.get("param", "none")}')

    app.blueprint(bp)

    _, response = app.test_client.get("/get?param=test")
    assert response.status == 200
    assert response.text == 'I am get method with param: test'

def test_get_method_empty_query_params(app):
    bp = Blueprint("test_bp", version=1)

    @bp.get("/get")
    def get_method(request):
        return text(f'I am get method with param: {request.args.get("param", "none")}')

    app.blueprint(bp)

    _, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == 'I am get method with param: none'