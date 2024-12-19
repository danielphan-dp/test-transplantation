import pytest
from sanic import Sanic
from sanic.response import text
from sanic.views import HTTPMethodView

app = Sanic("TestApp")

class TestView(HTTPMethodView):
    def get(self, request):
        return text('I am get method')

app.add_route(TestView.as_view(), "/test")

def test_get_method(app):
    request, response = app.test_client.get("/test")
    assert response.text == 'I am get method'

def test_get_method_not_found(app):
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404

def test_get_method_with_query_param(app):
    request, response = app.test_client.get("/test?param=value")
    assert response.text == 'I am get method'

def test_get_method_with_empty_path(app):
    request, response = app.test_client.get("/")
    assert response.status == 404

def test_get_method_with_special_characters(app):
    request, response = app.test_client.get("/test?param=!@#$%^&*()")
    assert response.text == 'I am get method'