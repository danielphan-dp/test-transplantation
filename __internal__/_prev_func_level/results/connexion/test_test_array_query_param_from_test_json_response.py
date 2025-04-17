import pytest
from typing import List

def test_get_method_with_kwargs(simple_app):
    app_client = simple_app.test_client()
    headers = {"Content-type": "application/json"}
    url = "/v1.0/get_method?param1=value1&param2=value2"
    response = app_client.get(url, headers=headers)
    kwargs_response: dict = response.json()
    assert kwargs_response == {'name': 'get', 'param1': 'value1', 'param2': 'value2'}

def test_get_method_without_kwargs(simple_app):
    app_client = simple_app.test_client()
    headers = {"Content-type": "application/json"}
    url = "/v1.0/get_method"
    response = app_client.get(url, headers=headers)
    kwargs_response: List[dict] = response.json()
    assert kwargs_response == [{'name': 'get'}]

def test_get_method_with_empty_kwargs(simple_app):
    app_client = simple_app.test_client()
    headers = {"Content-type": "application/json"}
    url = "/v1.0/get_method?"
    response = app_client.get(url, headers=headers)
    kwargs_response: List[dict] = response.json()
    assert kwargs_response == [{'name': 'get'}]

def test_get_method_with_special_characters(simple_app):
    app_client = simple_app.test_client()
    headers = {"Content-type": "application/json"}
    url = "/v1.0/get_method?param1=val%20ue&param2=val@ue"
    response = app_client.get(url, headers=headers)
    kwargs_response: dict = response.json()
    assert kwargs_response == {'name': 'get', 'param1': 'val ue', 'param2': 'val@ue'}