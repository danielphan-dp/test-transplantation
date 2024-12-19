import pytest
from sanic import Sanic
from sanic.response import text
from sanic.views import HTTPMethodView

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_post_method(app):
    class PostView(HTTPMethodView):
        def post(self, request):
            return text('I am post method')

    app.add_route(PostView.as_view(), "/post")
    request, response = app.test_client.post("/post")
    assert response.body == b'I am post method'

def test_post_method_not_allowed(app):
    class DummyView(HTTPMethodView):
        def get(self, request):
            return text("I am get method")

    app.add_route(DummyView.as_view(), "/")
    request, response = app.test_client.post("/")
    assert b'Method POST not allowed for URL /' in response.body

def test_post_method_with_invalid_data(app):
    class PostView(HTTPMethodView):
        def post(self, request):
            return text('I am post method')

    app.add_route(PostView.as_view(), "/post")
    request, response = app.test_client.post("/post", data="invalid data")
    assert response.body == b'I am post method'  # Assuming the method handles invalid data gracefully

def test_post_method_with_headers(app):
    class PostView(HTTPMethodView):
        def post(self, request):
            return text('I am post method with headers')

    app.add_route(PostView.as_view(), "/post_with_headers")
    request, response = app.test_client.post("/post_with_headers", headers={"Custom-Header": "value"})
    assert response.body == b'I am post method with headers'