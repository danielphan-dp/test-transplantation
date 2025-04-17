import json
import pytest
from conftest import TEST_FOLDER

@pytest.mark.parametrize('input_data, expected_output', [
    ('{"key": "value"}', {"key": "value"}),
    ('{"number": 123}', {"number": 123}),
    ('{"float": 123.45}', {"float": 123.45}),
    ('{"boolean": true}', {"boolean": True}),
    ('{"null_value": null}', {"null_value": None}),
    ('invalid json', None),  # Edge case for invalid JSON
])
def test_json_method(input_data, expected_output):
    class MockResponse:
        def __init__(self, text):
            self.text = text

        def json(self):
            try:
                return json.loads(self.text)
            except json.JSONDecodeError:
                return None

    response = MockResponse(input_data)
    if expected_output is None:
        with pytest.raises(Exception):
            response.json()
    else:
        assert response.json() == expected_output

def test_app_with_invalid_json(app_class):
    app = app_class(__name__, specification_dir="..")
    app_client = app.test_client()

    response = app_client.post("/v1.0/greeting/Igor", data='invalid json')
    assert response.status_code == 400  # Expecting a bad request for invalid JSON
    response_data = response.json()
    assert response_data["detail"] == "Invalid JSON input"  # Assuming the API returns this detail for invalid JSON