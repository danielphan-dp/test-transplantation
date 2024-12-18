import pytest

def test_get_method_with_kwargs():
    inst = PetsView()
    result = inst.get(param1='value1', param2='value2')
    assert result == {'name': 'get', 'param1': 'value1', 'param2': 'value2'}

def test_get_method_without_kwargs():
    inst = PetsView()
    result = inst.get()
    assert result == [{'name': 'get'}]

def test_get_method_with_empty_kwargs():
    inst = PetsView()
    result = inst.get(empty_param='')
    assert result == {'name': 'get', 'empty_param': ''}

def test_get_method_with_none_kwargs():
    inst = PetsView()
    result = inst.get(param1=None)
    assert result == {'name': 'get', 'param1': None}