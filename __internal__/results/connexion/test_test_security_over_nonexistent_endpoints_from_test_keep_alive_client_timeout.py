import pytest

def test_get_method_with_kwargs():
    instance = PetsView()
    result = instance.get(param1='value1', param2='value2')
    assert result == {'name': 'get', 'param1': 'value1', 'param2': 'value2'}

def test_get_method_without_kwargs():
    instance = PetsView()
    result = instance.get()
    assert result == [{'name': 'get'}]

def test_get_method_with_empty_kwargs():
    instance = PetsView()
    result = instance.get(param1=None)
    assert result == {'name': 'get', 'param1': None}