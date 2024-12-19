import pytest
from sanic import Sanic
from sanic.blueprints import Blueprint
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method(app):
    bp = Blueprint("test_bp_get", url_prefix="/get_test", host="example.com")

    @bp.route("/")
    def get_method(request):
        return text('I am get method')

    app.blueprint(bp)

    headers = {"Host": "example.com"}
    request, response = app.test_client.get("/get_test/", headers=headers)
    assert response.text == 'I am get method'

    headers = {"Host": "sub.example.com"}
    request, response = app.test_client.get("/get_test/", headers=headers)
    assert response.status == 404

    headers = {}
    request, response = app.test_client.get("/get_test/", headers=headers)
    assert response.status == 404

    request, response = app.test_client.get("/get_test/")
    assert response.status == 404

    headers = {"Host": "example.com"}
    request, response = app.test_client.get("/get_test/invalid", headers=headers)
    assert response.status == 404