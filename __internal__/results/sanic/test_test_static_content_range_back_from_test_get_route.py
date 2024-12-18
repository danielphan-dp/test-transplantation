import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt'])
def test_get_method(file_name):
    app = Sanic("test_app")

    @app.get("/")
    def get_method(request):
        return text("I am get method")

    request, response = app.test_client.get("/")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_with_query_params():
    app = Sanic("test_app")

    @app.get("/greet")
    def get_method(request):
        name = request.args.get('name', 'World')
        return text(f"Hello, {name}!")

    request, response = app.test_client.get("/greet?name=Alice")
    assert response.status == 200
    assert response.text == "Hello, Alice!"

    request, response = app.test_client.get("/greet")
    assert response.status == 200
    assert response.text == "Hello, World!"