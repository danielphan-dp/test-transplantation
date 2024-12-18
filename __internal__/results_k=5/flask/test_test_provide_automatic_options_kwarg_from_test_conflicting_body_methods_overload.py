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
    rv = client.delete("/delete")
    assert rv.data == b"DELETE"
    assert rv.status_code == 200

    rv = client.delete("/nonexistent")
    assert rv.status_code == 404

    rv = client.get("/delete")
    assert rv.status_code == 405
    assert sorted(rv.allow) == ["DELETE"]