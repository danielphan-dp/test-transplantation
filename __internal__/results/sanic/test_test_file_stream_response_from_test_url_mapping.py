import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('method', ['GET', 'POST', 'PUT', 'DELETE'])
def test_http_methods(app: Sanic, method):
    @app.route("/", methods=["GET", "POST", "PUT", "DELETE"])
    def index(request):
        if request.method == "GET":
            return text("I am get method")
        elif request.method == "POST":
            return text("I am post method")
        elif request.method == "PUT":
            return text("I am put method")
        elif request.method == "DELETE":
            return text("I am delete method")
        return text("Method not allowed", status=405)

    request, response = app.test_client.get("/")
    assert response.status == 200
    assert response.text == "I am get method"

    request, response = app.test_client.post("/")
    assert response.status == 200
    assert response.text == "I am post method"

    request, response = app.test_client.put("/")
    assert response.status == 200
    assert response.text == "I am put method"

    request, response = app.test_client.delete("/")
    assert response.status == 200
    assert response.text == "I am delete method"

    request, response = app.test_client.head("/")
    assert response.status == 405
    assert "Method not allowed" in response.text

    request, response = app.test_client.options("/")
    assert response.status == 200
    assert "GET" in response.headers.get('Allow')
    assert "POST" in response.headers.get('Allow')
    assert "PUT" in response.headers.get('Allow')
    assert "DELETE" in response.headers.get('Allow')