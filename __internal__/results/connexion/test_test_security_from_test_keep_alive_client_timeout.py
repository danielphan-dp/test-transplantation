import pytest

def test_get_method_with_kwargs():
    instance = YourClass()  # Replace with the actual class name that contains the get method
    result = instance.get(param1='value1', param2='value2')
    assert result == {'name': 'get', 'param1': 'value1', 'param2': 'value2'}

def test_get_method_without_kwargs():
    instance = YourClass()  # Replace with the actual class name that contains the get method
    result = instance.get()
    assert result == [{'name': 'get'}]

def test_get_method_with_empty_kwargs():
    instance = YourClass()  # Replace with the actual class name that contains the get method
    result = instance.get(empty_param='')
    assert result == {'name': 'get', 'empty_param': ''}

def test_get_method_with_none_kwargs():
    instance = YourClass()  # Replace with the actual class name that contains the get method
    result = instance.get(param=None)
    assert result == {'name': 'get', 'param': None}