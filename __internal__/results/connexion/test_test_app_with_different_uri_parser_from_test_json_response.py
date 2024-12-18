import pytest
from connexion import App

@pytest.fixture
def simple_api_spec_dir():
    return "path/to/spec"

def test_get_method_with_kwargs(simple_api_spec_dir):
    app = App(__name__, specification_dir=".." / simple_api_spec_dir)
    app.add_api("swagger.yaml")

    app_client = app.test_client()
    resp = app_client.get("/v1.0/test_get_method?param1=value1&param2=value2")
    assert resp.status_code == 200
    j = resp.json()
    assert j == {'name': 'get', 'param1': 'value1', 'param2': 'value2'}

def test_get_method_without_kwargs(simple_api_spec_dir):
    app = App(__name__, specification_dir=".." / simple_api_spec_dir)
    app.add_api("swagger.yaml")

    app_client = app.test_client()
    resp = app_client.get("/v1.0/test_get_method")
    assert resp.status_code == 200
    j = resp.json()
    assert j == [{'name': 'get'}]

def test_get_method_with_empty_kwargs(simple_api_spec_dir):
    app = App(__name__, specification_dir=".." / simple_api_spec_dir)
    app.add_api("swagger.yaml")

    app_client = app.test_client()
    resp = app_client.get("/v1.0/test_get_method?empty_param=")
    assert resp.status_code == 200
    j = resp.json()
    assert j == {'name': 'get', 'empty_param': ''}