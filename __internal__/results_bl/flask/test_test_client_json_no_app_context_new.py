import pytest
from flask import Flask, json

def test_post_create_method(client):
    @app.route("/create", methods=["POST"])
    def create():
        return 'Create'

    rv = client.post("/create")
    assert rv.get_data(as_text=True) == 'Create'

def test_post_create_with_data(client):
    @app.route("/create", methods=["POST"])
    def create():
        data = flask.request.get_json()
        return f"Created with data: {data}"

    rv = client.post("/create", json={"key": "value"})
    assert rv.get_data(as_text=True) == 'Created with data: {"key": "value"}'

def test_post_create_no_data(client):
    @app.route("/create", methods=["POST"])
    def create():
        return 'Create'

    rv = client.post("/create", json={})
    assert rv.get_data(as_text=True) == 'Create'