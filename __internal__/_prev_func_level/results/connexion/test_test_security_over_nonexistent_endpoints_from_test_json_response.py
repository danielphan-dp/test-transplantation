import pytest

class TestGetMethod:
    def test_get_with_kwargs(self):
        instance = PetsView()
        result = instance.get(param1='value1', param2='value2')
        assert result == {'name': 'get', 'param1': 'value1', 'param2': 'value2'}

    def test_get_without_kwargs(self):
        instance = PetsView()
        result = instance.get()
        assert result == [{'name': 'get'}]

    def test_get_with_empty_kwargs(self):
        instance = PetsView()
        result = instance.get(**{})
        assert result == {'name': 'get'}

    def test_get_with_none_kwargs(self):
        instance = PetsView()
        result = instance.get(param1=None)
        assert result == {'name': 'get', 'param1': None}