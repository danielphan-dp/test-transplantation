import pytest
from sanic import Sanic
from sanic.response import text
from sanic_testing.reusable import ReusableClient

@pytest.fixture
def app():
    app = Sanic("TestApp")
    @app.post("/")
    async def handler(request):
        return text('I am post method')
    return app

def test_post_method_response(app):
    client = ReusableClient(app)

    with client:
        _, response = client.post("/")
    
    assert response.status == 200
    assert response.text == 'I am post method'

def test_post_method_multiple_requests(app):
    client = ReusableClient(app)

    with client:
        _, response1 = client.post("/")
        _, response2 = client.post("/")
    
    assert response1.status == response2.status == 200
    assert response1.text == response2.text == 'I am post method'

def test_post_method_edge_case(app):
    client = ReusableClient(app)

    with client:
        _, response = client.post("/", json={})
    
    assert response.status == 200
    assert response.text == 'I am post method'