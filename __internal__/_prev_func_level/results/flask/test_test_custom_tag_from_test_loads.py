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

def test_loads_with_empty_string():
    s = TaggedJSONSerializer()
    s.register(TagFoo)
    result = s.loads(s.dumps(Foo("")))
    assert result.data == ""

def test_loads_with_none():
    s = TaggedJSONSerializer()
    s.register(TagFoo)
    result = s.loads(s.dumps(Foo(None)))
    assert result.data is None

def test_loads_with_invalid_data():
    s = TaggedJSONSerializer()
    s.register(TagFoo)
    with pytest.raises(ValueError):
        s.loads(s.dumps("invalid data"))

def test_loads_with_nested_foo():
    s = TaggedJSONSerializer()
    s.register(TagFoo)
    nested_foo = Foo(Foo("nested"))
    result = s.loads(s.dumps(nested_foo))
    assert result.data.data == "nested"

def test_loads_with_multiple_tags():
    class TagBar(JSONTag):
        __slots__ = ()
        key = " b"

        def check(self, value):
            return isinstance(value, str)

        def to_json(self, value):
            return self.serializer.tag(value)

        def to_python(self, value):
            return value

    s = TaggedJSONSerializer()
    s.register(TagFoo)
    s.register(TagBar)
    result_foo = s.loads(s.dumps(Foo("foo")))
    result_bar = s.loads(s.dumps("bar"))
    assert result_foo.data == "foo"
    assert result_bar == "bar"