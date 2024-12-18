import pytest

@pytest.mark.parametrize("kwargs, expected", [
    ({"key1": "value1"}, {"key1": "value1", "name": "get"}),
    ({"key2": "value2"}, {"key2": "value2", "name": "get"}),
    ({"key1": "value1", "key2": "value2"}, {"key1": "value1", "key2": "value2", "name": "get"}),
])
def test_get_with_kwargs(kwargs, expected):
    result = get(**kwargs)
    assert result == expected

def test_get_without_kwargs():
    result = get()
    assert result == [{'name': 'get'}]