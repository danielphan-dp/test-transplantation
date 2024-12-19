import json
import unittest.mock
import pytest
import connexion.App

def test_get_method_with_kwargs():
    app = connexion.App(__name__)

    @app.route("/test_get", methods=["GET"])
    def test_get(**kwargs):
        return get(**kwargs)

    app_client = app.test_client()

    response_with_kwargs = app_client.get("/test_get?key1=value1&key2=value2")
    assert response_with_kwargs.json == {'key1': 'value1', 'key2': 'value2', 'name': 'get'}

def test_get_method_without_kwargs():
    app = connexion.App(__name__)

    @app.route("/test_get_no_kwargs", methods=["GET"])
    def test_get_no_kwargs():
        return get()

    app_client = app.test_client()

    response_without_kwargs = app_client.get("/test_get_no_kwargs")
    assert response_without_kwargs.json == [{'name': 'get'}]

def test_get_method_with_empty_kwargs():
    app = connexion.App(__name__)

    @app.route("/test_get_empty_kwargs", methods=["GET"])
    def test_get_empty_kwargs():
        return get(**{})

    app_client = app.test_client()

    response_empty_kwargs = app_client.get("/test_get_empty_kwargs")
    assert response_empty_kwargs.json == [{'name': 'get'}]