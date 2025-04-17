import pytest
from connexion import App

@pytest.fixture
def app():
    app = App(__name__)
    app.add_api("swagger.yaml")
    return app

def test_get_with_kwargs(app):
    app_client = app.test_client()
    resp = app_client.get("/v1.0/test_array_csv_query_param?items=a,b,c&items=d,e,f&extra_param=value")
    assert resp.status_code == 200
    j = resp.json()
    assert j == {'name': 'get', 'extra_param': 'value'}

def test_get_without_kwargs(app):
    app_client = app.test_client()
    resp = app_client.get("/v1.0/test_array_csv_query_param")
    assert resp.status_code == 200
    j = resp.json()
    assert j == [{'name': 'get'}]

def test_get_with_empty_kwargs(app):
    app_client = app.test_client()
    resp = app_client.get("/v1.0/test_array_csv_query_param?items=")
    assert resp.status_code == 200
    j = resp.json()
    assert j == [{'name': 'get'}]