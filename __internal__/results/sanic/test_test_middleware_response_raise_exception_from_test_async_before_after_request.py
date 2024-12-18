import logging
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method_response(app):
    class DummyView:
        def get(self, request):
            return text('I am get method')

    app.add_route(DummyView.get, "/get")

    request, response = app.test_client.get("/get")

    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_with_middleware(app, caplog):
    results = []

    @app.middleware("response")
    async def process_response(request, response):
        results.append(response)

    class DummyView:
        def get(self, request):
            return text('I am get method')

    app.add_route(DummyView.get, "/get")

    with caplog.at_level(logging.INFO):
        request, response = app.test_client.get("/get")

    assert response.status == 200
    assert response.text == 'I am get method'
    assert len(results) == 1
    assert isinstance(results[0], type(response))

def test_get_method_with_exception(app, caplog):
    class DummyView:
        def get(self, request):
            raise Exception("Test Exception")

    app.add_route(DummyView.get, "/get_exception")

    with caplog.at_level(logging.ERROR):
        request, response = app.test_client.get("/get_exception")

    assert response.status == 500
    assert "Test Exception" in caplog.text