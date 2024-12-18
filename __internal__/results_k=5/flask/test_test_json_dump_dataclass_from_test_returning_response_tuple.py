import pytest
from dataclasses import make_dataclass

@pytest.mark.parametrize("data", [
    '{"name": "Flask"}',
    '{"name": "Test"}',
    '{"name": ""}',
    '{"name": null}',
    '{"name": 123}',
    '{"name": true}',
])
def test_json_loads_dataclass(app, req_ctx, data):
    Data = make_dataclass("Data", [("name", str)])
    value = app.json.loads(data)
    assert isinstance(value, dict)
    assert "name" in value
    if value["name"] is None:
        assert value["name"] == ""
    elif isinstance(value["name"], str):
        assert value["name"] == value["name"]
    elif isinstance(value["name"], (int, bool)):
        assert str(value["name"]) == str(value["name"])