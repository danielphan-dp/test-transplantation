import asyncio
import pytest
from sanic import Sanic
from sanic.response import text
from sanic.views import HTTPMethodView

app = Sanic("TestApp")

class SimpleView(HTTPMethodView):
    async def post(self, request):
        return text('I am post method')

app.add_route(SimpleView.as_view(), "/simple_view")

@pytest.mark.parametrize('headers, expect_raise_exception', [
    ({'EXPECT': '100-continue'}, False),
    ({'Content-Type': 'application/json'}, False),
    ({'Content-Length': '0'}, False),
    ({'Content-Type': 'text/plain'}, True)
])
async def test_simple_view_post(app, headers, expect_raise_exception):
    data = "Test data"
    
    if not expect_raise_exception:
        request, response = await app.test_client.post(
            "/simple_view", data=data, headers=headers
        )
        assert response.status == 200
        assert response.text == 'I am post method'
    else:
        request, response = await app.test_client.post(
            "/simple_view", data=data, headers=headers
        )
        assert response.status == 417