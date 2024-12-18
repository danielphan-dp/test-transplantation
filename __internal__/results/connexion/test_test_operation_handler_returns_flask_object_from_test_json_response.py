import pytest

@pytest.fixture
def valid_kwargs_app():
    from connexion import FlaskApp
    app = FlaskApp(__name__)
    @app.route('/v1.0/get', methods=['GET'])
    def get_method(**kwargs):
        return get_method(**kwargs)
    return app

def test_get_method_with_kwargs(valid_kwargs_app):
    app_client = valid_kwargs_app.test_client()
    resp = app_client.get("/v1.0/get?param1=value1&param2=value2")
    assert resp.status_code == 200
    assert resp.json == {'name': 'get', 'param1': 'value1', 'param2': 'value2'}

def test_get_method_without_kwargs(valid_kwargs_app):
    app_client = valid_kwargs_app.test_client()
    resp = app_client.get("/v1.0/get")
    assert resp.status_code == 200
    assert resp.json == [{'name': 'get'}]

def test_get_method_with_empty_kwargs(valid_kwargs_app):
    app_client = valid_kwargs_app.test_client()
    resp = app_client.get("/v1.0/get?param1=")
    assert resp.status_code == 200
    assert resp.json == {'name': 'get', 'param1': ''}