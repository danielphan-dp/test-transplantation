import asyncio
import pytest
from sanic.app import Sanic
from sanic.blueprints import Blueprint
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method_with_valid_host(app):
    bp = Blueprint("test_bp_host", url_prefix="/test2", host=["example.com"])
    
    @bp.route("/")
    def get_method(request):
        return text('I am get method')
    
    app.blueprint(bp)
    
    headers = {"Host": "example.com"}
    request, response = app.test_client.get("/test2/", headers=headers)
    assert response.text == 'I am get method'

def test_get_method_with_invalid_host(app):
    bp = Blueprint("test_bp_host", url_prefix="/test2", host=["example.com"])
    
    @bp.route("/")
    def get_method(request):
        return text('I am get method')
    
    app.blueprint(bp)
    
    headers = {"Host": "invalid.example.com"}
    request, response = app.test_client.get("/test2/", headers=headers)
    assert response.status == 404

def test_get_method_with_no_host(app):
    bp = Blueprint("test_bp_host", url_prefix="/test2", host=["example.com"])
    
    @bp.route("/")
    def get_method(request):
        return text('I am get method')
    
    app.blueprint(bp)
    
    request, response = app.test_client.get("/test2/")
    assert response.status == 404

def test_get_method_with_subdomain(app):
    bp = Blueprint("test_bp_host", url_prefix="/test2", host=["sub.example.com"])
    
    @bp.route("/")
    def get_method(request):
        return text('I am get method')
    
    app.blueprint(bp)
    
    headers = {"Host": "sub.example.com"}
    request, response = app.test_client.get("/test2/", headers=headers)
    assert response.text == 'I am get method'