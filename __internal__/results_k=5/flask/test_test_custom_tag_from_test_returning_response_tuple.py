import pytest
from flask.json.tag import JSONTag
from flask.json.tag import TaggedJSONSerializer

class Foo:  
    def __init__(self, data):
        self.data = data

class TagFoo(JSONTag):
    __slots__ = ()
    key = " f"

    def check(self, value):
        return isinstance(value, Foo)

    def to_json(self, value):
        return self.serializer.tag(value.data)

    def to_python(self, value):
        return Foo(value)

def test_loads_with_valid_data():
    s = TaggedJSONSerializer()
    s.register(TagFoo)
    foo_instance = Foo("test")
    serialized = s.dumps(foo_instance)
    deserialized = s.loads(serialized)
    assert deserialized.data == "test"

def test_loads_with_invalid_data():
    s = TaggedJSONSerializer()
    s.register(TagFoo)
    with pytest.raises(TypeError):
        s.loads(s.dumps("invalid"))

def test_loads_with_empty_string():
    s = TaggedJSONSerializer()
    s.register(TagFoo)
    deserialized = s.loads(s.dumps(Foo("")))
    assert deserialized.data == ""

def test_loads_with_none():
    s = TaggedJSONSerializer()
    s.register(TagFoo)
    deserialized = s.loads(s.dumps(Foo(None)))
    assert deserialized.data is None

def test_loads_with_nested_foo():
    s = TaggedJSONSerializer()
    s.register(TagFoo)
    nested_foo = Foo(Foo("nested"))
    serialized = s.dumps(nested_foo)
    deserialized = s.loads(serialized)
    assert deserialized.data.data == "nested"