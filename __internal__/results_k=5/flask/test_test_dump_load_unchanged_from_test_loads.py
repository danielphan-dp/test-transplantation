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
        Markup("<div>Markup content</div>"),
        uuid4(),
        datetime.now(tz=timezone.utc).replace(microsecond=0),
        None,
        True,
        False,
    ),
)
def test_loads_with_various_data_types(data):
    s = TaggedJSONSerializer()
    serialized_data = s.dumps(data)
    assert s.loads(serialized_data) == data

def test_loads_with_invalid_json():
    s = TaggedJSONSerializer()
    with pytest.raises(ValueError):
        s.loads(b'invalid json')

def test_loads_with_empty_string():
    s = TaggedJSONSerializer()
    assert s.loads('') == {}  # Assuming empty string should return an empty dict

def test_loads_with_non_serializable_data():
    class NonSerializable:
        pass

    s = TaggedJSONSerializer()
    with pytest.raises(TypeError):
        s.loads(s.dumps(NonSerializable()))