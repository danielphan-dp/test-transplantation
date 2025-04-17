import pytest
from sanic_testing.reusable import ReusableClient
from sanic.response import text

@pytest.mark.asyncio
async def test_post_method_response(app, port):
    @app.post("/post")
    async def handler(request):
        return text('I am post method')

    client = ReusableClient(app, port=port)

    request, response = client.post("/post")
    
    assert response.status == 200
    assert response.text == 'I am post method'

@pytest.mark.asyncio
async def test_post_method_with_invalid_route(app, port):
    client = ReusableClient(app, port=port)

    request, response = client.post("/invalid_route")
    
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

@pytest.mark.asyncio
async def test_post_method_with_different_content_type(app, port):
    @app.post("/post")
    async def handler(request):
        return text('I am post method')

    client = ReusableClient(app, port=port)
    headers = {"Content-Type": "application/json"}
    
    request, response = client.post("/post", headers=headers)
    
    assert response.status == 200
    assert response.text == 'I am post method'