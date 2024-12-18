import pytest
from flask.json.tag import JSONTag, TaggedJSONSerializer

def test_loads_with_default_object_hook():
    class Foo:
        def __init__(self, data):
            self.data = data

    s = TaggedJSONSerializer()
    s.register(JSONTag)  # Registering a default tag for testing
    json_data = s.dumps(Foo("test"))
    result = s.loads(json_data)
    assert isinstance(result, Foo)
    assert result.data == "test"

def test_loads_with_invalid_json():
    s = TaggedJSONSerializer()
    with pytest.raises(ValueError):
        s.loads("invalid json")

def test_loads_with_custom_object_hook():
    class Foo:
        def __init__(self, data):
            self.data = data

    def custom_object_hook(dct):
        if 'data' in dct:
            return Foo(dct['data'])
        return dct

    s = TaggedJSONSerializer()
    json_data = s.dumps({"data": "custom"})
    result = s.loads(json_data, object_hook=custom_object_hook)
    assert isinstance(result, Foo)
    assert result.data == "custom"

def test_loads_with_empty_string():
    s = TaggedJSONSerializer()
    result = s.loads("")
    assert result is None

def test_loads_with_none():
    s = TaggedJSONSerializer()
    result = s.loads(None)
    assert result is None