import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    @app.post("/rest/<resource>")
    def post(request, resource):
        return text('I am post method')
    return app

def test_post_method_success(app, sanic_testing):
    request, response = sanic_testing.post('/rest/test_resource')
    assert response.status == 200
    assert response.text == 'I am post method'

def test_post_method_invalid_resource(app, sanic_testing):
    request, response = sanic_testing.post('/rest/')
    assert response.status == 404

def test_post_method_no_resource(app, sanic_testing):
    request, response = sanic_testing.post('/rest')
    assert response.status == 404

def test_post_method_with_special_characters(app, sanic_testing):
    request, response = sanic_testing.post('/rest/test@resource!')
    assert response.status == 200
    assert response.text == 'I am post method'