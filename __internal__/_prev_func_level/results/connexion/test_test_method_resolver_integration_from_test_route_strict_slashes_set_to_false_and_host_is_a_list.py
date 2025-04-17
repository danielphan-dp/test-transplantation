import pytest
from connexion import FlaskApp
from connexion.resolver import MethodResolver
from conftest import build_app_from_fixture

@pytest.fixture
def app_class():
    return FlaskApp

def test_put_method_integration(app_class):
    method_view_app = build_app_from_fixture(
        "method_view",
        app_class=app_class,
        resolver=MethodResolver("fakeapi.example_method_class"),
    )

    client = method_view_app.test_client()

    # Test valid PUT request
    r = client.put("/v1.0/pets/1", json={"name": "Igor"})
    assert r.json() == {"name": "put", "petId": 1, "body": {"name": "Igor"}}

    # Test PUT request with missing body
    r = client.put("/v1.0/pets/1")
    assert r.status_code == 400  # Assuming the API returns 400 for missing body

    # Test PUT request with invalid data
    r = client.put("/v1.0/pets/1", json={"invalid_key": "value"})
    assert r.status_code == 400  # Assuming the API returns 400 for invalid data

    # Test PUT request with empty body
    r = client.put("/v1.0/pets/1", json={})
    assert r.status_code == 400  # Assuming the API returns 400 for empty body

    # Test PUT request with valid data but different petId
    r = client.put("/v1.0/pets/2", json={"name": "Igor"})
    assert r.json() == {"name": "put", "petId": 2, "body": {"name": "Igor"}}