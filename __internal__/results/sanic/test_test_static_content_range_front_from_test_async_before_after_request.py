import pytest
from sanic import Sanic
from sanic.response import text
from sanic.blueprints import Blueprint

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt'])
def test_get_method(file_name, static_file_directory):
    app = Sanic("test_app")

    @app.get("/get")
    def get(request):
        return text('I am get method')

    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == 'I am get method'

    # Testing with additional headers
    headers = {"Custom-Header": "value"}
    request, response = app.test_client.get("/get", headers=headers)
    assert response.status == 200
    assert response.text == 'I am get method'
    assert response.headers["Custom-Header"] == "value"

    # Testing with query parameters
    request, response = app.test_client.get("/get?param=value")
    assert response.status == 200
    assert response.text == 'I am get method'

    # Testing with a blueprint
    bp = Blueprint("test_bp", url_prefix="/bp")
    @bp.get("/get")
    def bp_get(request):
        return text('I am get method from blueprint')

    app.blueprint(bp)

    request, response = app.test_client.get("/bp/get")
    assert response.status == 200
    assert response.text == 'I am get method from blueprint'