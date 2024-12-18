from __future__ import annotations
from flask import Flask, request
from flask.testing import FlaskClient
import pytest

def test_post_create(app: Flask, client: FlaskClient) -> None:
    @app.post("/create")
    def create():
        return 'Create'

    rv = client.post("/create")
    assert rv.data == b'Create'

def test_post_create_with_data(app: Flask, client: FlaskClient) -> None:
    @app.post("/create")
    def create():
        data = request.form.get("data")
        return data if data else 'No data'

    rv = client.post("/create", data={"data": "test"})
    assert rv.data == b'test'

def test_post_create_no_data(app: Flask, client: FlaskClient) -> None:
    @app.post("/create")
    def create():
        data = request.form.get("data")
        return data if data else 'No data'

    rv = client.post("/create")
    assert rv.data == b'No data'