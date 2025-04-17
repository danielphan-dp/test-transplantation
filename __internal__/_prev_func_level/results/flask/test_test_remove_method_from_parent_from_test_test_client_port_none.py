import pytest
from flask import Flask, request
from flask.views import MethodView

@pytest.fixture
def app():
    app = Flask(__name__)
    return app

class CreateView(MethodView):
    def post(self):
        return 'Create'

def test_create_view_post(app, client):
    app.add_url_rule("/create", view_func=CreateView.as_view("create"))
    
    response = client.post("/create")
    assert response.data == b'Create'
    
    response = client.get("/create")
    assert response.status_code == 405

def test_create_view_invalid_method(app, client):
    app.add_url_rule("/create", view_func=CreateView.as_view("create"))
    
    response = client.put("/create")
    assert response.status_code == 405

def test_create_view_methods(app):
    app.add_url_rule("/create", view_func=CreateView.as_view("create"))
    assert sorted(CreateView.methods) == ["POST"]