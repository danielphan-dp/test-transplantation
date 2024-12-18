import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def json_app():
    app = Sanic("TestApp")

    @app.route("/", methods=["DELETE"])
    def delete(request):
        return text('I am delete method')

    return app

def test_delete_method(json_app):
    request, response = json_app.test_client.delete("/")
    assert response.status == 200
    assert response.text == 'I am delete method'
    assert "Content-Length" in response.headers
    assert response.headers["Content-Length"] == str(len(response.text))

def test_delete_method_no_content(json_app):
    request, response = json_app.test_client.delete("/no-content")
    assert response.status == 204
    assert response.text == ""
    assert "Content-Length" not in response.headers

def test_delete_method_unmodified(json_app):
    request, response = json_app.test_client.delete("/unmodified")
    assert response.status == 304
    assert response.text == ""
    assert "Content-Length" not in response.headers
    assert "Content-Type" not in response.headers

def test_delete_method_invalid_route(json_app):
    request, response = json_app.test_client.delete("/invalid-route")
    assert response.status == 404
    assert "Content-Length" in response.headers
    assert response.text == "Not Found"