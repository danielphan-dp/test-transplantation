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
    instance = Data(**value)
    assert instance.name == value["name"]

def test_json_loads_invalid_data(app, req_ctx):
    with pytest.raises(ValueError):
        app.json.loads('{"name": "Flask", "extra": "data"}')