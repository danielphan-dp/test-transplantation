import pytest
from sanic import Sanic
from sanic.blueprints import Blueprint
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_get_method_with_valid_host(app):
    bp = Blueprint("test_get", url_prefix="/get", host="example.com")
    
    @bp.route("/")
    def get_handler(request):
        return text("I am get method")
    
    app.blueprint(bp)
    
    headers = {"Host": "example.com"}
    request, response = app.test_client.get("/get/", headers=headers)
    
    assert response.text == "I am get method"

def test_get_method_with_invalid_host(app):
    bp = Blueprint("test_get_invalid", url_prefix="/get", host="example.com")
    
    @bp.route("/")
    def get_handler(request):
        return text("I am get method")
    
    app.blueprint(bp)
    
    headers = {"Host": "invalid.com"}
    request, response = app.test_client.get("/get/", headers=headers)
    
    assert response.status == 404

def test_get_method_with_missing_host(app):
    bp = Blueprint("test_get_missing", url_prefix="/get", host="example.com")
    
    @bp.route("/")
    def get_handler(request):
        return text("I am get method")
    
    app.blueprint(bp)
    
    request, response = app.test_client.get("/get/")
    
    assert response.status == 404

def test_get_method_with_different_host(app):
    bp = Blueprint("test_get_diff", url_prefix="/get", host="example.com")
    
    @bp.route("/")
    def get_handler(request):
        return text("I am get method")
    
    app.blueprint(bp)
    
    headers = {"Host": "sub.example.com"}
    request, response = app.test_client.get("/get/", headers=headers)
    
    assert response.status == 404