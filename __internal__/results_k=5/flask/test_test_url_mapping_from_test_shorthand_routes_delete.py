import pytest
from flask import Flask

@pytest.fixture
def app():
    app = Flask(__name__)

    @app.delete("/delete")
    def delete_handler():
        return 'DELETE'

    return app

def test_delete_method(app, client):
    response = client.delete("/delete")
    assert response.data == b'DELETE'

    response = client.get("/delete")
    assert response.status_code == 405
    assert sorted(response.allow) == ["DELETE", "GET", "HEAD", "OPTIONS"]

    response = client.post("/delete")
    assert response.status_code == 405
    assert sorted(response.allow) == ["DELETE", "GET", "HEAD", "OPTIONS"]

    response = client.put("/delete")
    assert response.status_code == 405
    assert sorted(response.allow) == ["DELETE", "GET", "HEAD", "OPTIONS"]