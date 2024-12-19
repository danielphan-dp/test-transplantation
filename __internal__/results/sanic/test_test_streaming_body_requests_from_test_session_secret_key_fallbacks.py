import pytest
from sanic_testing.reusable import ReusableClient
from sanic.response import text

@pytest.mark.asyncio
async def test_post_method_response(app, port):
    @app.post("/")
    async def post_method(request):
        return text('I am post method')

    client = ReusableClient(app, port=port)

    request, response = await client.post("/")
    
    assert response.status == 200
    assert response.text == 'I am post method'

@pytest.mark.asyncio
async def test_post_method_with_invalid_data(app, port):
    @app.post("/")
    async def post_method(request):
        return text('I am post method')

    client = ReusableClient(app, port=port)

    request, response = await client.post("/", data="invalid data")
    
    assert response.status == 200
    assert response.text == 'I am post method'

@pytest.mark.asyncio
async def test_post_method_multiple_requests(app, port):
    @app.post("/")
    async def post_method(request):
        return text('I am post method')

    client = ReusableClient(app, port=port)

    request1, response1 = await client.post("/")
    request2, response2 = await client.post("/")

    assert response1.status == response2.status == 200
    assert response1.text == response2.text == 'I am post method'
    assert request1.id != request2.id

@pytest.mark.asyncio
async def test_post_method_streaming_data(app, port):
    @app.post("/", stream=True)
    async def post_method(request):
        data = [part.decode("utf-8") async for part in request.stream]
        return text('Received: ' + ', '.join(data))

    client = ReusableClient(app, port=port)

    async def stream(data):
        for value in data:
            yield value.encode("utf-8")

    data = ["hello", "world"]

    request, response = await client.post("/", data=stream(data))

    assert response.status == 200
    assert response.text == 'Received: hello, world'