import pytest
from sanic import Sanic, Request
from sanic.response import text

@pytest.mark.parametrize('request_path', ['/', '/test', '/another_test'])
def test_get_method_response(app: Sanic, request_path: str):
    @app.route(request_path, methods=["GET"])
    class DummyView:
        def get(self, request: Request):
            return text('I am get method')

    request, response = app.test_client.get(request_path)
    assert response.status == 200
    assert response.text == 'I am get method'

@pytest.mark.parametrize('invalid_path', ['/invalid', '/not_found'])
def test_get_method_invalid_route(app: Sanic, invalid_path: str):
    @app.route("/valid", methods=["GET"])
    class DummyView:
        def get(self, request: Request):
            return text('I am get method')

    request, response = app.test_client.get(invalid_path)
    assert response.status == 404
    assert "Requested URL" in response.text

def test_get_method_with_headers(app: Sanic):
    @app.route("/headers", methods=["GET"])
    class DummyView:
        def get(self, request: Request):
            return text('I am get method with headers')

    request, response = app.test_client.get("/headers", headers={"Custom-Header": "Value"})
    assert response.status == 200
    assert response.text == 'I am get method with headers'