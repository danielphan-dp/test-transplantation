import pytest
from flask import Flask
from flask.views import MethodView

class DeleteView(MethodView):
    def delete(self):
        return "DELETE"

@pytest.fixture
def app():
    app = Flask(__name__)
    app.add_url_rule("/delete", view_func=DeleteView.as_view("delete_view"))
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_delete_view(client):
    response = client.delete("/delete")
    assert response.data == b"DELETE"

def test_delete_view_not_allowed(client):
    response = client.get("/delete")
    assert response.status_code == 405  # Method Not Allowed

def test_delete_view_invalid_route(client):
    response = client.delete("/nonexistent")
    assert response.status_code == 404  # Not Found

def test_delete_view_content_type(client):
    response = client.delete("/delete")
    assert response.content_type == 'text/html; charset=utf-8'  # Check content type

def test_delete_view_response_type(client):
    response = client.delete("/delete")
    assert isinstance(response.data, bytes)  # Ensure response is in bytes
