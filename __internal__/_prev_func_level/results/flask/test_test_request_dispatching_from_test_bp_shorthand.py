import pytest
from flask import Flask

@pytest.fixture
def app():
    app = Flask(__name__)

    @app.route("/delete", methods=["DELETE"])
    def delete():
        return 'DELETE'

    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_delete_method(client):
    rv = client.delete("/delete")
    assert rv.data == b"DELETE"
    assert rv.status_code == 200

def test_delete_method_not_allowed(client):
    rv = client.get("/delete")
    assert rv.status_code == 405
    assert sorted(rv.allow) == ["DELETE", "HEAD", "OPTIONS"]

def test_delete_method_with_invalid_route(client):
    rv = client.delete("/nonexistent")
    assert rv.status_code == 404

def test_delete_method_with_other_methods(client):
    rv = client.post("/delete")
    assert rv.status_code == 405
    assert sorted(rv.allow) == ["DELETE", "HEAD", "OPTIONS"]

    rv = client.put("/delete")
    assert rv.status_code == 405
    assert sorted(rv.allow) == ["DELETE", "HEAD", "OPTIONS"]

    rv = client.patch("/delete")
    assert rv.status_code == 405
    assert sorted(rv.allow) == ["DELETE", "HEAD", "OPTIONS"]