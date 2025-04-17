import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('override', (True, False))
def test_post_method(override):
    app = Sanic("Test")

    @app.post("/post")
    async def post_method(request):
        return text('I am post method')

    _, response = app.test_client.post("/post")
    assert response.status == 200
    assert response.text == 'I am post method'

    # Testing with additional payload
    payload = {"key": "value"}
    _, response_with_payload = app.test_client.post("/post", json=payload)
    assert response_with_payload.status == 200
    assert response_with_payload.text == 'I am post method'