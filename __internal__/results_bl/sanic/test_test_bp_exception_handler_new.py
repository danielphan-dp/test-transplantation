import pytest
from sanic.app import Sanic
from sanic.blueprints import Blueprint
from sanic.response import text

def test_get_method(app: Sanic):
    blueprint = Blueprint("test_get_method")

    @blueprint.route("/get", methods=["GET"])
    def get_method(request):
        return text('I am get method')

    app.blueprint(blueprint)

    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == 'I am get method'

    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404

    request, response = app.test_client.get("/get", headers={"Accept": "application/json"})
    assert response.status == 200
    assert response.text == 'I am get method'