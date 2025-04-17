import pytest
from sanic import Sanic
from sanic.response import text
from sanic.views import HTTPMethodView

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_post_method_view(app):
    class PostView(HTTPMethodView):
        def post(self, request):
            return text('I am post method')

    app.add_route(PostView.as_view(), "/post_view")

    request, response = app.test_client.post("/post_view")
    assert response.status == 200
    assert response.text == 'I am post method'

def test_post_method_view_with_data(app):
    class PostView(HTTPMethodView):
        def post(self, request):
            return text(request.json.get('data', 'No data'))

    app.add_route(PostView.as_view(), "/post_view_data")

    request, response = app.test_client.post("/post_view_data", json={'data': 'Test data'})
    assert response.status == 200
    assert response.text == 'Test data'

def test_post_method_view_empty_data(app):
    class PostView(HTTPMethodView):
        def post(self, request):
            return text(request.json.get('data', 'No data'))

    app.add_route(PostView.as_view(), "/post_view_empty")

    request, response = app.test_client.post("/post_view_empty", json={})
    assert response.status == 200
    assert response.text == 'No data'

def test_post_method_view_invalid_route(app):
    request, response = app.test_client.post("/invalid_post_view")
    assert response.status == 404
    assert "Requested URL /invalid_post_view not found" in response.text

def test_post_method_view_method_not_allowed(app):
    class PostView(HTTPMethodView):
        def post(self, request):
            return text('I am post method')

    app.add_route(PostView.as_view(), "/post_view")

    request, response = app.test_client.get("/post_view")
    assert response.status == 405
    assert "Method GET not allowed for URL /post_view" in response.text