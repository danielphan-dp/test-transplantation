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
    if data == '{"name": ""}':
        assert value == {"name": ""}
    elif data == '{"name": null}':
        assert value == {"name": None}
    elif data == '{"name": 123}':
        assert value == {"name": "123"}
    elif data == '{"name": true}':
        assert value == {"name": "True"}
    else:
        value = app.json.dumps(Data(value["name"]))
        assert value == {"name": value["name"]}