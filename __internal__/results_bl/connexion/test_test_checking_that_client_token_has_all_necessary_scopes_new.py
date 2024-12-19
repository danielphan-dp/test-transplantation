import base64
import json
import pytest
from connexion import App
from connexion.exceptions import OAuthProblem
from connexion.security import NO_VALUE, BasicSecurityHandler, OAuthSecurityHandler

def test_get_method_with_kwargs():
    instance = App(__name__)
    result = instance.get(param1='value1', param2='value2')
    assert result == {'name': 'get', 'param1': 'value1', 'param2': 'value2'}

def test_get_method_without_kwargs():
    instance = App(__name__)
    result = instance.get()
    assert result == [{'name': 'get'}]

def test_get_method_with_empty_kwargs():
    instance = App(__name__)
    result = instance.get(**{})
    assert result == {'name': 'get'}

def test_get_method_with_none_kwargs():
    instance = App(__name__)
    result = instance.get(param1=None)
    assert result == {'name': 'get', 'param1': None}