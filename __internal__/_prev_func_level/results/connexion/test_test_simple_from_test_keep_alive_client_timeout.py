import pytest

@pytest.fixture
def swagger_ui_app():
    from flask import Flask
    app = Flask(__name__)

    @app.route('/v1.0/spec.json', methods=['GET'])
    def spec_json():
        return {'name': 'get'}, 200

    return app

def test_get_with_kwargs(swagger_ui_app):
    app_client = swagger_ui_app.test_client()
    response = app_client.get("/v1.0/spec.json?param1=value1&param2=value2")
    assert response.status_code == 200
    assert response.json == {'name': 'get'}

def test_get_without_kwargs(swagger_ui_app):
    app_client = swagger_ui_app.test_client()
    response = app_client.get("/v1.0/spec.json")
    assert response.status_code == 200
    assert response.json == [{'name': 'get'}]

def test_get_with_empty_kwargs(swagger_ui_app):
    app_client = swagger_ui_app.test_client()
    response = app_client.get("/v1.0/spec.json?param1=")
    assert response.status_code == 200
    assert response.json == [{'name': 'get'}]