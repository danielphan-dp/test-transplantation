import pytest
from connexion import FlaskApp

@pytest.fixture
def app():
    app = FlaskApp(__name__)
    return app

def test_put_method_success(app):
    @app.route('/v1.0/welcome', methods=['PUT'])
    def put_method(*args, **kwargs):
        kwargs.update({'name': 'put'})
        return (kwargs, 201)

    app_client = app.test_client()
    resp = app_client.put("/v1.0/welcome", json={"key": "value"})
    assert resp.status_code == 201
    assert resp.json == {'key': 'value', 'name': 'put'}

def test_put_method_with_no_body(app):
    @app.route('/v1.0/welcome', methods=['PUT'])
    def put_method(*args, **kwargs):
        kwargs.update({'name': 'put'})
        return (kwargs, 201)

    app_client = app.test_client()
    resp = app_client.put("/v1.0/welcome")
    assert resp.status_code == 201
    assert resp.json == {'name': 'put'}

def test_put_method_with_invalid_data(app):
    @app.route('/v1.0/welcome', methods=['PUT'])
    def put_method(*args, **kwargs):
        kwargs.update({'name': 'put'})
        return (kwargs, 201)

    app_client = app.test_client()
    resp = app_client.put("/v1.0/welcome", json={"invalid_key": "value"})
    assert resp.status_code == 201
    assert resp.json == {'invalid_key': 'value', 'name': 'put'}