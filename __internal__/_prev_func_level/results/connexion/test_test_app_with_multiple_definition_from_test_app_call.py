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
    assert response.json()["detail"] == "Invalid specification"

@pytest.mark.parametrize('specs', SPECS)
def test_app_with_missing_parameter(multiple_yaml_same_basepath_dir, specs, app_class):
    app = app_class(
        __name__,
        specification_dir=".."
        / multiple_yaml_same_basepath_dir.relative_to(TEST_FOLDER),
    )

    for spec in specs:
        app.add_api(**spec)

    app_client = app.test_client()

    response = app_client.post("/v1.0/greeting/")
    assert response.status_code == 400
    assert response.json()["detail"] == "Missing required parameter"

@pytest.mark.parametrize('specs', SPECS)
def test_app_with_unexpected_parameter(multiple_yaml_same_basepath_dir, specs, app_class):
    app = app_class(
        __name__,
        specification_dir=".."
        / multiple_yaml_same_basepath_dir.relative_to(TEST_FOLDER),
    )

    for spec in specs:
        app.add_api(**spec)

    app_client = app.test_client()

    response = app_client.post("/v1.0/greeting/Igor?unexpected_param=true")
    assert response.status_code == 400
    assert response.json()["detail"] == "Unexpected query parameter(s) unexpected_param"

@pytest.mark.parametrize('specs', SPECS)
def test_app_with_empty_body(multiple_yaml_same_basepath_dir, specs, app_class):
    app = app_class(
        __name__,
        specification_dir=".."
        / multiple_yaml_same_basepath_dir.relative_to(TEST_FOLDER),
    )

    for spec in specs:
        app.add_api(**spec)

    app_client = app.test_client()

    response = app_client.post("/v1.0/greeting/Igor", data=json.dumps({}), content_type='application/json')
    assert response.status_code == 400
    assert response.json()["detail"] == "Empty request body"