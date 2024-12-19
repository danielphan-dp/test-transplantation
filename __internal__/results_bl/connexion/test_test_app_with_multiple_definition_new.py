import json
import pytest
from conftest import TEST_FOLDER

@pytest.mark.parametrize('input_text, expected_output', [
    ('{"key": "value"}', {"key": "value"}),
    ('{"greeting": "Hello World"}', {"greeting": "Hello World"}),
    ('{"number": 123}', {"number": 123}),
    ('{"array": [1, 2, 3]}', {"array": [1, 2, 3]}),
    ('{"nested": {"key": "value"}}', {"nested": {"key": "value"}}),
    ('invalid json', None),  # Edge case for invalid JSON
])
def test_json_method(input_text, expected_output):
    class MockResponse:
        def __init__(self, text):
            self.text = text

        def json(self):
            try:
                return json.loads(self.text)
            except json.JSONDecodeError:
                return None

    response = MockResponse(input_text)
    if expected_output is None:
        with pytest.raises(TypeError):
            response.json()
    else:
        assert response.json() == expected_output