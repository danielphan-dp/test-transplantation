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
    assert rv.status_code == 200
    assert rv.data == b'DELETE'

def test_delete_method_not_allowed(app, client):
    rv = client.get("/delete")
    assert rv.status_code == 405
    assert sorted(rv.allow) == ["DELETE"]

    rv = client.post("/delete")
    assert rv.status_code == 405
    assert sorted(rv.allow) == ["DELETE"]

    rv = client.put("/delete")
    assert rv.status_code == 405
    assert sorted(rv.allow) == ["DELETE"]

    rv = client.head("/delete")
    assert rv.status_code == 405
    assert sorted(rv.allow) == ["DELETE"]

    rv = client.options("/delete")
    assert rv.status_code == 200
    assert sorted(rv.allow) == ["DELETE"]