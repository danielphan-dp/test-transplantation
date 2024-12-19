import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt', 'python.png'])
def test_get_method(app: Sanic, file_name: str):
    @app.route("/get", methods=["GET"])
    def get_route(request):
        return text('I am get method')

    _, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.body == b'I am get method'

    _, response = app.test_client.get("/get", headers={"Custom-Header": "value"})
    assert response.status == 200
    assert response.body == b'I am get method'

    _, response = app.test_client.get("/get", headers={"Accept": "text/plain"})
    assert response.status == 200
    assert response.body == b'I am get method'

    _, response = app.test_client.get("/get", headers={"Accept": "application/json"})
    assert response.status == 200
    assert response.body == b'I am get method'