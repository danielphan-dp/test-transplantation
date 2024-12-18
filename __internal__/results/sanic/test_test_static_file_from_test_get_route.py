import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt', 'python.png'])
def test_get_method(static_file_directory, file_name):
    app = Sanic("test_app")

    @app.get("/get")
    def get_method(request):
        return text('I am get method')

    app.router.finalize()

    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == 'I am get method'

    # Test for invalid route
    request, response = app.test_client.get("/invalid")
    assert response.status == 404

    # Test for other parameters
    uri = app.url_for("get_method", _external=True, _server="http://localhost")
    assert uri == "http://localhost/get"