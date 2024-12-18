import pytest
from dataclasses import make_dataclass

@pytest.fixture
def app():
    from flask import Flask
    return Flask(__name__)

@pytest.fixture
def req_ctx(app):
    with app.test_request_context() as ctx:
        yield ctx

def test_json_loads_dataclass(app, req_ctx):
    Data = make_dataclass("Data", [("name", str)])
    value = app.json.dumps(Data("Flask"))
    loaded_value = app.json.loads(value)
    assert loaded_value == {"name": "Flask"}

def test_json_loads_empty_string(app, req_ctx):
    loaded_value = app.json.loads("")
    assert loaded_value == {}

def test_json_loads_invalid_json(app, req_ctx):
    with pytest.raises(ValueError):
        app.json.loads("{invalid_json}")

def test_json_loads_nested_dataclass(app, req_ctx):
    Data = make_dataclass("Data", [("name", str), ("details", Data)])
    nested_value = app.json.dumps(Data("Flask", Data("Details")))
    loaded_value = app.json.loads(nested_value)
    assert loaded_value == {"name": "Flask", "details": {"name": "Details"}}

def test_json_loads_list_of_dataclasses(app, req_ctx):
    Data = make_dataclass("Data", [("name", str)])
    data_list = app.json.dumps([Data("Flask"), Data("Django")])
    loaded_value = app.json.loads(data_list)
    assert loaded_value == [{"name": "Flask"}, {"name": "Django"}]