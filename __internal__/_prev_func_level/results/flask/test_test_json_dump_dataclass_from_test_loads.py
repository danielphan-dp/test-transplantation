import pytest
from dataclasses import make_dataclass
from flask import Flask

@pytest.fixture
def app():
    app = Flask(__name__)
    return app

def test_json_loads_dataclass(app):
    Data = make_dataclass("Data", [("name", str)])
    value = app.json.dumps(Data("Flask"))
    loaded_value = app.json.loads(value)
    assert loaded_value == {"name": "Flask"}

def test_json_loads_empty_string(app):
    loaded_value = app.json.loads("")
    assert loaded_value == {}

def test_json_loads_invalid_json(app):
    with pytest.raises(ValueError):
        app.json.loads("{invalid_json}")

def test_json_loads_nested_dataclass(app):
    Data = make_dataclass("Data", [("name", str), ("age", int)])
    value = app.json.dumps(Data("Flask", 5))
    loaded_value = app.json.loads(value)
    assert loaded_value == {"name": "Flask", "age": 5}

def test_json_loads_with_object_hook(app):
    def custom_object_hook(dct):
        return Data(**dct)

    Data = make_dataclass("Data", [("name", str)])
    value = app.json.dumps(Data("Flask"))
    loaded_value = app.json.loads(value, object_hook=custom_object_hook)
    assert isinstance(loaded_value, Data)
    assert loaded_value.name == "Flask"