import pytest

@pytest.fixture
def simple_app():
    from connexion import FlaskApp
    app = FlaskApp(__name__)
    return app

def test_get_with_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/get?arg1=value1&arg2=value2")
    assert resp.status_code == 200, resp.text
    assert resp.json == {'name': 'get', 'arg1': 'value1', 'arg2': 'value2'}

def test_get_without_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/get")
    assert resp.status_code == 200, resp.text
    assert resp.json == [{'name': 'get'}]

def test_get_with_empty_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/get?")
    assert resp.status_code == 200, resp.text
    assert resp.json == [{'name': 'get'}]