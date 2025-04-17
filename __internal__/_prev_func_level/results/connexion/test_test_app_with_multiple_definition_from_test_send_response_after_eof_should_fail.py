import pytest
from connexion import FlaskApp

@pytest.mark.parametrize("kwargs, expected", [
    ({"key1": "value1"}, {"key1": "value1", "name": "get"}),
    ({}, [{"name": "get"}]),
    ({"param": "test"}, {"param": "test", "name": "get"}),
])
def test_get_method(kwargs, expected):
    app = FlaskApp(__name__)
    app.add_api('api.yaml')  # Assuming an API specification file is present
    app_client = app.test_client()

    response = app_client.get("/v1.0/get", query_string=kwargs)
    assert response.status_code == 200
    assert response.json() == expected

def test_get_method_no_kwargs():
    app = FlaskApp(__name__)
    app.add_api('api.yaml')  # Assuming an API specification file is present
    app_client = app.test_client()

    response = app_client.get("/v1.0/get")
    assert response.status_code == 200
    assert response.json() == [{"name": "get"}]