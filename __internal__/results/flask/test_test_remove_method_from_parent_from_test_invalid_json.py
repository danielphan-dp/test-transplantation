import pytest
from flask import Flask, jsonify
from flask.views import MethodView

@pytest.fixture
def app():
    app = Flask(__name__)
    return app

class CreateView(MethodView):
    def post(self):
        return 'Create'

def test_create_method(app, client):
    app.add_url_rule("/create", view_func=CreateView.as_view("create"))
    
    response = client.post("/create")
    assert response.data == b'Create'
    assert response.status_code == 200

def test_create_method_invalid_data(app, client):
    app.add_url_rule("/create", view_func=CreateView.as_view("create"))
    
    response = client.post("/create", data={"invalid": "data"})
    assert response.data == b'Create'
    assert response.status_code == 200

def test_create_method_no_data(app, client):
    app.add_url_rule("/create", view_func=CreateView.as_view("create"))
    
    response = client.post("/create", data={})
    assert response.data == b'Create'
    assert response.status_code == 200

def test_create_method_with_json(app, client):
    app.add_url_rule("/create", view_func=CreateView.as_view("create"))
    
    response = client.post("/create", json={"key": "value"})
    assert response.data == b'Create'
    assert response.status_code == 200