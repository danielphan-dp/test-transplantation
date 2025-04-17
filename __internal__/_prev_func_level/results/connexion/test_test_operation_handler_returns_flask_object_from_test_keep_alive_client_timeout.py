import pytest

@pytest.fixture
def valid_kwargs():
    return {'key1': 'value1', 'key2': 'value2'}

def test_get_with_kwargs(valid_kwargs):
    result = get(**valid_kwargs)
    assert result == {'key1': 'value1', 'key2': 'value2', 'name': 'get'}

def test_get_without_kwargs():
    result = get()
    assert result == [{'name': 'get'}]

def test_get_with_empty_kwargs():
    result = get(**{})
    assert result == {'name': 'get'}