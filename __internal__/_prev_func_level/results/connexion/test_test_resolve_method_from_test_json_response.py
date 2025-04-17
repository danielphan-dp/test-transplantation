import pytest

@pytest.fixture
def simple_app():
    from connexion import App
    app = App(__name__)
    return app

def test_get_with_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/resolver-test/method?arg1=value1&arg2=value2")
    assert resp.json == {'name': 'get', 'arg1': 'value1', 'arg2': 'value2'}

def test_get_without_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/resolver-test/method")
    assert resp.json == [{'name': 'get'}]