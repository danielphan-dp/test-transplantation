import json
import pytest
from sanic import Sanic, Request
from sanic.response import text

@pytest.fixture
def json_app():
    app = Sanic("TestApp")
    return app

def test_get_method(json_app):
    @json_app.route("/get", methods=["GET"])
    def get_method(request):
        return text('I am get method')

    _, resp = json_app.test_client.get("/get")
    assert resp.text == 'I am get method'

def test_get_method_with_query_params(json_app):
    @json_app.route("/get", methods=["GET"])
    def get_method(request):
        return text(f'Query params: {request.args}')

    _, resp = json_app.test_client.get("/get?param1=value1&param2=value2")
    assert resp.text == 'Query params: MultiDict([(\'param1\', [\'value1\']), (\'param2\', [\'value2\'])])'

def test_get_method_with_headers(json_app):
    @json_app.route("/get", methods=["GET"])
    def get_method(request):
        return text(f'Headers: {request.headers}')

    _, resp = json_app.test_client.get("/get", headers={"Custom-Header": "value"})
    assert resp.text == 'Headers: {\'host\': \'\', \'user-agent\': \'\', \'accept\': \'\', \'custom-header\': \'value\'}'

def test_get_method_empty_response(json_app):
    @json_app.route("/get", methods=["GET"])
    def get_method(request):
        return text('')

    _, resp = json_app.test_client.get("/get")
    assert resp.text == ''