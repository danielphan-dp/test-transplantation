import pytest
from flask import Flask

@pytest.fixture
def app():
    app = Flask(__name__)

    @app.route("/delete", methods=["DELETE"])
    def delete():
        return 'DELETE'

    return app

def test_delete_method(app, client):
    response = client.delete("/delete")
    assert response.status_code == 200
    assert response.data == b"DELETE"

def test_delete_method_not_allowed(app, client):
    response = client.get("/delete")
    assert response.status_code == 405
    assert sorted(response.allow) == ["DELETE"]

def test_delete_method_with_invalid_route(app, client):
    response = client.delete("/nonexistent")
    assert response.status_code == 404

def test_delete_method_with_additional_data(app, client):
    response = client.delete("/delete", data={"key": "value"})
    assert response.status_code == 200
    assert response.data == b"DELETE"