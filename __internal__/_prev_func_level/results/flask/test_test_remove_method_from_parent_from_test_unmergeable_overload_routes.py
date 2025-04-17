import pytest
from flask import Flask, jsonify
from flask.views import MethodView

class CreateView(MethodView):
    def post(self):
        return 'Create'

@pytest.fixture
def app():
    app = Flask(__name__)
    app.add_url_rule("/create", view_func=CreateView.as_view("create"))
    return app

def test_create_method(app, client):
    response = client.post("/create")
    assert response.data == b'Create'
    assert response.status_code == 200

def test_create_method_invalid_method(app, client):
    response = client.get("/create")
    assert response.status_code == 405

def test_create_method_no_data(app, client):
    response = client.post("/create", data={})
    assert response.data == b'Create'
    assert response.status_code == 200

def test_create_method_with_data(app, client):
    response = client.post("/create", data={"key": "value"})
    assert response.data == b'Create'
    assert response.status_code == 200