import pytest
from connexion import App

def test_get_with_kwargs(simple_api_spec_dir, spec):
    app = App(__name__, specification_dir=simple_api_spec_dir)
    app.add_api(spec)
    app_client = app.test_client()
    
    response = app_client.get("/v1.0/get", query_string={"key": "value"})
    assert response.status_code == 200
    assert response.json == {'key': 'value', 'name': 'get'}

def test_get_without_kwargs(simple_api_spec_dir, spec):
    app = App(__name__, specification_dir=simple_api_spec_dir)
    app.add_api(spec)
    app_client = app.test_client()
    
    response = app_client.get("/v1.0/get")
    assert response.status_code == 200
    assert response.json == [{'name': 'get'}]

def test_get_with_empty_kwargs(simple_api_spec_dir, spec):
    app = App(__name__, specification_dir=simple_api_spec_dir)
    app.add_api(spec)
    app_client = app.test_client()
    
    response = app_client.get("/v1.0/get", query_string={})
    assert response.status_code == 200
    assert response.json == [{'name': 'get'}]