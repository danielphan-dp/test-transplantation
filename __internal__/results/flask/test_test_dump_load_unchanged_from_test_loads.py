import pytest
from datetime import datetime, timezone
from uuid import uuid4
from markupsafe import Markup
from flask.json.tag import TaggedJSONSerializer

@pytest.mark.parametrize(
    "data",
    (
        {"key": "value"},
        {"list": [1, 2, 3]},
        {"nested": {"inner_key": "inner_value"}},
        {"bytes": b"byte data"},
        {"markup": Markup("<div>Test</div>")},
        uuid4(),
        datetime.now(tz=timezone.utc).replace(microsecond=0),
        None,
        True,
        False,
    ),
)
def test_loads_various_data_types(data):
    s = TaggedJSONSerializer()
    serialized = s.dumps(data)
    deserialized = s.loads(serialized)
    assert deserialized == data

def test_loads_empty_string():
    s = TaggedJSONSerializer()
    assert s.loads('') == {}

def test_loads_invalid_json():
    s = TaggedJSONSerializer()
    with pytest.raises(ValueError):
        s.loads('{"key": "value",}')  # Invalid JSON

def test_loads_none():
    s = TaggedJSONSerializer()
    assert s.loads('null') is None

def test_loads_boolean_values():
    s = TaggedJSONSerializer()
    assert s.loads('true') is True
    assert s.loads('false') is False

def test_loads_nested_structures():
    s = TaggedJSONSerializer()
    data = {"outer": {"inner": [1, 2, 3]}}
    serialized = s.dumps(data)
    assert s.loads(serialized) == data