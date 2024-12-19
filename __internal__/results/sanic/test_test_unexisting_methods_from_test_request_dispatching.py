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

def test_post_method_with_invalid_route(app):
    request, response = app.test_client.post("/invalid")
    assert response.status == 404
    assert b'Requested URL /invalid not found' in response.body

def test_post_method_with_data(app):
    class DataView(HTTPMethodView):
        def post(self, request):
            return text(f"Received data: {request.json}")

    app.add_route(DataView.as_view(), "/data", methods=["POST"])
    
    request, response = app.test_client.post("/data", json={"key": "value"})
    assert response.body == b'Received data: {"key": "value"}'