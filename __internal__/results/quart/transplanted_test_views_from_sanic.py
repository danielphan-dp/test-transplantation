# Transplanted from tests/test_views.py in the donor code to test src/quart/views.py in the host code

import pytest
from quart import Quart, request, jsonify
from quart.views import MethodView

# Fixture to create a Quart app for testing
@pytest.fixture
def app():
    app = Quart(__name__)
    return app

# Test all HTTP methods for a MethodView
@pytest.mark.parametrize("method", ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"])
@pytest.mark.asyncio
async def test_methods(app, method):
    class DummyView(MethodView):
        async def get(self, **kwargs):
            return jsonify({"method": "GET"})

        async def post(self, **kwargs):
            return jsonify({"method": "POST"})

        async def put(self, **kwargs):
            return jsonify({"method": "PUT"})

        async def delete(self, **kwargs):
            return jsonify({"method": "DELETE"})

        async def patch(self, **kwargs):
            return jsonify({"method": "PATCH"})

        async def options(self, **kwargs):
            return jsonify({"method": "OPTIONS"})

        async def head(self, **kwargs):
            return jsonify({"method": "HEAD"})

    app.add_url_rule('/', view_func=DummyView.as_view('dummy'))

    test_client = app.test_client()
    response = await getattr(test_client, method.lower())('/')
    assert (await response.get_json())["method"] == method

# Test a MethodView with only a GET method implemented
@pytest.mark.asyncio
async def test_unexisting_methods(app):
    class DummyView(MethodView):
        async def get(self, **kwargs):
            return jsonify("I am get method")

    app.add_url_rule('/', view_func=DummyView.as_view('dummy'))

    test_client = app.test_client()
    response = await test_client.get('/')
    assert (await response.get_data(as_text=True)) == "I am get method"

    response = await test_client.post('/')
    assert response.status_code == 405  # Method Not Allowed

# Test a MethodView with URL parameters
@pytest.mark.asyncio
async def test_argument_methods(app):
    class DummyView(MethodView):
        async def get(self, my_param_here, **kwargs):
            return jsonify(f"I am get method with {my_param_here}")

    app.add_url_rule('/<my_param_here>', view_func=DummyView.as_view('dummy'))

    test_client = app.test_client()
    response = await test_client.get('/test123')
    assert (await response.get_data(as_text=True)) == "I am get method with test123"

# Test a MethodView with decorators
@pytest.mark.asyncio
async def test_with_decorator(app):
    results = []

    def simple_decorator(func):
        async def wrapper(*args, **kwargs):
            results.append(1)
            return await func(*args, **kwargs)
        return wrapper

    class DummyView(MethodView):
        decorators = [simple_decorator]

        async def get(self, **kwargs):
            return jsonify("I am get method")

    app.add_url_rule('/', view_func=DummyView.as_view('dummy'))

    test_client = app.test_client()
    response = await test_client.get('/')
    assert (await response.get_data(as_text=True)) == "I am get method"
    assert results[0] == 1