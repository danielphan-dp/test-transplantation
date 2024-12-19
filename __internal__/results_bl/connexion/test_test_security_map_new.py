import base64
import json
import pytest
from connexion import App
from connexion.exceptions import OAuthProblem
from connexion.security import NO_VALUE, BasicSecurityHandler

def test_post_method_with_empty_kwargs():
    app = App(__name__)
    app_client = app.test_client()
    
    res = app_client.post("/v1.0/greeting_basic/")
    assert res.status_code == 201
    assert res.json == {'name': 'post'}

def test_post_method_with_additional_kwargs():
    app = App(__name__)
    app_client = app.test_client()
    
    res = app_client.post("/v1.0/greeting_basic/", json={'key': 'value'})
    assert res.status_code == 201
    assert res.json == {'name': 'post', 'key': 'value'}

def test_post_method_with_invalid_data():
    app = App(__name__)
    app_client = app.test_client()
    
    res = app_client.post("/v1.0/greeting_basic/", data='invalid_data')
    assert res.status_code == 400  # Assuming the API returns 400 for invalid data

def test_post_method_with_none_kwargs():
    app = App(__name__)
    app_client = app.test_client()
    
    res = app_client.post("/v1.0/greeting_basic/", json=None)
    assert res.status_code == 201
    assert res.json == {'name': 'post'}