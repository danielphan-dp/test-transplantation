import pytest
from flask import Flask, jsonify
from flask.views import MethodView

def test_post_method(app, client):
    class PostView(MethodView):
        def post(self):
            return 'Create'

    app.add_url_rule("/create", view_func=PostView.as_view("create"))

    response = client.post("/create")
    assert response.data == b'Create'
    assert response.status_code == 200

    response = client.get("/create")
    assert response.status_code == 405

    response = client.post("/")
    assert response.status_code == 404

    response = client.post("/create", json={"data": "test"})
    assert response.data == b'Create'
    assert response.status_code == 200