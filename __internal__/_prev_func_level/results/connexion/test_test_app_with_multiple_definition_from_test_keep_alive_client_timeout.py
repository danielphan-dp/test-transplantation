import pytest

@pytest.mark.parametrize("kwargs, expected", [
    ({"key1": "value1"}, {"key1": "value1", "name": "get"}),
    ({"key2": "value2"}, {"key2": "value2", "name": "get"}),
    ({}, [{"name": "get"}]),
])
def test_get_method(kwargs, expected):
    class MockClass:
        def get(self, **kwargs):
            if kwargs:
                kwargs.update({'name': 'get'})
                return kwargs
            else:
                return [{'name': 'get'}]

    mock_instance = MockClass()
    result = mock_instance.get(**kwargs)
    assert result == expected