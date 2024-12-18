import pytest
from dataclasses import make_dataclass

def test_json_loads_empty_string(app, req_ctx):
    value = app.json.loads("")
    assert value == {}

def test_json_loads_invalid_json(app, req_ctx):
    with pytest.raises(ValueError):
        app.json.loads("invalid json")

def test_json_loads_none(app, req_ctx):
    value = app.json.loads(None)
    assert value is None

def test_json_loads_nested_dataclass(app, req_ctx):
    Data = make_dataclass("Data", [("name", str), ("age", int)])
    value = app.json.dumps(Data("Flask", 5))
    value = app.json.loads(value)
    assert value == {"name": "Flask", "age": 5}

def test_json_loads_with_object_hook(app, req_ctx):
    def custom_object_hook(dct):
        return {k: v.upper() for k, v in dct.items()}

    app.json.object_hook = custom_object_hook
    Data = make_dataclass("Data", [("name", str)])
    value = app.json.dumps(Data("Flask"))
    value = app.json.loads(value)
    assert value == {"name": "FLASK"}