import json
import pytest
from conftest import TEST_FOLDER

@pytest.mark.parametrize('specs', SPECS)
def test_app_with_invalid_definition(multiple_yaml_same_basepath_dir, specs, app_class):
    app = app_class(
        __name__,
        specification_dir=".."
        / multiple_yaml_same_basepath_dir.relative_to(TEST_FOLDER),
    )

    invalid_spec = {"invalid": "specification"}
    app.add_api(**invalid_spec)

    app_client = app.test_client()

    response = app_client.post("/v1.0/greeting/Igor")
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid specification provided"

@pytest.mark.parametrize('specs', SPECS)
def test_app_with_missing_endpoint(multiple_yaml_same_basepath_dir, specs, app_class):
    app = app_class(
        __name__,
        specification_dir=".."
        / multiple_yaml_same_basepath_dir.relative_to(TEST_FOLDER),
    )

    for spec in specs:
        app.add_api(**spec)

    app_client = app.test_client()

    response = app_client.get("/v1.0/nonexistent_endpoint")
    assert response.status_code == 404
    assert response.json()["detail"] == "Not Found"

@pytest.mark.parametrize('specs', SPECS)
def test_app_with_empty_request_body(multiple_yaml_same_basepath_dir, specs, app_class):
    app = app_class(
        __name__,
        specification_dir=".."
        / multiple_yaml_same_basepath_dir.relative_to(TEST_FOLDER),
    )

    for spec in specs:
        app.add_api(**spec)

    app_client = app.test_client()

    response = app_client.post("/v1.0/greeting", json={})
    assert response.status_code == 400
    assert response.json()["detail"] == "Request body is required"

@pytest.mark.parametrize('specs', SPECS)
def test_app_with_invalid_method(multiple_yaml_same_basepath_dir, specs, app_class):
    app = app_class(
        __name__,
        specification_dir=".."
        / multiple_yaml_same_basepath_dir.relative_to(TEST_FOLDER),
    )

    for spec in specs:
        app.add_api(**spec)

    app_client = app.test_client()

    response = app_client.put("/v1.0/greeting/Igor")
    assert response.status_code == 405
    assert response.json()["detail"] == "Method Not Allowed"